"""
This script is for inline use ONLY !!!
"""
# built in lib
import os
import sys

# custom lib
from .tools import profiler
from .lib_prof import export_stats


entrypoint = sys.argv[1] # script name
if not entrypoint.endswith('.py') and not ("-h" in sys.argv or "-V" in sys.argv) :
    print("Please Check the command format by - lprof_ext -h\nUsually wrong command format:\n\n      lprof_ext <*.py> [args]\n\n")
    # print("Error: Please provide a valid .py file.")
    sys.exit(1)
entrypoint = os.path.join('./', os.path.relpath(entrypoint))


def export_profiler(output_path:str = None):
    if output_path is None:
        output_path = lprofext_json_outpath # builtins obj, init in cli.py
    lstats = profiler.get_stats()
    # profiler.dump_stats(lprof_pkl)
    # lstats = load_stats(lprof_pkl)
    export_stats(lstats.timings, entrypoint, json_dst=output_path)
    print(f"[INFO] - JSON stats saved to `{output_path}`")
