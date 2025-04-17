import os
import inspect
import json
# import pickle
from collections import defaultdict

from .tools import profile_decorator

"""
This File is used to transform the lstats from `line_profiler::LineProfiler.get_stats().timings`
into lprof_ext.json format for GUI Visualising.
"""

stat_dict_template = defaultdict(lambda: #file_name :
                    defaultdict(lambda:  { # func_name
                        "line": defaultdict(
                            lambda: {}
                        ),
                        # "total_hit": 0,
                        "total_time": 0
                    }))


def transform(stats:dict):
    """
    count the number of functions before the line
    and add n to the line number.

    stats_dict
    {
        <file_name> :
            <func_name> :
                "line":{
                    <line_no> : dict w/o type
                },
                # "total_hit": int,
                "total_time": int,
        entrypoint: str
    }
    """
    stats_dict = stat_dict_template.copy()

    for (file_name, first_line, func_name), line_stats in stats.items():
        if line_stats:
            for line in line_stats:
                line_no, count, totaltime = line
                stats_dict[file_name][func_name]["line"][line_no]['count'] = count
                stats_dict[file_name][func_name]["line"][line_no]['time'] = totaltime
    return stats_dict

# def load_stats(filename):
#     """ Utility function to load a pickled LineStats object from a given
#     filename.
#     """
#     with open(filename, 'rb') as f:
#         return pickle.load(f)

def get_func_sublines(script, index):
    """
    get the func code block.
    return: distance from `first_line` to `def `
    """
    func_sublines = []
    # Collect lines starting from @deco
    for dist in range(20):
        # print(script[index + i].rstrip())
        line = script[index + dist].strip()
        if not line:  # Skip empty lines
            continue
        if line.startswith("def "):
            # Use inspect.getblock to get the function body
            block = inspect.getblock(script[index + dist:])
            func_sublines.extend(block)  # Skip the def line since we already added it
            break
    return dist, func_sublines

def number_of_profiles(script, index):
    """
    Get the number of profiles from a given script before line `index`.
    """
    line_strip = [line.strip() for line in script[:index]]
    return line_strip.count("@lprofile_ext")


def export_stats(stats, entry_script:str, json_dst = "lprof_ext.json"):
    """
    modified from line_profiler.line_profiler.show_text
    note: line_profiler==4.2.0
    """

    # transform stats into new dict
    stats_order = sorted(stats.items())
    stats_dict = transform(stats)
    scripts = profile_decorator.modified_code
    # with open("script.json", 'w') as f:
    #     json.dump(profile_decorator.modified_code, f, indent=4)
    clean_dict = stat_dict_template.copy()

    for (file_name, start_lineno, func_name), v in stats_order:
        if v:
            all_lines = [ x + "\n" for x in scripts[file_name].split("\n")]
            dist, func_sublines = get_func_sublines(all_lines, start_lineno)

            numprof = number_of_profiles(all_lines, start_lineno)

            # Calculate total func hit and time
            # total_hit = sum([x['count']for x in stats_dict[file_name][func_name]["line"].values()])
            total_time = sum([x.get('time',0)for x in stats_dict[file_name][func_name]["line"].values()])
            # stats_dict[file_name][func_name]['total_hit'] = total_hit
            stats_dict[file_name][func_name]['total_time'] = total_time

            for n, line in enumerate(func_sublines):
                run_line_no = start_lineno + dist + n + 1
                show_line_no = run_line_no - numprof # align with the line number in the source code and exec code
                # print(run_line_no, numprof, show_line_no, line)
                # print(stats_dict[file_name][func_name]["line"][run_line_no].items())
                for k,v in stats_dict[file_name][func_name]["line"][run_line_no].items():
                    clean_dict[file_name][func_name]["line"][show_line_no][k] = v
                clean_dict[file_name][func_name]["line"][show_line_no]["code"] = line.split("\n")[0]
                # clean_dict[file_name][func_name]['total_hit'] = stats_dict[file_name][func_name]['total_hit']
                clean_dict[file_name][func_name]['total_time'] = stats_dict[file_name][func_name]['total_time']
                # clean_dict[file_name][func_name]["func_time"] = func_time

    for file_name, func_profile in clean_dict.items():
        for func_name, func_dict in func_profile.items():
            line_stats = func_dict["line"]
            for line_no, stats_dict_ in sorted(line_stats.items()):
                count = stats_dict_.get('count', "")
                time = stats_dict_.get('time', "")
                pct_time =  round(time/clean_dict[file_name][func_name]["total_time"]*100,1) if count else ""
                clean_dict[file_name][func_name]["line"][line_no]["pct_time"] = pct_time

    # remove parent dir, from abs to relative path
    rename_dict = {old_file_path: old_file_path.replace(f"{os.getcwd()}", ".")  \
                    for old_file_path in clean_dict.keys()}                          # w/  "./"
    # rename_dict = {old_file_path : os.path.relpath(old_file_path) \
    #                for old_file_path in clean_dict.keys()}                         # w/o  "./"
    for old_file_path, new_file_path in rename_dict.items():
        clean_dict[new_file_path] = clean_dict.pop(old_file_path)

    clean_dict["entrypoint"] = entry_script.replace(f"{os.getcwd()}", ".")

    # dump json for GUI
    with open(json_dst, "w") as f:
        json.dump(clean_dict, f, indent=4)