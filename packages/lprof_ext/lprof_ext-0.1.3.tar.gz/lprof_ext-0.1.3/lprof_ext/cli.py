# lprof_ext/cli.py
import sys
import os
import argparse
from pathlib import Path
import builtins

# custom lib
from . import __version__
from .flow import profiling_flow

def main():
    usage_msg = '''

Whole script:
    lprof_ext <file_to_run.py> [-o, ./prof.json]

Inline:
    lprof_ext <file_to_run.py> [-o, ./prof.json] [--snap]
'''
    parser = argparse.ArgumentParser(
        # description="Profile Python scripts by adding decorators and collecting performance stats",
        description="---------------------------------------",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage = usage_msg
    )
    parser.add_argument(
        "entrypoint",
        type=str,
        help="Entrypoint to run script."
    )

    parser.add_argument(
        '--snap',
        action="store_true",
        help="Snapshots the profile every `export_profiler()` called."
    )

    parser.add_argument(
        '-o',
        # '--output',
        dest='out_path',
        default='.lprofile/lprof_ext.json',
        help='Output path for the JSON profile stats [default: %(default)s]'
    )

    parser.add_argument(
        "-V",
        action="version",
        version=f"{__version__}",
    )

    if not Path('.lprofile').exists():
        os.makedirs('.lprofile')

    args = parser.parse_args()
    output_path:str = args.out_path # use for 1. flow::export_stats , 2. exporter::export_profiler
    # set it to builtins , avoid cyclic imports loop
    builtins.lprofext_json_outpath = output_path # used in exporter.py::export_profiler
    
    # Validate input
    input_path = Path(args.entrypoint).resolve()
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)

    if not input_path.is_file() or input_path.suffix != '.py':
        print("Error: Please provide a valid .py file.")
        sys.exit(1)

    
    entrypoint: str = str(input_path)

    try:
        profiling_flow(entrypoint, output_path, args.snap)

    except Exception as e:
        print(f"Error during profiling: {e}")
        raise e



if __name__ == "__main__":
    main()