import re
import os

def only_flag(param):
    parts = param.split()
    flag = parts[0] if len(parts) > 1 and parts[1] == 'True' else ""
    return flag

def ext_to_folder(file):
    if file.endswith('.pod5'):
        dir_path = os.path.dirname(file)
        return dir_path

def paralelization_func(threads_num):
    if threads_num == 1:
        return 1
    else:
        if int(config["paral_ops"]) == 0:
            return int(config["threads"])
        else:
            return int(config["paral_threads"])/int(config["paral_ops"])

def hg_to_GRCh(hg):
    if hg == "hg37":
        return "GRCh37"
    else:
        return "GRCh38"