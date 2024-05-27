import os
import subprocess
import ruamel.yaml
from collections import OrderedDict
import re
from ui_utils import wrnmodal
from server_utils import tool_vec_create, bool_updconf, updconf, updconfadv, updconfvariant, check_ext_folder
from compiler import nangenline_compiler

yaml = ruamel.yaml.YAML()

def launch_gonangen(data, workdir, in_path, threads_num, sampsize, ref, hg19_path, hg38_path, svnano, snvnano,
                    up_mul_file, mulcst_name_check, mulcst_name, singcst_name_check, singcst_name,
                    DORADO, ALNANO, SAMBAM, SRTBAM, IDXBAM, ANNANO, ONLYANNANO, SVNANO, SNVNANO, 
                    def_dorado, def_alnano, def_sambam, def_srtbam, def_idxbam, def_svim, def_snif, def_cut, def_gas, def_long, def_nanoc, def_cla3, def_deep, def_ann, def_vep,
                    alnano_advp, sambam_advp, srtbam_advp, idxbam_advp,
                    dorado_model, dorado_device, dorado_modifiedbases, dorado_advp,
                    svim_minmapq, svim_minsvsize, svim_maxsvsize, svim_skipgenotyping, svim_minimumscore, svim_minimumdepth, svim_advp,
                    snif_phase, snif_minsupport, snif_minsvlen, snif_mapq, snif_noqc, snif_advp,
                    cut_minmapq, cut_minreadlen, cut_minsupport, cut_minsize, cut_maxsize, cut_genotype, cut_advp,
                    gas_som_check, gas_som_path, gas_bed_path, gas_pars_Q, gas_germ_NS, gas_germ_Q, gas_germ_MS, gas_germ_OT, gas_germ_vcf_TS, gas_germ_vcf_TC, gas_germ_vcf_TI, gas_germ_vcf_TO, 
                    gas_som_NS, gas_som_Q, gas_som_MS, gas_som_OV, gas_som_vcf_TS, gas_som_vcf_TC, gas_som_vcf_TI, gas_som_vcf_TO, gas_som_vcf_TR, gas_som_vcf_TP, gas_som_vcf_TH,
                    long_region, long_mincov, long_maxcov, long_minmapq, long_minaltcount, long_minaltfrac, long_advp,
                    nanoc_mode, nanoc_mincov, nanoc_maxcov, nanoc_bed_path, nanoc_phase, nanoc_advp,
                    cla3_callsnponly, clair3_mod_path, clair3_bed_path, cla3_qual, cla3_snpminaf, cla3_indelminaf, cla3_minmq, cla3_advp,
                    deep_region, deep_pepperminmapq, deep_pepperminsnpbaseq, deep_pepperminindelbaseq, deep_peppersnpfrequency, deep_pepperinsertfrequency, deep_pepperdeletefrequency, 
                    deep_pepperskipindels, deep_dvminmappingquality, deep_dvminbasequality, deep_advp,
                    ann_svinputinfo, ann_annotationmode, ann_tx, ann_svminsize, ann_advp,
                    vep_cache, vep_dircache, vep_everything, vep_codingonly, vep_nointergenic, vep_offline, vep_advp,
                    ):
        w_dir = str(workdir())
        in_filepath = str(in_path())
        op_seq = []
        frst_op = None
        #NOT-LAUNCH-READY CONDITIONS WARNINGS
        if ref == "GRCh37/hg19" and str(hg19_path.get()) == "None":
            wrnmodal("Please specify the selected reference genome file","WARNING")
        elif ref == "GRCh38/hg38" and str(hg38_path.get()) == "None":
                wrnmodal("Please specify the selected reference genome file","WARNING")
        elif not(DORADO) and not(ALNANO) and not(SAMBAM) and not(SRTBAM) and not(IDXBAM) and not(ANNANO) and len(SVNANO) == 0 and len(SNVNANO) == 0: #and not(input.MULINP())
            wrnmodal("You need to select at least one operation to launch your pipeline", "WARNING")
        elif ANNANO and (len(ONLYANNANO) == 0 and (not(DORADO) and not(ALNANO) and not(SAMBAM) and not(SRTBAM) and not(IDXBAM) and len(SVNANO) == 0 and len(SNVNANO) == 0)): #and not(input.MULINP())
            wrnmodal("For annotation operation only, please select the right annotation tool for your variants", "WARNING")
        elif ANNANO and (DORADO or ALNANO or SAMBAM or SRTBAM or IDXBAM) and (len(SVNANO) == 0 and len(SNVNANO) == 0): #or input.MULINP()
            wrnmodal("Please select at least a Variant Caller Tool in the pipeline to proceed to Variant annotation", "WARNING")
        elif ANNANO and len(ONLYANNANO) != 0 and not (in_filepath.endswith(".vcf") or in_filepath.endswith(".vcf.gz")):
            wrnmodal("For annotation operation only, please use a .vcf or .vcf.gz file", "WARNING")
        else:
            if "Clair3" in SNVNANO and (str(clair3_mod_path()) == "None" or str(clair3_mod_path()) == ""):
                wrnmodal("When selecting Clair3, you need to specify the model path in Pipeline Customization", "WARNING")
            elif "Gasoline" in SVNANO and gas_som_check == 1 and (str(gas_som_path.get()) == "None" or str(gas_som_path.get())) == "":
                wrnmodal("When selecting Gasoline with somatic variant calling option, you need to specify a germline reference file", "WARNING")
            else:
                if w_dir.endswith(os.path.sep):
                    wrk_folder = w_dir[:-1]
                else:
                    wrk_folder = w_dir
                if SAMBAM:
                    op_seq = [DORADO, SAMBAM, SRTBAM, IDXBAM, bool(len(SVNANO)!=0), bool(len(SNVNANO)!=0), ANNANO]
                else:
                    op_seq = [DORADO, ALNANO, SRTBAM, IDXBAM, bool(len(SVNANO)!=0), bool(len(SNVNANO)!=0), ANNANO]
                for i, var in enumerate(op_seq):
                    if var:
                        frst_op = i
                        break
                if frst_op == 0 and not check_ext_folder(in_filepath, ".pod5"):
                    wrnmodal("There is no .pod5 format file in the input directory.","WARNING")
                elif frst_op == 1 and ALNANO and not in_filepath.endswith(".fastq"):
                    wrnmodal("The input file given is not in .fastq format.","WARNING")
                elif frst_op == 1 and SAMBAM and not in_filepath.endswith(".sam"):
                    wrnmodal("The input file given is not in .sam format.","WARNING")
                elif (frst_op == 2 or frst_op == 3 or frst_op == 4 or frst_op == 5) and not in_filepath.endswith(".bam"):
                    wrnmodal("The input file given is not in .bam format.","WARNING")
                elif frst_op == 6 and (not in_filepath.endswith(".vcf") and not in_filepath.endswith(".vcf.gz")):
                    wrnmodal("The input file given is not in .vcf or vcf.gz format.", "WARNING")
                else:
                    if not os.path.exists(wrk_folder):
                        wrnmodal("You need to select an already existing Working Directory", "WARNING")
                    else:
                                                                                            #CONFIG.YAML FILE MODIFICATIONS
                        launch_name = None
                        core_num = threads_num
                        ref_vers = ""
                        refer_gen = ""
                        if "GRCh37/hg19" in str(ref):
                            ref_vers = "hg19"
                            refer_gen = hg19_path.get()
                        else:
                            ref_vers = "hg38"
                            refer_gen = hg38_path.get()
                        if not dorado_device:
                            dorado_device = "cuda:all"
                        else:
                            dorado_device = str(dorado_device)
                        if not dorado_modifiedbases:
                            dorado_modifiedbases = "None"
                        else:
                            dorado_modifiedbases = dorado_modifiedbases
                        vec_dorado = tool_vec_create(str(dorado_model), str(dorado_device), str(dorado_modifiedbases), "", "--device ", "--modified-bases ")
                        par_dorado = OrderedDict([("model", vec_dorado[0]), ("--device", vec_dorado[1]), ("--modified-bases", vec_dorado[2]), ("adv", dorado_advp)])
                        vec_svim = tool_vec_create(str(svim_minmapq), str(svim_minsvsize), str(svim_maxsvsize), str(svim_skipgenotyping), str(svim_minimumscore), str(svim_minimumdepth), "--min_mapq ", "--min_sv_size ", "--max_sv_size ", "--skip_genotyping ", "--minimum_score ", "--minimum_depth ")
                        par_svim = OrderedDict([("--min_mapq", vec_svim[0]), ("--min_sv_size", vec_svim[1]), ("--max_sv_size", vec_svim[2]), ("--skip_genotyping", vec_svim[3]), 
                                                ("--minimum_score", vec_svim[4]), ("--minimum_depth", vec_svim[5]), ("adv", svim_advp)])
                        if not snif_minsupport:
                            snif_minsup = "--minsupport auto"
                        else:
                            snif_minsup = "--minsupport "+str(snif_minsupport)
                        vec_snif = tool_vec_create(str(snif_phase), str(snif_minsupport), str(snif_minsvlen), str(snif_mapq), str(snif_noqc),
                                                    "--phase ", "--minsupport ", "--minsvlen ", "--mapq ", "--no-qc ")
                        par_snif = OrderedDict([("--phase", vec_snif[0]),("--minsupport", snif_minsup),("--minsvlen", vec_snif[2]),
                                                    ("--mapq", vec_snif[3]), ("--no-qc", vec_snif[4]), ("adv", snif_advp)])
                        vec_cut = tool_vec_create(str(cut_minmapq), str(cut_minreadlen), str(cut_minsupport), str(cut_minsize), str(cut_maxsize), str(cut_genotype), "--min_mapq ", "--min_read_len ", "--min_support ", "--min_size ", "--max_size ", "--genotype ")
                        par_cut = OrderedDict([("--min_mapq", vec_cut[0]), ("--min_read_len", vec_cut[1]), ("--min_support", vec_cut[2]), ("--min_size", vec_cut[3]),
                                                   ("--max_size", vec_cut[4]), ("--genotype", vec_cut[5]), ("adv", cut_advp)])
                        if gas_bed_path.get() == "":
                            gas_bed_path.set(None)
                        if gas_som_check == 0:
                            vec_gas = tool_vec_create(str(gas_pars_Q), str(gas_bed_path.get()), str(gas_germ_NS), str(gas_germ_Q), str(gas_germ_MS), str(gas_germ_OT),
                                                      str(gas_germ_vcf_TS), str(gas_germ_vcf_TC), str(gas_germ_vcf_TI), str(gas_germ_vcf_TO), 
                                                      "-Q ", "-T ", "-NS " ,"-Q ", "-MS ", "-OT ", "-TS ", "-TC ", "-TI ", "-TO ")
                            par_gas = OrderedDict([("pars_Q", vec_gas[0]),("pars_T", vec_gas[1]), ("germ_NS", vec_gas[2]), ("germ_Q", vec_gas[3]), ("germ_MS", vec_gas[4]), 
                                                   ("germ_OT", vec_gas[5]), ("germ_vcf_TS", vec_gas[6]), ("germ_vcf_TC", vec_gas[7]), ("germ_vcf_TI", vec_gas[8]), ("germ_vcf_TO", vec_gas[9])])
                        else:
                            vec_gas = tool_vec_create(str(gas_som_path.get()), str(gas_pars_Q), str(gas_bed_path.get()), str(gas_germ_NS), str(gas_germ_Q), str(gas_germ_MS), str(gas_germ_OT),
                                                      str(gas_germ_vcf_TS), str(gas_germ_vcf_TC), str(gas_germ_vcf_TI), str(gas_germ_vcf_TO), str(gas_som_NS), str(gas_som_Q), 
                                                      str(gas_som_MS), str(gas_som_OV), str(gas_som_vcf_TS), str(gas_som_vcf_TC), str(gas_som_vcf_TI), str(gas_som_vcf_TO), 
                                                      str(gas_som_vcf_TR), str(gas_som_vcf_TP), str(gas_som_vcf_TH), "", "-Q ", "-T ", "-NS " ,"-Q ", "-MS ", "-OT ", "-TS ", "-TC ", "-TI ", "-TO ",
                                                      "-NS ", "-Q ", "-MS ", "-OV ", "-TS ", "-TC ", "-TI ", "-TO ", "-TR ", "-TP ", "-TH ")
                            par_gas = OrderedDict([("som_ref", vec_gas[0]),("pars_Q", vec_gas[1]),("pars_T", vec_gas[2]), ("germ_NS", vec_gas[3]), ("germ_Q", vec_gas[4]), ("germ_MS", vec_gas[5]), 
                                                   ("germ_OT", vec_gas[6]), ("germ_vcf_TS", vec_gas[7]), ("germ_vcf_TC", vec_gas[8]), ("germ_vcf_TI", vec_gas[9]), ("germ_vcf_TO", vec_gas[10]),
                                                   ("som_NS",vec_gas[11]), ("som_Q", vec_gas[12]), ("som_MS", vec_gas[13]), ("som_OV", vec_gas[14]), ("som_vcf_TS", vec_gas[15]), ("som_vcf_TC", vec_gas[16]), 
                                                   ("som_vcf_TI", vec_gas[17]),  ("som_vcf_TO", vec_gas[18]), ("som_vcf_TR", vec_gas[19]), ("som_vcf_TP", vec_gas[20]), ("som_vcf_TH", vec_gas[21])])
                        if not long_region:
                             long_reg = "None"
                        else:
                             long_reg = str(long_region)
                        vec_long = tool_vec_create(long_reg, str(long_mincov), str(long_maxcov), str(long_minmapq), str(long_minaltcount), str(long_minaltfrac),
                                                   "--region ", "--min_cov ", "--max_cov ", "--min_mapq ", "--min_alt_count ", "--min_alt_frac ")
                        par_long = OrderedDict([("--region", vec_long[0]), ("--min_cov", vec_long[1]), ("--max_cov", vec_long[2]), ("--min_mapq", vec_long[3]),
                                                    ("--min_alt_count", vec_long[4]), ("--min_alt_frac", vec_long[5]), ("adv", long_advp)])
                        vec_nanoc = tool_vec_create(str(nanoc_mode), str(nanoc_mincov), str(nanoc_maxcov), str(nanoc_bed_path.get()), str(nanoc_phase), "--mode ", "--mincov ", "--maxcov ",
                                                    "--bed ", "--phase ")
                        par_nanoc = OrderedDict([("--mode", vec_nanoc[0]), ("--mincov", vec_nanoc[1]), ("--maxcov", vec_nanoc[2]), ("--bed", vec_nanoc[3]), ("--phase", vec_nanoc[4]), ("adv", nanoc_advp)])
                        if cla3_callsnponly:
                            cla3snponly = "enable"
                        else:
                            cla3snponly = "disable"
                        vec_cla3 = tool_vec_create(str(clair3_mod_path.get()), str(clair3_bed_path.get()), str(cla3_qual), str(cla3_snpminaf), str(cla3_indelminaf), str(cla3_minmq), str(cla3snponly), 
                                                   "--model_path ", "--bed_fn ", "--qual ", "--snp_min_af ", "--indel_min_af ", "--min_mq ", "--call_snp_only ")
                        par_cla3 = OrderedDict([("--model_path", vec_cla3[0]), ("--bed_fn", vec_cla3[1]), ("--qual", vec_cla3[2]), ("--snp_min_af", vec_cla3[3]), ("--indel_min_af", vec_cla3[4]), 
                                                    ("--min_mq", vec_cla3[5]), ("--call_snp_only", vec_cla3[6]), ("adv", cla3_advp)])
                        if not deep_region:
                             deep_reg = "None"
                        else:
                             deep_reg = str(deep_region)
                        vec_deep = tool_vec_create(deep_reg, str(deep_pepperminmapq), str(deep_pepperminsnpbaseq), str(deep_pepperminindelbaseq), str(deep_peppersnpfrequency), 
                                                   str(deep_pepperinsertfrequency), str(deep_pepperdeletefrequency), str(deep_pepperskipindels), str(deep_dvminmappingquality), 
                                                   str(deep_dvminbasequality), "--region ", "--pepper_min_mapq ", "--pepper_min_snp_baseq ", "--pepper_min_indel_baseq ", "--pepper_snp_frequency ", 
                                                   "--pepper_insert_frequency ", "--pepper_delete_frequency ", "--pepper_skip_indels ", "--dv_min_mapping_quality ", "--dv_min_base_quality ")
                        par_deep = OrderedDict([("--region", vec_deep[0]), ("--pepper_min_mapq", vec_deep[1]), ("--pepper_min_snp_baseq", vec_deep[2]),  ("--pepper_min_indel_baseq", vec_deep[3]), 
                                                ("--pepper_snp_frequency", vec_deep[4]), ("--pepper_insert_frequency", vec_deep[5]), ("--pepper_delete_frequency", vec_deep[6]), 
                                                ("--pepper_skip_indels", vec_deep[7]), ("--dv_min_mapping_quality", vec_deep[8]), ("--dv_min_base_quality", vec_deep[9]), ("adv", deep_advp)])
                        vec_ann = tool_vec_create(str(int(ann_svinputinfo)), str(ann_annotationmode), str(ann_tx), str(ann_svminsize),"-SVinputInfo ", "-annotationMode ", "-tx ", "-SVminSize ")
                        par_ann = OrderedDict([("-SVinputInfo", vec_ann[0]), ("-annotationMode", vec_ann[1]), ("-tx", vec_ann[2]), ("-SVminSize", vec_ann[3]), ("adv", ann_advp)])
                        if str(vep_cache) != "--cache":
                            vep_dir_cache = "None"
                            vep_offline = False
                        else:
                            vep_dir_cache = str(vep_dircache.get())
                        if not vep_offline:
                            vep_ref = ""
                        else:
                            vep_ref = f"--fasta {refer_gen}"
                        vec_vep = tool_vec_create(str(vep_everything), str(vep_cache), vep_dir_cache, str(vep_codingonly), str(vep_nointergenic), str(vep_offline), str(vep_ref),
                                                  "--everything ", "", "--dir_cache ", "--coding_only ", "--no_intergenic ", "--offline ", "")
                        par_vep = OrderedDict([("--everything", vec_vep[0]), ("--cache", vec_vep[1]), ("--dir_cache", vec_vep[2]), ("--coding_only", vec_vep[3]), ("--no_intergenic", vec_vep[4]), ("--offline", vec_vep[5]), ("--fasta", vec_vep[6]), ("adv", vep_advp)])
                        data["threads"] = core_num
                        data["ref_version"] = ref_vers
                        data["ref_genome"] = refer_gen
                        #More than one sample NOT WORKING
                        if sampsize == True:
                            mulfiles_tmp = re.split('[,;\s]+', up_mul_file) 
                            mulfiles_tmp = list(filter(None, mulfiles_tmp))
                            data["in_file"] = mulfiles_tmp
                            if mulcst_name_check == 1:
                                mulcst_tmp = re.split('[,;\s]+', mulcst_name)
                                launch_name = list(filter(None, mulcst_tmp))
                                data["cstm_name"] = launch_name
                            else:
                                launch_name = []
                                for file_element in mulfiles_tmp:
                                    lauch_element = os.path.splitext(os.path.basename(file_element))[0]
                                    launch_name.append(lauch_element)
                                data["cstm_name"] = launch_name
                        else:
                            data["in_file"] = in_filepath
                            if singcst_name_check == 1:
                                if not singcst_name:
                                    launch_name = os.path.splitext(os.path.basename(in_filepath))[0]
                                else:
                                    launch_name = singcst_name
                                data["cstm_name"] = launch_name
                            else:
                                launch_name = os.path.splitext(os.path.basename(in_filepath))[0]
                                data["cstm_name"] = launch_name
                            data["work_folder"] = wrk_folder
                        dor_sel = []
                        if DORADO == 1 and (ALNANO == 1 or SRTBAM == 1 or IDXBAM == 1 or len(SVNANO) > 0 or len(SNVNANO) > 0 or ANNANO == 1):
                            dor_sel.append("True")
                        else:
                            dor_sel.append("False")
                        data["dorado_minimap2"] = dor_sel
                        bool_updconf(DORADO, def_dorado, par_dorado, data, "par_dorado")
                        updconfadv(ALNANO, def_alnano, data, "par_alnano", alnano_advp)
                        updconfadv(SAMBAM, def_sambam, data, "par_sambam", sambam_advp)
                        #updconfadv(input.MULINP(), input.def_mulinp(), data, "par_mulinp", input.mulinp_advp())
                        samt_sel = []
                        if SAMBAM == 1:
                            samt_sel.append("sam_bam")
                        if SRTBAM == 1:
                             samt_sel.append("sorting")
                        if IDXBAM == 1:
                             samt_sel.append("indexing")
                        data["samtools_selection"] = samt_sel
                        updconfadv(SRTBAM, def_srtbam, data, "par_srtbam", srtbam_advp)
                        updconfadv(IDXBAM, def_idxbam, data, "par_idxbam", idxbam_advp)
                        updconf("SVIM", SVNANO, def_svim, par_svim, data, "par_svim")
                        updconf("Sniffles2", SVNANO, def_snif, par_snif, data, "par_snif")
                        updconf("cuteSV", SVNANO, def_cut, par_cut, data, "par_cut")
                        gas_sel = []
                        if gas_som_check == 1:
                             gas_sel.append("somatic")
                        else:
                            gas_sel.append("germline")
                        data["gas_som_selection"] = gas_sel
                        if "Gasoline" in SVNANO and gas_som_check == 1:
                                data["par_gas"]["som_ref"] = gas_som_path.get()
                        updconf("Gasoline", SVNANO, def_gas, par_gas, data, "par_gas")
                        updconf("Longshot", SNVNANO, def_long, par_long, data, "par_long")
                        updconf("NanoCaller", SNVNANO, def_nanoc, par_nanoc, data, "par_nanoc")
                        if "Clair3" in SNVNANO and def_cla3:
                            data["par_cla3"]["--model_path"] = f"--model_path {str(clair3_mod_path())}"
                        updconf("Clair3", SNVNANO, def_cla3, par_cla3, data, "par_cla3")
                        updconf("DeepVariant", SNVNANO, def_deep, par_deep, data, "par_deep")
                        ann_sel = []
                        if ANNANO == 1:
                            ann_sel.append("annotation")
                            if "AnnotSV" in ONLYANNANO:
                                ann_sel.append("annotsv")
                            elif "VEP" in ONLYANNANO:
                                ann_sel.append("vep")
                        data["annotation_selection"] = ann_sel
                        updconfvariant(ANNANO, def_ann, par_ann, data, "par_ann")
                        updconfvariant(ANNANO, def_vep, par_vep, data, "par_vep")
                        paral_varcall = [tool for tool in SVNANO + SNVNANO if tool not in ["SVIM", "Longshot"]]
                        no_paral_varcall = [tool for tool in ["SVIM", "Longshot"] if tool in SVNANO + SNVNANO]
                        paral_threads = threads_num-len(no_paral_varcall)
                        if int(paral_threads) < (len(paral_varcall)+len(no_paral_varcall)):
                            data["paral_threads"] = 1
                        else:
                            data["paral_threads"] = paral_threads
                        data["paral_ops"] = len(paral_varcall)
                        data["paral_exc"] = len(no_paral_varcall)
                        config_path = f"{wrk_folder}/{launch_name}"
                        if not os.path.exists(config_path):
                            os.makedirs(config_path)
                        config_path = f"{config_path}/config.yaml"
                        with open(config_path, 'wb') as f:
                            yaml.dump(data, f)
                                                                                                #SNAKEMAKE LAUNCH OPTIONS
                            vec_op = []
                        vec_tot_op = ["DORADO", "ALNANO", "SAMBAM", "SRTBAM", "IDXBAM", svnano, snvnano] #("SVIM", "Sniffles2", "cuteSV", "Gasoline"), ("Longshot", "Nanocaller", "Clair3", "DeepVariant") #"MULINP",
                        vec_sel_op = [DORADO, ALNANO, SAMBAM, SRTBAM, IDXBAM, len(SVNANO) > 0, len(SNVNANO) > 0] #input.MULINP(),
                        for op, selec in zip(vec_tot_op, vec_sel_op):
                            if selec == True:
                                if isinstance(op, list):
                                    if len(SVNANO) > 0:
                                        vec_op.extend([var for var in SVNANO if var not in vec_op])
                                    if len(SNVNANO) > 0:
                                        vec_op.extend([var for var in SNVNANO if var not in vec_op])
                                else:
                                    vec_op.append(op)
                            unique_vec = " ".join(vec_op)
                            unique_vec = str(unique_vec)
                        pipe_cmd = nangenline_compiler(unique_vec, ann_sel, wrk_folder, launch_name, core_num) 
                        return subprocess.run(pipe_cmd, shell=True) 