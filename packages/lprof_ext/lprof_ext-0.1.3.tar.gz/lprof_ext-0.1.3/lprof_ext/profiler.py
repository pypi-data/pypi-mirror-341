# lprof_ext/profiler.py
# built-in libraries
import os
import sys
from pathlib import Path
import builtins

# custom libraries
from .tools import profile_decorator, profiler
from .exporter import export_profiler

# Initialize profiler
builtins.lprofile_ext = profiler
builtins.export_profiler = export_profiler

"""
functions for profiling. call in flow.
"""

def find_script(script_name):
    """ Find the script.

    If the input is not a file, then $PATH will be searched.
    """
    if os.path.isfile(script_name):
        return script_name
    path = os.getenv('PATH', os.defpath).split(os.pathsep)
    for dir in path:
        if dir == '':
            continue
        filename = os.path.join(dir, script_name)
        if os.path.isfile(filename):
            return filename

    sys.stderr.write('Could not find script %s\n' % script_name)
    raise SystemExit(1)


def check_source_code(content: str) -> bool:
    """Check if source code already contains @lprofile_ext decorator."""
    content = [line.strip() for line in content.splitlines()]
    if "@lprofile_ext" in content:
        return False
    return True

def isolate_import_lines(entryscript:str):
    """
    extracts the `import` lines from script and comments them out.
    """
    lines = entryscript.split("\n")
    import_lines = []
    for idx, line in enumerate(lines):
        if "import" in line:
            import_lines.append(line)
            lines[idx] = "# " + line
    script = '\n'.join(lines)
    import_lines = "\n".join(import_lines)
    return import_lines, script

def add_decorator(script_path: str, source_code = '') -> bool:
    """
    add @lprofile_ext decorators
    reference to lineprofiler:v4.2.0 :: process_script() first half 
    """
    script_file = find_script(script_path)
    try:
        if source_code:
            source = source_code
        else:
            with open(script_path, "r") as f:
                source = f.read()

        if not check_source_code(source):
            print(f"Skipping {script_path} due to existing @lprofile_ext decorator.")
            return False

        # Parse and modify CST
        modified_code = profile_decorator.get_modified_code(source)
        profile_decorator.set_modified_code(script_file, modified_code)
        return modified_code

    except Exception as e:
        print(f"Error processing {script_path}: {str(e)}")
        raise e

def find_python_scripts(project_dir: str): # -> list[str]:
    """Find all .py files in project directory, excluding .venv/."""
    project_path = Path(project_dir).resolve()
    python_files = []
    for py_file in project_path.rglob("*.py"):
        if ".venv" not in str(py_file.relative_to(project_path)).split(os.sep):
            python_files.append(str(py_file))
    return python_files

def remove_caches(project_dir: str):
    """Remove profiling cache files (.lprof, snapshot.temp.json)."""
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith((".lprof", ".lprofe", "snapshot.temp.json")):
                os.remove(os.path.join(root, file))