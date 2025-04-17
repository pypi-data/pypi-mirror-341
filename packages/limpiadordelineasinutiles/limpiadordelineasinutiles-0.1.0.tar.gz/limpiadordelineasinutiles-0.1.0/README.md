# Limpiador de Líneas Inútiles (Uso personal)

Este script te ayuda a limpiar esos archivos Markdown que a veces se llenan de líneas vacías innecesarias.


Este script en Python tiene las siguientes funciones:

*   **`main()`**: Función principal del script. Configura el analizador de argumentos y procesa el directorio especificado.
*   **`process_directory(directory)`**: Procesa recursivamente el directorio especificado para eliminar líneas vacías de los archivos Markdown y TXT.
    *   `directory` (str): El directorio a procesar.
*   **`clean_empty_lines(content)`**: Elimina las líneas vacías de un texto, excepto dentro de los bloques de código.
    *   `content` (str): El texto a limpiar.
    *   Returns: El texto limpio.

## Ejemplo

Para procesar el directorio `mi_proyecto`:

```bash
python limpiadordelineasinutiles.py mi_proyecto
```