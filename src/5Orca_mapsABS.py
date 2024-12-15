import os
import subprocess
import glob
import sys

# Función para ejecutar el comando orca_mapspc.exe
def generate_abs_file(out_file):
    # Comando que se ejecutará para generar el archivo .abs
    command = f"orca_mapspc.exe {out_file} abs -x030000 -x160000 -w200 -n5000"
    
    try:
        # Ejecutar el comando en el shell
        print(f"Ejecutando: {command}")
        subprocess.run(command, shell=True, check=True)
        print(f"Archivo .abs generado para {out_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando para {out_file}: {e}")

# Función principal
def main():
    # Verificar que se haya pasado la carpeta como argumento
    if len(sys.argv) != 2:
        print("Uso: python Get_Abs_From_Out.py <Carpeta>")
        sys.exit(1)
    
    # Obtener el directorio desde los argumentos
    base_directory = sys.argv[1]

    # Verificar si la carpeta existe
    if not os.path.exists(base_directory):
        print(f"La carpeta {base_directory} no existe.")
        sys.exit(1)

    # Buscar todos los archivos que terminen con "_toSpect.out" en todas las subcarpetas
    out_files = glob.glob(os.path.join(base_directory, '**', '*_toSpect.out'), recursive=True)

    # Si no se encuentran archivos, mostrar un mensaje
    if not out_files:
        print(f"No se encontraron archivos que terminen en '_toSpect.out' en la carpeta {base_directory}.")
    else:
        # Procesar cada archivo encontrado
        for out_file in out_files:
            print(f"Procesando archivo: {out_file}")
            generate_abs_file(out_file)

if __name__ == "__main__":
    main()
