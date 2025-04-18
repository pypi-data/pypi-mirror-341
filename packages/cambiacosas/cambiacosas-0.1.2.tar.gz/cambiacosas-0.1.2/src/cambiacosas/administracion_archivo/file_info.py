import os
from typing import Dict, Any

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Obtiene información sobre un archivo.

   Args:
        file_path: La ruta al archivo.

    Returns:
        Un diccionario que contiene información del archivo, incluyendo:
        - name: El nombre del archivo sin la ruta.
        - metadata: Un diccionario que contiene metadatos del archivo (tamaño, fecha de modificación, tipo de archivo).
        - full_path: La ruta absoluta al archivo.
        - content: El contenido del archivo como una cadena de texto.
        - line_count: El número de líneas del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        PermissionError: Si el archivo no se puede leer debido a permisos.
        Exception: Para otros errores inesperados durante el procesamiento del archivo.
    """
    try:
        full_path = os.path.abspath(file_path)
        file_name = os.path.basename(file_path)
        file_stats = os.stat(file_path)

        metadata = {
            "size": file_stats.st_size,
            "modification_date": file_stats.st_mtime, # Considerar formatear esta fecha para mejor legibilidad
            "file_type": "file", # Determinar el tipo de archivo con mayor precisión si es necesario (ej., usando mimetypes)
        }

        with open(file_path, 'r') as file: # Asumiendo archivos de texto, manejar binarios si es necesario
            content = file.read()

        return {
            "name": file_name,
            "metadata": metadata,
            "full_path": full_path,
            "content": content,
            "line_count": len(content.splitlines()),
        }

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied to read file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while processing file: {file_path}. Error: {e}")