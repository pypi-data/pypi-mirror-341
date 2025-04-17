import os
import sys

# custom lib
from .profiler import find_python_scripts, add_decorator , isolate_import_lines
from .tools import profiler
from .lib_prof import export_stats #, load_stats


def profiling_flow(main_script: str, output_path: str, snapshot:bool = False):
    # Find scripts
    project_dir = os.getcwd()
    sys.path.append(project_dir) # for importing custom lib

    scripts = find_python_scripts(project_dir)
    if not scripts:
        print(f"[ERROR] - No Python scripts found in {project_dir}.")
        sys.exit(1)

    """
    steps:
    [Pre] - deco add scripts 
    [Pre] - Split the entry script into two parts: 
        - import lines
        - remain lines
    1. exec entryscript import lib lines
        usage: import the lib called
    2. exec non-entry script with deco.
        usage: overwrite the func in 1. 
    3. Run the entry script with deco.
    """
    isolate_import_lines


    # Process non-entry scripts
    non_entry_scripts = {}
    for script_path in scripts:
        deco_script = add_decorator(script_path)
        if script_path != main_script:
            non_entry_scripts[script_path] = deco_script
        else:
            import_lines, entryscript = isolate_import_lines(deco_script)

    # 1. exec entryscript import lib lines
    print(f"[INFO] - loading lib from {main_script}...")
    local_vars = {}
    exec(compile(import_lines, "entryscript import lines", "exec"), local_vars, local_vars)

    # 2. exec non-entry scripts with deco.
    for script_path, deco_script in non_entry_scripts.items():
        print(f"[INFO] - loading {script_path}...")
        exec(compile(deco_script, script_path, "exec"), local_vars, local_vars)

    # 3. Run the entry script with deco.
    print("[INFO] - Running the entry script...")
    # main_script = os.path.relpath(main_script) # rel path
    local_vars["__file__"] = entryscript
    local_vars["__name__"] = "__main__"
    exec(compile(entryscript, main_script, "exec"), local_vars, local_vars)

    if snapshot:
        return
    print(f"[INFO] - Dumping profile stats to JSON")
    lstats = profiler.get_stats()
    # profiler.print_stats()
    # profiler.dump_stats("lprof_pkl")
    # lstats = load_stats("lprof_pkl")
    export_stats(lstats.timings, main_script, json_dst=output_path)
    print(f"[INFO] - JSON stats saved to `{output_path}`")
    print("""
-------------------- [FINISH] --------------------
Run the following command to view the profile stats in GUI:

> docker run --rm -d --name prof_gui \
             -v $PWD/.lprofile/lprof_ext.json:/lprof_ext.json \
             -p 8080:8080 ruprof/prof_gui:rust

> http://0.0.0.0:8080/
""")