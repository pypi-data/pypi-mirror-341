import os


class GeminiOptionsError(Exception):
    """Excepción base para errores en las opciones de Gemini."""
    pass

class GeminiAPIKeyError(GeminiOptionsError):
    """Excepción para errores relacionados con la clave de API de Gemini."""
    pass

class GeminisOptions:
    """
    Opciones para la API de Gemini.

    Esta clase configura las opciones necesarias para interactuar con la API de Gemini,
    incluyendo la clave de API, el modelo a utilizar, la URL de la API, las cabeceras,
    el método HTTP y el cuerpo de la petición.
    """
    def __init__(self):
        """
        Inicializa las opciones de Gemini.

        Configura la clave de API, el modelo por defecto, la URL de la API, las cabeceras,
        el método HTTP y el cuerpo de la petición con valores predeterminados.
        La clave de API se obtiene de la variable de entorno 'GEMINI_API_KEY'.
        """
        api_key = os.environ.get("GEMINI_API_KEY") # Obtiene la clave de API de las variables de entorno
        if not api_key:
            raise GeminiAPIKeyError("Error: La variable de entorno 'GEMINI_API_KEY' no está configurada. Por favor, configura tu clave de API de Gemini.")
        self.api_key = api_key
        self.model_id = "gemini-2.0-flash" # Modelo por defecto
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:streamGenerateContent?key={self.api_key}" # URL de la API
        self.headers = {"Content-Type": "application/json"} # Cabeceras para la petición JSON
        self.method = "POST" # Método HTTP POST
        self.body = { # Cuerpo de la petición
            "contents": [
                {
                    "role": "user", # Rol del contenido: usuario
                    "parts": [
                        {
                            "text": "INSERT_INPUT_HERE" # Texto de entrada del usuario (se reemplaza dinámicamente)
                        }
                    ]
                }
            ],
            "systemInstruction": { # Instrucciones para el sistema (actualmente vacías)
                "parts": [
                    {
                        "text": "    "
                    }
                ]
            },
            "generationConfig": { # Configuración de generación
                "responseMimeType": "application/json", # Tipo MIME de la respuesta esperado: JSON
                "responseSchema": { # Esquema de la respuesta esperado
                    "type": "object",
                    "properties": {
                        "response": {
                            "type": "string" # La propiedad 'response' debe ser de tipo string
                        }
                    }
                }
            }
        }

    def set_input_text(self, input_text):
        """
        Establece el texto de entrada para la petición a la API de Gemini.

        Args:
            input_text (str): El texto de entrada del usuario.
        """
        try:
            self.body["contents"][0]["parts"][0]["text"] = input_text # Actualiza el texto de entrada en el cuerpo de la petición
        except Exception as e:
            raise GeminiOptionsError(f"Error al establecer el texto de entrada: {e}") from e

    def set_model(self, model):
        """
        Establece el modelo de Gemini a utilizar.

        Args:
            model (str): El ID del modelo de Gemini.
        """
        try:
            self.model_id = model # Actualiza el ID del modelo
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:streamGenerateContent?key={self.api_key}" # Reconstruye la URL con el nuevo modelo
            if model == "gemini-2.0-flash": # Configuración específica para el modelo 'gemini-2.0-flash'
                self.body["generationConfig"]["responseMimeType"] = "application/json" # Espera respuesta en JSON
                if "responseSchema" not in self.body["generationConfig"]: # Asegura que el esquema de respuesta esté definido
                    self.body["generationConfig"]["responseSchema"] = {
                        "type": "object",
                        "properties": {
                            "response": {
                                "type": "string"
                            }
                        }
                    }
            else:  # model == "gemini-2.0-flash-thinking-exp-01-21" # Configuración para otros modelos (ej. 'gemini-2.0-flash-thinking-exp-01-21')
                self.body["generationConfig"]["responseMimeType"] = "text/plain" # Espera respuesta en texto plano
                if "responseSchema" in self.body["generationConfig"]: # Elimina el esquema de respuesta si existe
                    del self.body["generationConfig"]["responseSchema"]
        except Exception as e:
            raise GeminiOptionsError(f"Error al establecer el modelo: {e}") from e

    def set_response_schema(self, response_schema):
        """
        Establece el esquema de respuesta esperado para la API de Gemini.

        Args:
            response_schema (dict): El esquema de respuesta en formato diccionario.
        """
        try:
            self.body["generationConfig"]["responseMimeType"] = "application/json" # Asegura que el tipo MIME sea JSON
            self.body["generationConfig"]["responseSchema"] = response_schema # Establece el esquema de respuesta
        except Exception as e:
            raise GeminiOptionsError(f"Error al establecer el esquema de respuesta: {e}") from e

    def set_system_instruction(self, system_instruction):
        """
        Establece las instrucciones del sistema para la API de Gemini.

        Args:
            system_instruction (str): Las instrucciones del sistema en formato string.
        """
        try:
            self.body["systemInstruction"]["parts"][0]["text"] = system_instruction # Actualiza las instrucciones del sistema en el cuerpo de la petición
        except Exception as e:
            raise GeminiOptionsError(f"Error al establecer las instrucciones del sistema: {e}") from e