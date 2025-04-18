import os
import argparse
import numpy as np
from ase.io import read
from ase.db import connect

def store_to_db(base_folder, db_name, subfolder, filename, DFT_type):
    db = connect(db_name)

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
            if DFT_type == "opt":
                atoms = read(file_path, format='vasp-xml', index=-1)
                data = {
                    "energy": atoms.get_potential_energy(),
                    "forces": atoms.get_forces().tolist(),
                    "coordinates": atoms.get_positions().tolist(),
                    "type": "opt"
                }
                db.write(atoms, data=data)
                print(f"Written opt frame from: {file_path}")

            elif DFT_type == "md":
                vasprun_list = read(file_path, format='vasp-xml', index=':')
                frames = len(vasprun_list)

                for i, frame in enumerate(vasprun_list):
                    data = {
                        "energy": frame.get_potential_energy(),
                        "forces": frame.get_forces().tolist(),
                        "coordinates": frame.get_positions().tolist(),
                        "type": "md",
                        "frame": i
                    }
                    db.write(frame, data=data)

                print(f"Written {frames} MD frames from: {file_path}")

            else:
                print(f"Unknown DFT_type '{DFT_type}', skipping {file_path}.")
                continue

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    print(f"All {DFT_type.upper()} structures stored in {db_name}")


def main():
    parser = argparse.ArgumentParser(description="Store structures from vasprun.xml into an ASE DB.")
    parser.add_argument("--base", required=True, help="Base folder containing trajectory_* directories")
    parser.add_argument("--db", required=True, help="Name of the output .db file")
    parser.add_argument("--filename", default="vasprun.xml", help="Filename to read")
    parser.add_argument("--type", default="opt", choices=["opt", "md"], help="DFT calculation type: 'opt' or 'md'")
    parser.add_argument("--subfolder", help="Subfolder inside trajectory folders (auto-set by DFT type if not given)")

    args = parser.parse_args()

    # Auto-set subfolder if not provided
    if not args.subfolder:
        args.subfolder = "md_PBE_400_111" if args.type == "md" else "opt_PBE_400_111"

    store_to_db(args.base, args.db, args.subfolder, args.filename, args.type)

if __name__ == "__main__":
    main()
