# cambiacosas

cambiacosas es un script de Python que procesa archivos en una carpeta especificada utilizando la API de Gemini. Modifica los archivos basándose en un prompt proporcionado en un archivo separado.

## Uso

```bash
python -m cambiacosas <nombre_carpeta> <archivo_prompt> [--divide]
```

- `<nombre_carpeta>`: Ruta a la carpeta que contiene los archivos a procesar.
- `<archivo_prompt>`: Ruta al archivo que contiene el prompt de procesamiento.
- `--divide`: (Opcional) Si está presente, los archivos grandes (>300 líneas) se dividen en archivos de fragmentos procesados separados en lugar de fusionarlos.