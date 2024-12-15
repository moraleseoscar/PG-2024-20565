import os
import subprocess
import sys

def run_orca(name, bases, functionals):
    try:
        for functional in functionals:
            for base in bases:
                try:
                    sanitized_base = base.replace("*", "")
                    combo_name = f"{name}_{functional}_{sanitized_base}"
                    combo_dir = os.path.join(name, combo_name)
                    orcainp_file_path = os.path.join(combo_dir, f"{combo_name}.orcainp")
                    
                    if not os.path.exists(orcainp_file_path):
                        print(f"No se encontró {orcainp_file_path}. Saltando...")
                        continue
                    
                    orca_output_dir = os.path.join(combo_dir, f"{combo_name}_orca_files")
                    os.makedirs(orca_output_dir, exist_ok=True)
                    
                    orca_command = f"orca {orcainp_file_path} > {os.path.join(orca_output_dir, f'{combo_name}.out')}"
                    
                    print(f"Ejecutando optimización con ORCA para {combo_name}...")
                    
                    subprocess.run(orca_command, shell=True, check=True)
                    
                    print(f"Cálculo de ORCA completado para {combo_name}. Archivos generados en la carpeta {orca_output_dir}.")
                
                except subprocess.CalledProcessError as e:
                    print(f"Error al procesar {combo_name}. Error: {e}. Continuando con la siguiente combinación...")
                
                except Exception as e:
                    print(f"Error inesperado al procesar {combo_name}. Error: {e}. Continuando con la siguiente combinación...")
    
    except Exception as e:
        print(f"Error en el proceso general: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python run_orca.py <nombre>")
        sys.exit(1)
    
    nombre = sys.argv[1]
    
    bases = ["STO-3G", "6-311+G**", "def2-TZVP"]
    functionals = ["B3LYP", "PBE", "TPSS"]
    
    run_orca(nombre, bases, functionals)
