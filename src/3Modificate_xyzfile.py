import os
import re
import sys

def sanitize_name(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)

def modify_orcainp_xyz(file_path, functional, base):
    # Leer las líneas del archivo original
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Eliminar las primeras dos líneas
    lines = lines[2:]
    
    # Crear el encabezado personalizado
    header = f"# ORCA xyz input file \n# \n!{functional} {base} CPCM(WATER) LARGEPRINT \n"
    header += "%tddft\n    NRoots 30\n    MaxDim 5\nend\n"
    header += "* xyz 0 1\n"
    
    # Combinar el encabezado con el contenido restante del archivo
    modified_content = header + ''.join(lines) + "*\n"
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Modificaciones completadas en {file_path}")

def process_directory(directory, functionals, bases):
    for functional in functionals:
        for base in bases:
            sanitized_base = sanitize_name(base)
            file_name_pattern = f"{functional}_{sanitized_base}.orcainp.xyz"
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".orcainp.xyz") and file_name_pattern in file:
                        file_path = os.path.join(root, file)
                        modify_orcainp_xyz(file_path, functional, base)

if __name__ == "__main__":
    directory = sys.argv[1]
    functionals = ["B3LYP", "PBE", "TPSS"]
    bases = ["STO-3G", "6-311+G**", "def2-TZVP"]
    
    process_directory(directory, functionals, bases)
