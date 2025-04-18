import sys
import os
import pathlib
import tempfile
import argparse 

from typing import List, Dict, Union
from src.cambiacosas.administracion_archivo.file_info import get_file_info
from src.cambiacosas.administracion_archivo.edit_file import modify_file_lines
from src.cambiacosas.googleapi.gemini_options import GeminisOptions
from src.cambiacosas.googleapi.api_client import call_gemini_api, parse_gemini_response


def scan_folder(folder_path: str) -> list[dict]:
    """
    Escanea todos los archivos en la carpeta especificada y recupera información del archivo.

    Args:
        folder_path (str): Ruta a la carpeta para escanear.

    Returns:
        list[dict]: Una lista de diccionarios, donde cada diccionario contiene
                      información del archivo obtenida de get_file_info.
    """
    file_info_list = []
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"Ruta de carpeta no válida: {folder_path}")

    for file_path_obj in folder.rglob('*'):
        if file_path_obj.is_file():
            try:
                file_info = get_file_info(str(file_path_obj))  # get_file_info expects string path
                file_info_list.append(file_info)
            except Exception as e:
                print(f"Error al procesar el archivo {file_path_obj}: {e}")  # Registra el error y continua
    return file_info_list


def process_large_file(file_info: Dict, prompt_content: str, divide: bool) -> Union[str, bool]:
    """
    Procesa un archivo grande (>300 líneas).
    Si divide es False, divide en fragmentos, procesa cada uno, combina los resultados y devuelve la cadena combinada.
    Si divide es True, divide en fragmentos, procesa cada uno, guarda cada fragmento permanentemente y devuelve True si tiene éxito, False si falla.

    Args:
        file_info (Dict): Información del archivo ('full_path', 'name', 'content').
        prompt_content (str): El prompt para aplicar a cada fragmento.
        divide (bool): Si es True, guarda los fragmentos como archivos separados en lugar de fusionarlos.

    Returns:
        Union[str, bool]: Cadena de contenido combinada si divide es False y tiene éxito.
                          True si divide es True y tiene éxito.
                          Una cadena vacía o False si falla el procesamiento.
    """

    lines = file_info['content'].splitlines(keepends=True)
    chunk_size = 300
    total_chunks = (len(lines) + chunk_size - 1) // chunk_size
    modified_chunks_content = []
    temp_files = []
    processed_chunk_paths = []  # Keep track of successfully saved permanent chunks if divide=True

    original_path = pathlib.Path(file_info['full_path'])
    original_name = file_info['name']

    try:
        for i in range(0, len(lines), chunk_size):
            chunk_index = i // chunk_size
            chunk_lines = lines[i:i + chunk_size]
            chunk_content = "".join(chunk_lines)
            chunk_num = chunk_index + 1

            print(f"    Procesando fragmento {chunk_num}/{total_chunks} para {original_name}...")

            # --- Llamada a la API de Gemini ---
            gemini_config = GeminisOptions()
            input_text = f"Eres una herramienta que lee un archivo, aplica el siguiente cambio — '{prompt_content}' — y reescribe el archivo con la modificación.\\n'{chunk_content}'"
            gemini_config.set_input_text(input_text)

            api_response = call_gemini_api(gemini_config)
            if not api_response:
                print(f"    Error al llamar a la API de Gemini para el fragmento {chunk_num} de {original_name}.")
                # Si se divide, idealmente deberíamos limpiar los fragmentos guardados previamente, pero por simplicidad, simplemente fallamos.
                return False if divide else ""

            modified_chunk_data = parse_gemini_response(api_response)
            if not modified_chunk_data:
                print(f"    Error al analizar la respuesta de Gemini para el fragmento {chunk_num} de {original_name}.")
                return False if divide else ""

            # Extract text content from response
            if isinstance(modified_chunk_data, dict) and modified_chunk_data:
                modified_text = next(iter(modified_chunk_data.values()), None)
                if modified_text is None or not isinstance(modified_text, str):
                    print(f"    Contenido de texto no válido en la respuesta de Gemini para el fragmento {chunk_num} de {original_name}: {modified_chunk_data}")
                    return False if divide else ""
            else:
                print(f"    Respuesta no válida o vacía de parse_gemini_response para el fragmento {chunk_num} de {original_name}: {modified_chunk_data}")
                return False if divide else ""
            # --- Fin de la llamada a la API de Gemini ---

            if divide:
                # Save chunk permanently
                output_filename = f"{original_path.stem}.part{chunk_num}{original_path.suffix}"
                output_path = original_path.parent / output_filename
                try:
                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(modified_text)
                    processed_chunk_paths.append(output_path)  # Seguimiento del éxito
                    print(f"    Fragmento {chunk_num} procesado y guardado con éxito en {output_filename}.")
                except IOError as e:
                    print(f"    Error al escribir el archivo de fragmento permanente {output_filename}: {e}")
                    # ¿Limpiar los fragmentos ya guardados para este archivo? Tal vez sea demasiado complejo por ahora. Falla explícitamente.
                    return False  # Indica falla para el modo de división
            else:
                # Usar archivo temporal y almacenar contenido para fusionar (lógica existente)
                # Crear un archivo temporal para el fragmento (necesario para el seguimiento de la limpieza)
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding='utf-8') as temp_f:
                    # Ya no necesitamos estrictamente escribir el fragmento original aquí,
                    # pero necesitamos la ruta del archivo temporal para el bloque final.
                    # Simplemente hagamos un seguimiento de las rutas sin escribir.
                    temp_path = temp_f.name
                    temp_files.append(temp_path)  # Seguimiento para la limpieza

                modified_chunks_content.append(modified_text)
                print(f"    Fragmento {chunk_num} procesado con éxito.")

        # --- Loop finished ---
        if divide:
            # Si llegamos aquí, todos los fragmentos se procesaron y guardaron con éxito
            return True
        else:
            # Combinar fragmentos modificados
            return "".join(modified_chunks_content)

    except Exception as e:
        print(f"    Se produjo un error durante el procesamiento de archivos grandes para {original_name}: {e}")
        return False if divide else ""  # Indica falla
    finally:
        # Limpiar archivos temporales SOLO si no se divide
        if not divide:
            for temp_path in temp_files:
                try:
                    os.remove(temp_path)
                except OSError as e:
                    print(f"    Advertencia: No se pudo eliminar el archivo temporal {temp_path}: {e}")


