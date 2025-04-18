import argparse
import os
from sidtools import s_make, s_run, s_store

def s_make_main():
    parser = argparse.ArgumentParser(
        description="Split an .xyz or .db file into trajectories and organize them into folders."
    )
    parser.add_argument("-T", "--trajectory", required=True, help="Path to the input .xyz or .db file.")
    parser.add_argument("--base", required=True, help="Name of the base directory to create.")
    parser.add_argument(
        "-F", "--files", nargs="*", default=["01_submit.py", "script.sh", "src"],
        help="List of files or folders to copy into each trajectory folder. Defaults to ['01_submit.py', 'script.sh', 'src']."  
    )
    
    args = parser.parse_args()
    
    # Call the main functionality of s_make
    s_make.split_trajectories_and_setup_directories(args.trajectory, args.base, args.files)

def s_run_main():
    parser = argparse.ArgumentParser(
        description="Run 'sbatch script.sh' in all directories containing script.sh."
    )
    parser.add_argument(
        "--base", required=True, help="Path to the base directory where subdirectories contain script.sh files."
    )
    
    args = parser.parse_args()

    # Call the main functionality of s_run
    s_run.run_sbatch_in_all_directories(args.base)

def s_store_main():
    parser = argparse.ArgumentParser(
        description="Store VASP output from trajectory folders into an ASE .db file."
    )
    parser.add_argument("--base", required=True, help="Base directory containing trajectory folders.")
    parser.add_argument("--db", required=True, help="Output .db file name.")
    parser.add_argument("--subfolder", default="opt_PBE_400_111", help="Subfolder in each trajectory dir. Default: opt_PBE_400_111")
    parser.add_argument("--file", default="vasprun.xml", help="VASP output file name. Default: vasprun.xml")

    args = parser.parse_args()
    s_store.store_to_db(args.base, args.db, args.subfolder, args.file)



def main():
    parser = argparse.ArgumentParser(
        description="Command-line interface for sidtools utilities."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # s_make command
    s_make_parser = subparsers.add_parser('s_make', help="Split .xyz or .db file into trajectories and organize them into folders.")
    s_make_parser.add_argument("-T", "--trajectory", required=True, help="Path to the input .xyz or .db file.")
    s_make_parser.add_argument("--base", required=True, help="Name of the base directory to create.")
    s_make_parser.add_argument(
        "-F", "--files", nargs="*", default=["01_submit.py", "script.sh", "src"],
        help="List of files or folders to copy into each trajectory folder."
    )
    s_make_parser.set_defaults(func=s_make_main)

    # s_run command
    s_run_parser = subparsers.add_parser('s_run', help="Run 'sbatch script.sh' in all directories containing script.sh.")
    s_run_parser.add_argument("--base", required=True, help="Path to the base directory where subdirectories contain script.sh files.")
    s_run_parser.set_defaults(func=s_run_main)


    # s_store command
    s_store_parser = subparsers.add_parser('s_store', help="Store VASP outputs into an ASE .db")
    s_store_parser.add_argument("--base", required=True, help="Base directory containing trajectory folders.")
    s_store_parser.add_argument("--db", required=True, help="Output .db file name.")
    s_store_parser.add_argument("--subfolder", default="opt_PBE_400_111", help="Subfolder name. Default: opt_PBE_400_111")
    s_store_parser.add_argument("--file", default="vasprun.xml", help="VASP output file. Default: vasprun.xml")
    s_store_parser.set_defaults(func=s_store_main)

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "s_make":
        s_make_main()
    elif args.command == "s_run":
        s_run_main()
    elif args.command == "s_store":
        s_store_main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
