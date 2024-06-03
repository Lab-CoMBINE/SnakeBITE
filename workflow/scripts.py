import re
import os

def only_flag(param):
    parts = param.split()
    flag = parts[0] if len(parts) > 1 and parts[1] == 'True' else ""
    return flag

def empty_flag(param):
    parts = param.split(maxsplit=1)
    if len(parts) == 2 and parts[1].strip():
        return param
    else:
        return ""

def ext_to_folder(file):
    if file.endswith('.pod5'):
        dir_path = os.path.dirname(file)
        return dir_path

def paralelization_func(threads_num, config_file):
    if threads_num == 1:
        return 1
    else:
        if int(config_file["paral_ops"]) == 0:
            return int(config_file["threads"])
        else:
            return int(config_file["paral_threads"])/int(config_file["paral_ops"])

def hg_to_GRCh(hg):
    if hg == "hg37":
        return "GRCh37"
    else:
        return "GRCh38"