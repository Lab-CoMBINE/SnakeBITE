import os
from shiny import ui
import subprocess
import ruamel.yaml
from ui_utils import wrnmodal

yaml = ruamel.yaml.YAML()

def tool_vec_create(*args):
    vec_len = len(args) // 2
    vec_value = args[:vec_len]
    vec_flag = args[vec_len:]
    if len(vec_value) != len(vec_flag):
        return print("Inserted vectors not lenght-corresponding")
    else:
        vec_tool = [""] * vec_len
        for i in range(vec_len):
            if vec_value[i] != "None":
                vec_tool[i] = vec_flag[i] + vec_value[i]
            else:
                vec_tool[i] = ""
        return vec_tool

def updconfadv(op, defa, data, key_param, up_param):
     if op == True and defa == False:
          data[key_param]["adv"] = up_param

def bool_updconf(op, defa, par_tool, data, name_tool):
     if op == True and defa == False:
          updict(par_tool, data, name_tool)

def updconf(tool, op, defa, par_tool, data, name_tool):
    if tool in op and defa == False:
            updict(par_tool, data, name_tool)

def updconfvariant(tool, defa, par_tool, data, name_tool):
     if tool == True and defa == False:
        updict(par_tool, data, name_tool)

def updict(dctnr, data, param):
    for key, value in dctnr.items():
                if key in data.get(str(param), {}):
                    data[param][key] = value #as an alternative, can use str(value)

def explore_ssh_server(host, port, username, password):
    filexpl_dir = os.path.dirname(os.path.abspath(__file__))
    filexpl_path = os.path.join(filexpl_dir, 'filexplorer_ssh.py')
    process = subprocess.Popen(["python", filexpl_path, host, port, username, password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return stdout.decode().strip()
    else:
        print("Error during SSH server exploration:")
        print(stderr.decode().strip())
        return None

def warnfill(tabswitch, platform, pipeline, reference, refhg19, refhg38):
        if tabswitch != "Start": 
            if platform == "" or pipeline == "" or reference  == "":
                wrnmodal("You need to select a value for each field before proceeding to pipeline settings","WARNING")
            elif reference == "GRCh37/hg19" and str(refhg19.get()) == "None":
                wrnmodal("Please specify the selected reference genome file","WARNING")
            elif reference == "GRCh38/hg38" and str(refhg38.get()) == "None":
                wrnmodal("Please specify the selected reference genome file","WARNING")

def reset_sambam_minmap(dor, aln, sam):
        if dor == 1:
            ui.update_checkbox("SAMBAM", value = False)
        if aln == 1:
            ui.update_checkbox("SAMBAM", value = False)
        if sam == 1:
            ui.update_checkbox("ALNANO", value = False)
        if sam == 1 and aln == 1:
            ui.notification_show("Minimap2 already outputs reads in BAM format!", type = "default", duration=1200)
        if sam == 1 and dor == 1:
            ui.update_checkbox("ALNANO", value = True)
            ui.notification_show("Checked Minimap2 to obtain aligned reads in BAM format.", type = "default", duration=1200)

def reset_annosev(ann, svn, snvn):
        if ann == 1:
            if len(svn) > 0 or len(snvn) > 0:
                ui.update_checkbox_group("ONLYANNANO", selected="")
        elif ann == 0:
            ui.update_checkbox_group("ONLYANNANO", selected="")

def nodb_tool(onlann):
        if len(onlann) > 1:
            ui.update_checkbox_group("ONLYANNANO", selected="")
            ui.notification_show("Choose only one tool depending on the Variant type (SV or SNV)", type = "default", duration=1200)

def conn_ssh(ip, usr,btt):
        m = ui.modal(  
            ui.input_text("ssh", "IP:", value=ip.get()),
            ui.input_text("user", "Username:", value=usr.get()),
            ui.input_password("password", "Password:"),
            ui.input_action_button(str(btt.get()), "Connect"),
            title="Server Credentials",  
            easy_close=True,  
            footer=None,  
        )  
        ui.modal_show(m)
        btt.set(None)

def tool_dtpt(ssh, usr, psswrd, save_ip, save_usr, dtpt, dtpt_txt, data, config):
    ui.modal_remove()
    path = explore_ssh_server(ssh, "22", usr, psswrd)
    if str(path) != "None":
        save_ip.set(ssh)
        save_usr.set(usr)
    dtpt.set(path)
    data["tool_usage"][dtpt_txt] = dtpt.get()
    with open(config, 'wb') as f:
        yaml.dump(data, f)
    return

def ref_dtpt(ssh, usr, psswrd, save_ip, save_usr, dtpt, dtpt_txt, data, config):
    ui.modal_remove()
    path = explore_ssh_server(ssh, "22", usr, psswrd)
    if str(path) != "None":
        save_ip.set(ssh)
        save_usr.set(usr)
    dtpt.set(path)
    data[dtpt_txt] = dtpt.get()
    with open(config, 'wb') as f:
        yaml.dump(data, f)
    return

def dtpt(ssh, usr, psswrd, save_ip, save_usr, old_path):
    ui.modal_remove()
    path = explore_ssh_server(ssh, "22", usr, psswrd)
    if str(path) != "None":
        save_ip.set(ssh)
        save_usr.set(usr)
    old_path.set(path)
    return

def text_dtpt(path, warn):
        if str(path.get()) == "None":
            return warn
        else:
            return str(path.get())

def check_ext_folder(folder, ext):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext): 
                return True
        for sub_dir in dirs:
            if check_ext_folder(os.path.join(root, sub_dir), ext):
                return True
    return False

#def check_ext_folder(folder, ext):
#    for root, dirs, files in os.walk(folder):
#         for file in files:
#              if file.endswith(ext): 
#                   return True
#    return False