def process_files_with_gemini(file_info_list: List[Dict], prompt_content: str, divide: bool):
    """
    Procesa cada archivo usando la API de Gemini. Maneja archivos grandes dividiéndolos en fragmentos.
    Si divide es True, los archivos grandes se dividen en archivos de fragmentos permanentes y el original se elimina si tiene éxito.

    Args:
        file_info_list (List[Dict]): Lista de diccionarios de información de archivos.
        prompt_content (str): El prompt para aplicar.
        divide (bool): Indica si se deben dividir los archivos grandes en fragmentos permanentes.
    """
    for file_info in file_info_list:
        original_file_path = file_info['full_path']  # Almacenar para posible eliminación
        original_file_name = file_info['name']
        print(f"Procesando archivo: {original_file_path}...")
        try:
            # Comprobar el número de líneas en el archivo
            line_count = len(file_info['content'].splitlines())
            text_content = ""  # Inicializar text_content para el caso sin división
            process_as_large_file = line_count > 300
            skip_final_write = False  # Bandera para omitir la escritura si se divide

            if process_as_large_file:
                print(f"  El archivo {original_file_name} tiene {line_count} líneas, superando las 300 líneas. Procesando en fragmentos...")
                # Llamar a process_large_file con la bandera de división
                large_file_result = process_large_file(file_info, prompt_content, divide)

                if divide:
                    if large_file_result is True:
                        print(f"  Se procesó y dividió con éxito el archivo grande {original_file_name} en fragmentos.")
                        skip_final_write = True  # No reescribir el original
                        # Intentar eliminar el archivo original
                        try:
                            os.remove(original_file_path)
                            print(f"  Se eliminó con éxito el archivo grande original: {original_file_name}")
                        except OSError as e:
                            print(f"  Advertencia: No se pudo eliminar el archivo grande original {original_file_name}: {e}")
                        # Dividido con éxito, continuar con el siguiente archivo en la lista
                        continue
                    else:  # large_file_result es False
                        print(f"  No se pudo procesar y dividir el archivo grande {original_file_name}.")
                        continue  # Saltar al siguiente archivo
                else:  # No se divide, se espera una cadena de contenido combinada
                    # Comprobar si el resultado es una cadena no vacía (éxito)
                    if isinstance(large_file_result, str) and large_file_result:
                         text_content = large_file_result  # Usar el contenido combinado
                    else:  # El resultado es una cadena vacía "" (falla)
                        print(f"  No se pudo procesar el archivo grande {original_file_name} para la fusión.")
                        continue  # Saltar al siguiente archivo

            else:  # Procesar normalmente para archivos <= 300 líneas
                # Crear instancia de GeminisOptions
                gemini_config = GeminisOptions()

                # Formatear el texto de entrada y establecerlo
                input_text = f"Eres una herramienta que lee un archivo, aplica el siguiente cambio — '{prompt_content}' — y reescribe el archivo con la modificación.\\n'{file_info['content']}'"
                gemini_config.set_input_text(input_text)

                # Llamar a la API de Gemini
                api_response = call_gemini_api(gemini_config)
                if not api_response:
                    print(f"  Error al llamar a la API de Gemini para {file_info['name']}.")
                    continue  # Saltar al siguiente archivo

                # Analizar la respuesta
                modified_content_data = parse_gemini_response(api_response)
                if not modified_content_data:
                    print(f"  Error al analizar la respuesta de Gemini para {file_info['name']}.")
                    continue  # Saltar al siguiente archivo

                # Extraer el contenido de texto del diccionario de respuesta
                if isinstance(modified_content_data, dict) and modified_content_data:
                    extracted_text = next(iter(modified_content_data.values()), None)
                    if extracted_text is None or not isinstance(extracted_text, str):
                        print(f"  No se pudo extraer contenido de texto válido del diccionario de respuesta de Gemini para {file_info['name']}: {modified_content_data}")
                        continue  # Saltar al siguiente archivo
                    text_content = extracted_text  # Asignar el texto extraído
                else:
                    print(f"  Se recibió un diccionario no válido o vacío de parse_gemini_response para {file_info['name']}: {modified_content_data}")
                    continue  # Saltar al siguiente archivo

            # --- Fin del if/else para el procesamiento de archivos grandes/pequeños ---

            # Escribir el contenido modificado final de nuevo en el archivo original
            # Esto solo debería suceder si NO estamos dividiendo un archivo grande.
            if not skip_final_write:
                if text_content:  # Asegurarse de que tenemos contenido para escribir (de un archivo pequeño o un archivo grande fusionado)
                    modify_file_lines(file_path=original_file_path, line_range=None, new_content=text_content)
                    print(f"  Se modificó con éxito {original_file_name}.")
                else:
                    # Este caso implica que ocurrió un problema en el procesamiento de archivos pequeños o en la fusión de archivos grandes
                    # (o el procesamiento de archivos grandes falló antes de establecer text_content)
                    if not process_as_large_file:  # Solo imprimir si no fue una falla de archivo grande (ya registrado)
                        print(f"  No se generó contenido válido para {original_file_name}, omitiendo la modificación.")

        except Exception as e:
            print(f"  Se produjo un error al procesar {original_file_name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Procesa archivos usando la API de Gemini, con fragmentación opcional para archivos grandes.")
    parser.add_argument("folder_name", help="Ruta a la carpeta que contiene los archivos para procesar.")
    parser.add_argument("prompt_file", help="Ruta al archivo que contiene el prompt de procesamiento.")
    parser.add_argument("--divide", action="store_true", help="Divide archivos grandes (>300 líneas) en archivos de fragmentos procesados separados en lugar de fusionarlos.")

    args = parser.parse_args()

    folder_name = args.folder_name
    prompt_file_path = args.prompt_file
    divide_flag = args.divide

    # Leer el contenido del archivo de prompt
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        if not prompt_content:
             raise ValueError("El archivo de prompt está vacío.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de prompt en {prompt_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo de prompt: {e}")
        sys.exit(1)

    try:
        print(f"Escaneando carpeta: {folder_name}...")
        file_info_results = scan_folder(folder_name)
        print(f"Se encontraron {len(file_info_results)} archivos.")

        if file_info_results:
             print("Procesando archivos con Gemini...")
             process_files_with_gemini(file_info_results, prompt_content, divide_flag)  # Pasar la bandera de división
             print("Procesamiento de archivos finalizado.")
        else:
             print("No se encontraron archivos para procesar.")

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()