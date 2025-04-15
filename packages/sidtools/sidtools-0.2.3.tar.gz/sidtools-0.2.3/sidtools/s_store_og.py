import os
import argparse
from ase.io import read
from ase.db import connect

def store_to_db(base_folder, db_name, subfolder="opt_PBE_400_111", filename="vasprun.xml"):
    """
    Collects structures from multiple trajectory folders and stores them in an ASE database.

    Parameters:
    - base_folder: str, path to the folder containing trajectory_*/subfolder/vasprun.xml
    - db_name: str, name of the output ASE database file.
    - subfolder: str, subdirectory inside each trajectory folder where vasprun.xml exists.
    - filename: str, name of the VASP output file to read structures from.
    """
    db = connect(db_name)

    # Dynamically detect folders like trajectory_1, trajectory_2, ...
    trajectory_dirs = sorted([
        d for d in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, d)) and d.startswith("trajectory_")
    ], key=lambda x: int(x.split("_")[-1]))  # Sort numerically by index

    for folder in trajectory_dirs:
        traj_dir = os.path.join(base_folder, folder, subfolder)
        file_path = os.path.join(traj_dir, filename)

        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found. Skipping.")
            continue

        try:
            atoms = read(file_path, format='vasp-xml', index=-1)  # Last structure only
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()
            coordinates = atoms.get_positions()
            db.write(atoms, data={"energy": energy, "forces": forces, "coordinates": coordinates})
            print(f"Written: {file_path}")
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    print(f"All optimized structures stored in {db_name}")


def main():
    parser = argparse.ArgumentParser(description="Store optimized structures from vasprun.xml into an ASE DB.")
    parser.add_argument("--base", required=True, help="Base folder containing trajectory_* directories")
    parser.add_argument("--db", required=True, help="Name of the output .db file")
    parser.add_argument("--subfolder", default="opt_PBE_400_111", help="Subfolder inside trajectory folders (default: opt_PBE_400_111)")
    parser.add_argument("--filename", default="vasprun.xml", help="Filename to read (default: vasprun.xml)")
    
    args = parser.parse_args()
    store_to_db(args.base, args.db, args.subfolder, args.filename)

if __name__ == "__main__":
    main()

