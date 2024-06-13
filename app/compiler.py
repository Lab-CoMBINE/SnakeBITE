import os

def check_varcall_op(operations, op, out, outputs):
    if op in operations:
        outputs=f"{outputs} {out}"
        return outputs
    else:
        return
    
def check_nannot_op(vec, ops):
    if not vec:
        return "empty"
    elif vec[0] == ops[0]:
        if len(vec) == 1:
            return "only_annot"
        elif len(vec) == 2:
            sec_el = vec[1]
            if sec_el == ops[1]:
                return "annotation_annotsv"
            elif sec_el == ops[2]:
                return "annotation_vep"
    else:
        return

def nangenline_compiler(ops, ann_vec, work_dir, cst_name, ref1, ref2, in_file, cores, snake_dir):
    selected_var_call = any(keyword in ops for keyword in ["SVIM", "Sniffles2", "cuteSV", "Gasoline", "Longshot", "NanoCaller", "Clair3", "DeepVariant"])
    annot_op = check_nannot_op(ann_vec, ["annotation", "annotsv", "vep"])
    outputs = ""
    snake_cmd = ""
    sing_bind1 = ""
    if (selected_var_call == True):
        if annot_op == "empty":
            svim_out = f"{work_dir}/{cst_name}/sv/{cst_name}_svim"
            sniffles_out = f"{work_dir}/{cst_name}/sv/{cst_name}_sniffles.vcf"
            cutesv_out = f"{work_dir}/{cst_name}/sv/{cst_name}_cutesv.vcf"
            gasoline_out = f"{work_dir}/{cst_name}/sv/{cst_name}_gasoline/gasoline_final.vcf"
            longshot_out = f"{work_dir}/{cst_name}/snv/{cst_name}_longshot.vcf"
            nanocaller_out = f"{work_dir}/{cst_name}/snv/{cst_name}_nanocaller"
            clair3_out = f"{work_dir}/{cst_name}/snv/{cst_name}_clair3"
            deepvariant_out = f"{work_dir}/{cst_name}/snv/{cst_name}_deepvariant"
        elif annot_op == "only_annot":
            svim_out = f"{work_dir}/{cst_name}/sv/{cst_name}_svim_annotsv.tsv"
            sniffles_out = f"{work_dir}/{cst_name}/sv/{cst_name}_sniffles_annotsv.tsv"
            cutesv_out = f"{work_dir}/{cst_name}/sv/{cst_name}_cutesv_annotsv.tsv"
            gasoline_out = f"{work_dir}/{cst_name}/sv/{cst_name}_gasoline_annotsv.tsv"
            longshot_out = f"{work_dir}/{cst_name}/snv/{cst_name}_longshot_vep.vcf"
            nanocaller_out = f"{work_dir}/{cst_name}/snv/{cst_name}_nanocaller_vep.vcf"
            clair3_out = f"{work_dir}/{cst_name}/snv/{cst_name}_clair3_vep.vcf"
            deepvariant_out = f"{work_dir}/{cst_name}/snv/{cst_name}_deepvariant_vep.vcf"
        if "SVIM" in ops:
            outputs = f"{outputs} {svim_out}"
        if "Sniffles2" in ops:
            outputs = f"{outputs} {sniffles_out}"
        if "cuteSV" in ops:
            outputs = f"{outputs} {cutesv_out}"
        if "Gasoline" in ops:
            outputs = f"{outputs} {gasoline_out}"
        if "Longshot" in ops:
            outputs = f"{outputs} {longshot_out}"
        if "NanoCaller" in ops:
            outputs = f"{outputs} {nanocaller_out}"
        if "Clair3" in ops:
            outputs = f"{outputs} {clair3_out}"
        if "DeepVariant" in ops:
            outputs = f"{outputs} {deepvariant_out}"
    else:
        annotsv_out = f"{work_dir}/{cst_name}/sv/{cst_name}_annotsv.tsv"
        vep_out = f"{work_dir}/{cst_name}/snv/{cst_name}_vep.vcf"
        dorado_out = f"{work_dir}/{cst_name}/mapped_reads/{cst_name}.bam"
        minimap_out = f"{work_dir}/{cst_name}/mapped_reads/{cst_name}.bam"
        sambam_out=f"{work_dir}/{cst_name}/mapped_reads/{cst_name}.bam"
        srt_out=f"{work_dir}/{cst_name}/sorted_reads/{cst_name}_sorted.bam"
        idx_out=f"{work_dir}/{cst_name}/sorted_reads/{cst_name}_sorted.bam.bai"
        if annot_op == "annotation_annotsv":
            outputs = f"{outputs} {annotsv_out}"
        elif annot_op == "annotation_vep":
            outputs = f"{outputs} {vep_out}"
        else:
            if "IDXBAM" in ops:
                outputs = f"{outputs} {idx_out}"
            else:
                if "SRTBAM" in ops:
                    outputs = f"{outputs} {srt_out}"
                else:
                    if "SAMBAM" in ops:
                        outputs = f"{outputs} {sambam_out}"
                    elif "DORADO" in ops:
                        outputs = f"{outputs} {dorado_out}"
                    elif "ALNANO" in ops and "DORADO" not in ops:
                        outputs = f"{outputs} {minimap_out}"
    #bind_sing = f'--singularity-args \"--bind {work_dir}, {os.path.dirname(ref1)}, {os.path.dirname(ref2)}, {os.path.dirname(in_file)}, /data2/abimbocci\"'
    snake_cmd = f'nohup snakemake --snakefile {snake_dir}/Snakefile --use-conda --use-singularity --cores {cores} --printshellcmds --keep-going --configfile={work_dir}/{cst_name}/config.yaml {outputs} >> {work_dir}/{cst_name}/log.out'
    return snake_cmd
