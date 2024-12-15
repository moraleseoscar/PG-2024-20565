import os
import shutil
import sys
import subprocess

def run_orca(antiinflamatorio):
    try:
        base_dir = os.getcwd()  
        anti_dir = os.path.join(base_dir, f"Complejos/CMC-{antiinflamatorio}")
        orca_dir = os.path.join(anti_dir, f"CMC-{antiinflamatorio}-OrcaFiles")
        inp_file = f"Complejo_CMC{antiinflamatorio}.inp"
        inp_path = os.path.join(anti_dir, inp_file)
        

        if not os.path.exists(orca_dir):
            os.makedirs(orca_dir)  
            print(f"Carpeta creada: {orca_dir}")
        
        new_inp_path = os.path.join(orca_dir, inp_file)
        shutil.copy(inp_path, new_inp_path)
        
        orca_command = f"orca {new_inp_path} > {new_inp_path.replace('.inp', '.out')}"
        print(f"Comando orca corriendo en: {new_inp_path}")
        subprocess.run(orca_command, shell=True, check=True)
        print(f"Completado correctamente para {antiinflamatorio}")

    except Exception as e:
        print(f"Ocurrió un error con {antiinflamatorio}: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione al menos un antiinflamatorio.")
        sys.exit(1)

    antiinflamatorios = sys.argv[1:]
    
    for anti in antiinflamatorios:
        run_orca(anti)
