from typing import Union, List, Tuple, Optional
from src.cambiacosas.administracion_archivo import file_info

def modify_file_lines(file_path: str, line_range: Optional[Union[Tuple[int, int], slice]], new_content: Union[str, List[str]]):
    """
    Modifica un archivo de texto, reemplazando un rango de líneas especificado con nuevo contenido.
    Si no se proporciona line_range, se modificará el archivo completo.

    Args:
        file_path (str): La ruta al archivo que se va a modificar.
        line_range (tuple o slice, opcional): Una tupla (start_line, end_line) o un objeto slice
                                      que define el rango de líneas basado en 1 para reemplazar (inclusivo).
                                      Si no se proporciona, se utiliza el rango completo del archivo.
        new_content (str o list de str): El contenido para reemplazar las líneas especificadas.
                                          Si es una cadena, se trata como un solo bloque de texto.
                                          Si es una lista de cadenas, cada cadena es una línea de nuevo contenido.

    Raises:
        FileNotFoundError: Si el file_path especificado no existe.
        ValueError: Si start_line > end_line, o si los números de línea no son enteros positivos,
                    o si el rango de líneas no es válido para el contenido del archivo.
        TypeError: Si los parámetros son de tipos incorrectos.

    Example:
        modify_file_lines("my_file.txt", (2, 4), "This is the new line 2.\\nThis is the new line 3.\\nThis is the new line 4.")
        modify_file_lines("my_file.txt", slice(2, 5), ["New line 2", "New line 3", "New line 4"])
        modify_file_lines("my_file.txt", "This replaces the entire file content") # Replaces entire file
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path debe ser una cadena de texto.")
    if line_range is not None and not isinstance(line_range, (tuple, slice)):
        raise TypeError("line_range debe ser una tupla o un slice.")
    if not isinstance(new_content, (str, list)):
        raise TypeError("new_content debe ser una cadena de texto o una lista de cadenas de texto.")

    if line_range is not None and isinstance(line_range, tuple):
        if len(line_range) != 2:
            raise ValueError("La tupla line_range debe contener exactamente dos enteros (start_line, end_line).")
        start_line, end_line = line_range
    elif line_range is not None and isinstance(line_range, slice):
        start_line = line_range.start
        end_line = line_range.stop
        if line_range.step is not None:
            raise ValueError("El paso de slice no está soportado para line_range.")
    elif line_range is None:
        start_line = 1
        end_line = None  # Se determinará después de leer el archivo
    else:
        raise TypeError("line_range debe ser una tupla, un slice o None.")

    if line_range is not None:
        if not isinstance(start_line, int) or not isinstance(end_line, int):
            raise TypeError("Las líneas de inicio y fin deben ser enteros.")
        if start_line <= 0 or end_line <= 0:
            raise ValueError("Las líneas de inicio y fin deben ser enteros positivos.")
        if start_line > end_line:
            raise ValueError("start_line no puede ser mayor que end_line.")

    try:
        file_info_dict = file_info.get_file_info(file_path)
        total_lines = file_info_dict['line_count']
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    if line_range is None:
        end_line = total_lines  # Establecer end_line al final del archivo si line_range es None
    elif start_line > total_lines or end_line > total_lines:
        raise ValueError("El rango de líneas especificado excede el número de líneas en el archivo.")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if isinstance(new_content, str):
        new_lines = [line + '\n' if not line.endswith('\n') else line for line in new_content.splitlines()]
    else:  # lista de cadenas de texto
        new_lines = [line + '\n' if not line.endswith('\n') else line for line in new_content]

    modified_lines = lines[:start_line-1] + new_lines + lines[end_line:]

    print("líneas_modificadas:", modified_lines)
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)