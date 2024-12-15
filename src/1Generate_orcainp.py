import os
import subprocess
import sys
import re

def sanitize_name(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)

def generate_orcainp(name, sequence, bases, functionals):
    try:
        os.makedirs(name, exist_ok=True)
        
        smiles_file_path = os.path.join(name, f"{name}.smiles")
        with open(smiles_file_path, 'w') as smiles_file:
            smiles_file.write(sequence)
        
        for functional in functionals:
            for base in bases:
                try:
                    sanitized_base = sanitize_name(base)
                    combo_name = f"{name}_{functional}_{sanitized_base}"
                    combo_dir = os.path.join(name, combo_name)
                    os.makedirs(combo_dir, exist_ok=True)
                    
                    orcainp_file_path = os.path.join(combo_dir, f"{combo_name}.orcainp")
                    
                    # Comando para Open Babel
                    command = f'obabel {smiles_file_path} -O {orcainp_file_path} -xk "!{functional} {base} Opt CPCM(WATER)" --gen3d'
                    
                    # Ejecutar el comando Open Babel
                    subprocess.run(command, shell=True, check=True)
                    
                    print(f"Archivo {combo_name}.orcainp creado en la carpeta {combo_dir}.")
                
                except subprocess.CalledProcessError as e:
                    print(f"Error al generar {combo_name}.orcainp. Error: {e}. Continuando con la siguiente combinación...")
                
                except Exception as e:
                    print(f"Error inesperado al generar {combo_name}.orcainp. Error: {e}. Continuando con la siguiente combinación...")
    
    except Exception as e:
        print(f"Error en el proceso general: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python generate_orcainp.py <nombre> <secuencia>")
        sys.exit(1)
    
    nombre = sys.argv[1]
    secuencia = sys.argv[2]
    
    bases = ["STO-3G", "6-311+G**", "def2-TZVP"]
    functionals = ["B3LYP", "PBE", "TPSS"]
    
    generate_orcainp(nombre, secuencia, bases, functionals)
