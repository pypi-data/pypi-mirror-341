import os
import argparse
from ase.io import read
from ase.db import connect
import re

def parse_extra_args(extra_args):
    """
    Parses extra key-value pairs passed via command line.
    Also detects dynamic keys like num_X for atom counting.
    """
    static_data = {}
    dynamic_keys = []

    for item in extra_args:
        if re.fullmatch(r"num_[A-Z][a-z]?", item):  # e.g., num_Rh, num_O
            dynamic_keys.append(item)
        elif "=" in item:
            key, value = item.split("=", 1)
            static_data[key] = value
        else:
            print(f"Warning: Unrecognized extra format '{item}', skipping.")

    return static_data, dynamic_keys


def store_to_db(base_folder, db_name, subfolder="opt_PBE_400_111", filename="vasprun.xml", extra_args=[]):
    """
    Collects structures from multiple trajectory folders and stores them in an ASE database.
    Supports dynamic extra keys like 'num_Rh' to count atoms.
    """
    db = connect(db_name)
    static_data, dynamic_keys = parse_extra_args(extra_args)

    # Detect trajectory folders like trajectory_1, trajectory_2, ...
    trajectory_dirs = sorted([
        d for d in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, d)) and d.startswith("trajectory_")
    ], key=lambda x: int(x.split("_")[-1]))

    for folder in trajectory_dirs:
        traj_dir = os.path.join(base_folder, folder, subfolder)
        file_path = os.path.join(traj_dir, filename)

        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found. Skipping.")
            continue

        try:
            atoms = read(file_path, format='vasp-xml', index=-1)
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()
            coordinates = atoms.get_positions()

            data = {
                "energy": energy,
                "forces": forces,
                "coordinates": coordinates,
                **static_data
            }

            # Handle dynamic keys like num_Rh, num_O, etc.
            for key in dynamic_keys:
                match = re.fullmatch(r"num_([A-Z][a-z]?)", key)
                if match:
                    symbol = match.group(1)
                    data[key] = sum(1 for atom in atoms if atom.symbol == symbol)

            db.write(atoms, data=data)
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
    parser.add_argument("--extra", nargs="*", default=[], help="Additional key=value pairs or dynamic tags like num_Rh")

    args = parser.parse_args()
    store_to_db(args.base, args.db, args.subfolder, args.filename, args.extra)

if __name__ == "__main__":
    main()
