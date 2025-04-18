import argparse
from sidtools import s_make, s_run, s_store

def s_make_main(args=None):
    parser = argparse.ArgumentParser(
        description="Split an .xyz or .db file into trajectories and organize them into folders."
    )
    parser.add_argument("-T", "--trajectory", required=True, help="Path to the input .xyz or .db file.")
    parser.add_argument("--base", required=True, help="Name of the base directory to create.")
    parser.add_argument(
        "-F", "--files", nargs="*", default=["01_submit.py", "script.sh", "src"],
        help="List of files or folders to copy into each trajectory folder."
    )
    parsed = parser.parse_args(args)
    s_make.split_trajectories_and_setup_directories(parsed.trajectory, parsed.base, parsed.files)

def s_run_main(args=None):
    parser = argparse.ArgumentParser(
        description="Run 'sbatch script.sh' in all directories containing script.sh."
    )
    parser.add_argument("--base", required=True, help="Path to the base directory.")
    parsed = parser.parse_args(args)
    s_run.run_sbatch_in_all_directories(parsed.base)

# def s_store_main(args=None):
#     parser = argparse.ArgumentParser(
#         description="Store VASP output from trajectory folders into an ASE .db file."
#     )
#     parser.add_argument("--base", required=True, help="Base directory containing trajectory folders.")
#     parser.add_argument("--db", required=True, help="Output .db file name.")
#     parser.add_argument("--subfolder", default="opt_PBE_400_111", help="Subfolder name. Default: opt_PBE_400_111")
#     parser.add_argument("--file", default="vasprun.xml", help="VASP output file. Default: vasprun.xml")
#     parsed = parser.parse_args(args)
#     s_store.store_to_db(parsed.base, parsed.db, parsed.subfolder, parsed.file)

# def s_store_main():
#     parser = argparse.ArgumentParser(
#         description="Store VASP output from trajectory folders into an ASE .db file."
#     )
#     parser.add_argument("--base", required=True, help="Base directory containing trajectory folders.")
#     parser.add_argument("--db", required=True, help="Output .db file name.")
#     parser.add_argument("--subfolder", default="opt_PBE_400_111", help="Subfolder in each trajectory dir. Default: opt_PBE_400_111")
#     parser.add_argument("--file", default="vasprun.xml", help="VASP output file name. Default: vasprun.xml")
#     parser.add_argument(
#         "--extra", nargs="*", default=[],
#         help="Extra data fields to store in the ASE DB. Supports key=value pairs or dynamic tags like num_Rh"
#     )

#     args = parser.parse_args()
#     s_store.store_to_db(args.base, args.db, args.subfolder, args.file, args.extra)

def s_store_main():
    parser = argparse.ArgumentParser(
        description="Store VASP output from trajectory folders into an ASE .db file."
    )
    parser.add_argument("--base", required=True, help="Base directory containing trajectory folders.")
    parser.add_argument("--db", required=True, help="Output .db file name.")
    parser.add_argument(
        "--type", default="opt", choices=["opt", "md"],
        help="DFT type: 'opt' for optimized structures, 'md' for molecular dynamics. Default: opt"
    )
    parser.add_argument("--subfolder", default=None, help="Optional subfolder override. Auto-set based on type if not provided.")
    parser.add_argument("--file", default="vasprun.xml", help="VASP output file name. Default: vasprun.xml")

    args = parser.parse_args()

    # Determine subfolder based on type if not explicitly provided
    subfolder = args.subfolder
    if subfolder is None:
        if args.type == "md":
            subfolder = "md_PBE_400_111"
        else:
            subfolder = "opt_PBE_400_111"

    s_store.store_to_db(base_folder=args.base, db_name=args.db, DFT_type=args.type,
                        subfolder=subfolder, filename=args.file)


def main():
    parser = argparse.ArgumentParser(description="Command-line interface for sidtools.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("s_make", help="Split trajectories and organize folders.").set_defaults(func=s_make_main)
    subparsers.add_parser("s_run", help="Run sbatch in subdirectories.").set_defaults(func=s_run_main)
    subparsers.add_parser("s_store", help="Store VASP outputs into an ASE .db").set_defaults(func=s_store_main)

    args, unknown = parser.parse_known_args()
    args.func(unknown)

if __name__ == "__main__":
    main()
