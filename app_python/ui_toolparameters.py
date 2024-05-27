from shiny import ui
from ui_utils import question_circle_fill as qst

#UI-SIDE GENERIC FUNCTIONS FOR PARAMETERS TAB:

def condpar(in_id, cond1, cond2, op, defa, par_func):
    return ui.panel_conditional(cond1,
                    def_opt(op,defa), 
                    ui.panel_conditional(cond2, 
                    par_func
                    ),
                    ui.hr()
                ),

#VARIOUS WRAPPERS FOR SIMPLE PARAMETERS SELECTION

def par_switch_wrapper(par_name, par_idx, par_def, descr):
    nm = str(not(par_def))
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_switch(par_idx, nm, value = par_def)), ui.column(6, descr, ui.hr()))

def par_switchvar_wrapper(par_name, par_idx, par_def, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_switch(par_idx, par_def, value = par_def)), ui.column(6, descr, ui.hr()))

def par_num_switch_wrapper(par_name, par_idx, par_def, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_switch(par_idx, "",value = par_def)), ui.column(6, descr, ui.hr()))

def par_num_wrapper(par_name, par_idx, par_def, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_numeric(par_idx, "", value = par_def)), ui.column(6, descr, ui.hr()))

def par_numfloat_wrapper(par_name, par_idx, par_def, par_step, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_numeric(par_idx, "", value = par_def, min = 0, max = 1, step = par_step)), ui.column(6, descr, ui.hr()))

def par_text_wrapper(par_name, par_idx, par_def, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_text(par_idx, "", placeholder = par_def)), ui.column(6, descr, ui.hr()))

def par_sel_wrapper(par_name, par_idx, par_def, par_choi, descr):
    return ui.row(ui.column(2,par_name), ui.column(4, ui.input_selectize(par_idx, "", choices = par_choi, selected=par_def, multiple=False, width=None)), ui.column(6, descr, ui.hr()))

def par_datapath_wrapper(par_name, par_idx, out_text, descr):
    return ui.row(ui.column(2,par_name), ui.column(2, ui.input_action_button(par_idx, "Selected File:")), ui.column(2, ui.output_text_verbatim(out_text)), ui.column(6, descr, ui.hr()))

def par_folder_datapath_wrapper(par_name, par_idx, out_text, descr):
    return ui.row(ui.column(2,par_name), ui.column(2, ui.input_action_button(par_idx, "Selected Folder:")), ui.column(2, ui.output_text_verbatim(out_text)), ui.column(6, descr, ui.hr()))

def par_popover_wrapper(optitle, pword, plink):
    return ui.TagList(
        ui.popover(
            ui.span(optitle, qst),
            "See ",
                    ui.a(
                    pword,
                    href=plink,
                    target="_blank",
                ),
            placement="right",
            id="card_tooltip",
            )
    )

def advp(pid, pword, plink):
    return ui.TagList(
        ui.popover(
            ui.span("Advanced Options: ", qst),
            "Manually input a string of additional advanced options for the tool, as in ",
                    ui.a(
                    pword,
                    href=plink,
                    target="_blank",
                ),
            placement="right",
            id="card_tooltip",
            ),
        ui.input_text(pid, "", ""),
        )

def def_opt(toolid, defid):
    return ui.TagList(
        ui.h2(toolid + " SETTINGS"),
        ui.input_checkbox(defid, "Default Settings", value = True)
    )

#UI-SIDE NANOPORE GENOMICS PIPELINE:

def param_nangen():
    return ui.TagList(
        condpar("input.DORADO", "input.DORADO == 1", "input.def_dorado == 0", "DORADO", "def_dorado", param_dorado()),
        condpar("input.ALNANO", "input.ALNANO == 1 && input.DORADO == 0", "input.def_alnano == 0", "MINIMAP2", "def_alnano", param_alnano()),
        condpar("input.SAMBAM", "input.SAMBAM == 1", "input.def_sambam == 0", "SAMTOOLS SAM->BAM", "def_sambam", param_sambam()),
        #condpar("input.MULINP", "input.MULINP == 1", "input.def_mulinp == 0", "SAMTOOLS MERGE", "def_mulinp", param_mulinp()),
        condpar("input.SRTBAM", "input.SRTBAM == 1", "input.def_srtbam == 0", "SAMTOOLS SORT", "def_srtbam", param_srtbam()),
        condpar("input.IDXBAM", "input.IDXBAM == 1", "input.def_idxbam == 0", "SAMTOOLS INDEX", "def_idxbam", param_idxbam()),
        condpar("input.SVNANO", "input.SVNANO.indexOf('SVIM') > -1", "input.def_svim == 0", "SVIM", "def_svim", param_svim()),
        condpar("input.SVNANO", "input.SVNANO.indexOf('Sniffles2') > -1", "input.def_snif == 0", "SNIFFLES2", "def_snif", param_snif()),
        condpar("input.SVNANO", "input.SVNANO.indexOf('cuteSV') > -1", "input.def_cut == 0", "CUTESV", "def_cut", param_cut()),
        ui.panel_conditional("input.SVNANO.indexOf('Gasoline') > -1",
                             ui.h2("GASOLINE SETTINGS"),
                             ui.input_checkbox("gas_som_check", "Perform Somatic Variant Calling", value = False),
                             ui.panel_conditional("input.gas_som_check == 1", par_datapath_wrapper("Reference", "gas_som_ref", "text_gassomref_dtpt", "Path to Somatic Variant Calling Reference")),#par_text_wrapper("Reference", "gas_som_ref", "Path/to/somatic/variant/calling/reference", "Path to Somatic Variant Calling Reference")),
                             ui.input_checkbox("def_gas", "Default Settings", value = True),
                             ui.panel_conditional("input.def_gas == 0", param_gas()),
                             ui.hr()
                             ),
        condpar("input.SNVNANO", "input.SNVNANO.indexOf('Longshot') > -1", "input.def_long == 0", "LONGSHOT", "def_long", param_long()),
        condpar("input.SNVNANO", "input.SNVNANO.indexOf('NanoCaller') > -1", "input.def_nanoc == 0", "NANOCALLER", "def_nanoc", param_nanoc()),
        ui.panel_conditional("input.SNVNANO.indexOf('Clair3') > -1",
                             ui.h2("CLAIR3 SETTINGS"),
                             par_folder_datapath_wrapper("Model", "cla3_mod", "text_cla3mod_dtpt", "The folder path containing a Clair3 model (requiring six files in the folder, including pileup.data-00000-of-00002, pileup.data-00001-of-00002 pileup.index, full_alignment.data-00000-of-00002, full_alignment.data-00001-of-00002 and full_alignment.index)."),
                             #par_sel_wrapper("Model", "cla3_mod", "---", ["---", "/data2/mbaragli/tools/Clair3/clair_models/r941_prom_sup_g5014", "/data2/mbaragli/tools/Clair3/clair_models/r941_prom_hac_g238"], "The folder path containing a Clair3 model (requiring six files in the folder, including pileup.data-00000-of-00002, pileup.data-00001-of-00002 pileup.index, full_alignment.data-00000-of-00002, full_alignment.data-00001-of-00002 and full_alignment.index)."), #("cla3_mod", "Select Clair3 Model", ["a", "b", "c"], selected=None),
                             ui.input_checkbox("def_cla3", "Default Settings", value = True),
                             ui.panel_conditional("input.def_cla3 == 0", param_cla3())
                             ),
        condpar("input.SNVNANO", "input.SNVNANO.indexOf('DeepVariant') > -1", "input.def_deep == 0", "DEEPVARIANT", "def_deep", param_deep()),
        condpar("input.ANNANO", "input.ANNANO == 1 && (input.SVNANO.length > 0 || input.ONLYANNANO.indexOf('AnnotSV') > -1)", "input.def_ann == 0", "ANNOTSV", "def_ann", param_ann()),
        condpar("input.ANNANO", "input.ANNANO == 1 && (input.SNVNANO.length > 0 || input.ONLYANNANO.indexOf('VEP') > -1)", "input.def_vep == 0", "VEP", "def_vep", param_vep()),
    )

def param_dorado():
    return ui.TagList(
        ui.h3("Common parameters"),
        par_sel_wrapper("Model", "dorado_model", "dna_r10.4.1_e8.2_400bps_fast@v4.3.0", ["dna_r10.4.1_e8.2_400bps_fast@v4.3.0","dna_r10.4.1_e8.2_400bps_hac@v4.3.0", "dna_r10.4.1_e8.2_400bps_sup@v4.3.0", 
                                                                                         "dna_r10.4.1_e8.2_400bps_fast@v4.2.0", "dna_r10.4.1_e8.2_400bps_hac@v4.2.0", "dna_r10.4.1_e8.2_400bps_sup@v4.2.0",
                                                                                         "dna_r10.4.1_e8.2_400bps_fast@v4.1.0", "dna_r10.4.1_e8.2_400bps_hac@v4.1.0", "dna_r10.4.1_e8.2_400bps_sup@v4.1.0",
                                                                                         "dna_r10.4.1_e8.2_260bps_fast@v4.1.0", "dna_r10.4.1_e8.2_260bps_hac@v4.1.0", "dna_r10.4.1_e8.2_260bps_sup@v4.1.0",
                                                                                         "dna_r10.4.1_e8.2_400bps_fast@v4.0.0", "dna_r10.4.1_e8.2_400bps_hac@v4.0.0", "dna_r10.4.1_e8.2_400bps_sup@v4.0.0",
                                                                                         "dna_r10.4.1_e8.2_260bps_fast@v4.0.0", "dna_r10.4.1_e8.2_260bps_hac@v4.0.0", "dna_r10.4.1_e8.2_260bps_sup@v4.0.0",
                                                                                         "dna_r10.4.1_e8.2_260bps_fast@v3.5.2", "dna_r10.4.1_e8.2_260bps_hac@v3.5.2", "dna_r10.4.1_e8.2_260bps_sup@v3.5.2",
                                                                                         "dna_r10.4.1_e8.2_400bps_fast@v3.5.2", "dna_r10.4.1_e8.2_400bps_hac@v3.5.2", "dna_r10.4.1_e8.2_400bps_sup@v3.5.2",
                                                                                         "dna_r9.4.1_e8_sup@v3.6", "dna_r9.4.1_e8_fast@v3.4", "dna_r9.4.1_e8_hac@v3.3", "dna_r9.4.1_e8_sup@v3.3"],
                                                                                         "model selection {fast,hac,sup}@v{version} for automatic model selection including modbases, or path to existing model directory"),
        par_text_wrapper("--device", "dorado_device", "cuda:all", "device string in format 'cuda:0,...,N', 'cuda:all', 'metal', 'cpu' etc.. [default: 'cuda:all']"),
        par_text_wrapper("--modified-bases", "dorado_modifiedbases", "", par_popover_wrapper("[nargs: 1 or more], manually insert the desired modified bases, depending on the chosen Model", "Compatible Modification Table", "https://github.com/nanoporetech/dorado?tab=readme-ov-file#dna-models")),
        advp("dorado_advp", "dorado Manual:", "https://github.com/nanoporetech/dorado?tab=readme-ov-file#performance-tips"),
    )

def param_alnano():
    return ui.TagList(
    advp("alnano_advp","minimap2 Manual:", "https://lh3.github.io/minimap2/minimap2.html"),
    )

def param_sambam():
    return ui.TagList(
    advp("sambam_advp","samtools view Manual","http://www.htslib.org/doc/samtools-view.html"),
    )

#def param_mulinp():
#    return ui.TagList(
#    advp("mulinp_advp","samtools merge Manual","http://www.htslib.org/doc/samtools-merge.html"),
#    )

def param_srtbam():
    return ui.TagList(
    advp("srtbam_advp","samtools sort Manual","http://www.htslib.org/doc/samtools-sort.html"),
    )

def param_idxbam():
    return ui.TagList(
    advp("idxbam_advp","samtools index Manual", "http://www.htslib.org/doc/samtools-index.html"),
    )

def param_svim():
    return ui.TagList(
    ui.h3("Collect SVS parameters"),
    par_num_wrapper("--min_mapq", "svim_minmapq", 20, "Minimum mapping quality of reads to consider (default:20). Reads with a lower mapping quality are ignored."),
    par_num_wrapper("--min_sv_size", "svim_minsvsize", 40, "Minimum SV size to detect (default: 40). SVIM canpotentially detect events of any size but is limitedby the signal-to-noise ratio in the input alignments.That means that more accurate reads and alignmentsenable the detection of smaller events. For currentPacBio or Nanopore data, we would recommend a minimumsize of 40bp or larger."),
    par_num_wrapper("--max_sv_size", "svim_maxsvsize", 100000, "Maximum SV size to detect (default: 100000). Thisparameter is used to distinguish long deletions (andinversions) from translocations which cannot bedistinguished from the alignment alone. Split readsegments mapping far apart on the reference couldeither indicate a very long deletion (inversion) or atranslocation breakpoint. SVIM calls a translocationbreakpoint if the mapping distance is larger than thisparameter and a deletion (or inversion) if it issmaller or equal."),
    ui.h3("Genotyping parameters"),
    par_switch_wrapper("--skip_genotyping", "svim_skipgenotyping", False, "Disable genotyping (default: False)"),
    par_num_wrapper("--minimum_score", "svim_minimumscore", 3, "Minimum score for genotyping (default: 3). Only SVcandidates with a higher or equal score are genotyped.Depending on the score distribution among the SVcandidates, decreasing this value increases theruntime. We recommend to choose a value close to thescore threshold used for filtering the SV candidates."),
    par_num_wrapper("--minimum_depth", "svim_minimumdepth", 4, "Minimum total read depth for genotyping (default: 4).Variants covered by a total number of reads lower thanthis value are not assigned a genotype (./. in theoutput VCF file)."),
    advp("svim_advp","svim alignment Manual","https://github.com/eldariont/svim/wiki/Command-line-parameters"),
    )

def param_snif():
    return ui.TagList(
    ui.h3("Common parameters"),
    #par_switch_wrapper("--non-germline", "snif_nongermline", False, "Call non-germline SVs (rare, somatic or mosaic SVs) (Default: False)"),
    par_switch_wrapper("--phase", "snif_phase", False, "Determine phase for SV calls (requires the input alignments to be phased) (Default: False)"),
    ui.h3("SV filtering parameters"),
    par_text_wrapper("--minsupport", "snif_minsupport", "auto", "Minimum number of supporting reads for a SV to be reported (default: automatically choose based on coverage) (Default: auto)"),                                                           
    par_num_wrapper("--minsvlen", "snif_minsvlen", 35, "Minimum SV length (in bp) (default: 35)"),
    par_num_wrapper("--mapq", "snif_mapq", 25, "Alignments with mapping quality lower than this value will be ignored (Default: 25)"),
    par_switch_wrapper("--no-qc", "snif_noqc", False, "Output all SV candidates, disregarding quality control steps. (Default: False)"),
    advp("snif_advp","Sniffles2 Manual","https://manpages.ubuntu.com/manpages/jammy/man1/sniffles.1.html"),
    )

def param_cut():
    return ui.TagList(
    ui.h3("SV signatures collection parameters"),
    par_num_wrapper("--min_mapq", "cut_minmapq", 20, "Minimum mapping quality value of alignment to be taken into account. (Default: 20)"),
    par_num_wrapper("--min_read_len", "cut_minreadlen", 500, "Ignores reads that only report alignments with not longer than bp. (Default: 500)"),
    ui.h3("SV clusters generation parameters"),
    par_num_wrapper("--min_support", "cut_minsupport", 10, "Minimum number of reads that support a SV to be reported. (Default: 10)"),
    par_num_wrapper("--min_size", "cut_minsize", 30, "Minimum length of SV to be reported. (Default: 30)"),
    par_num_wrapper("--max_size", "cut_maxsize", 100000, "Maximum size of SV to be reported. Full length SVs are reported when using -1. (Default: 100000)"),
    ui.h3("Genotype computing parameters"),
    par_switch_wrapper("--genotype", "cut_genotype", False, "Enable to generate genotypes. (Default: False)"),
    advp("cut_advp","cuteSV Manual","https://github.com/tjiangHIT/cuteSV"),
    )

def param_gas():
    return ui.TagList(
    ui.h3("Parsing parameters"),
    par_num_wrapper("-Q", "gas_pars_Q", 20, "Mapping Quality Threshold to filter our reads from the analysis. (Default: 20)"),
    par_datapath_wrapper("-T", "gas_pars_T", "text_gasbed_dtpt","bed file with the genomic coordinates of the regions where to perform the analysis. (Default: all the genome)"),
    #par_text_wrapper("-T", "gas_pars_T", "path/to/bed/file", "bed file with the genomic coordinates of the regions where to perform the analysis. (Default: all the genome)"),
    ui.h3("SV Germline detection parameters"),
    par_num_wrapper("-NS", "gas_germ_NS", 5000, "Normalization size factor. (Default: 5000)"),
    par_num_wrapper("-Q", "gas_germ_Q", 20, "Mapping Quality Threshold to filter our reads from the analysis. (Default: 20)"),
    par_num_wrapper("-MS", "gas_germ_MS", 2, "The minimum number of signatures for calling a variant. (Default: 2)"),
    par_numfloat_wrapper("-OT", "gas_germ_OT", 0.8, 0.1, "Overlap between SV signatures. (Default: 0.8)"),
    ui.h3("Germline VCF create parameters"),
    par_num_wrapper("-TS", "gas_germ_vcf_TS", 40, "Threshold to filter out SVs based on breakends sd estimation. (Default: 40)"),
    par_num_wrapper("-TC", "gas_germ_vcf_TC", 10, "Minimum coverage threshold to filter our SVs in test and/or control samples. (Default: 10)"),
    par_numfloat_wrapper("-TI", "gas_germ_vcf_TI", 0.8, 0.1, "Coesion threshold to filter outìr insertions. (Default: 0.8)"),
    par_numfloat_wrapper("-TO", "gas_germ_vcf_TO", 0.9, 0.1, "Coesion threshold to filter other SVs. (Default: 0.9)"),
    ui.panel_conditional("input.gas_som_check == 1",
        ui.h3("Somatic detection parameters"),
        par_num_wrapper("-NS", "gas_som_NS", 5000, "Normalization size factor. (Default: 5000)"),
        par_num_wrapper("-Q", "gas_som_Q", 20, "Mapping Quality Threshold to filter our reads from the analysis. (Default: 20)"),
        par_num_wrapper("-MS", "gas_som_MS", 2, "The minimum number of signatures for calling a variant. (Default: 2)"),
        par_numfloat_wrapper("-OV", "gas_som_OV", 0.8, 0.1, "Overlap between SV signatures. (Default: 0.8)"),
        ui.h3("Somatic VCF create parameters"),
        par_num_wrapper("-TS", "gas_som_vcf_TS", 40, "Threshold to filter out SVs based on breakends sd estimation. (Default: 40)"),
        par_num_wrapper("-TC", "gas_som_vcf_TC", 10, "Minimum coverage threshold to filter our SVs in test and/or control samples. (Default: 10)"),
        par_numfloat_wrapper("-TI", "gas_som_vcf_TI", 0.8, 0.1,"Coesion threshold to filter outìr insertions. (Default: 0.8)"),
        par_numfloat_wrapper("-TO", "gas_som_vcf_TO", 0.9, 0.1, "Coesion threshold to filter other SVs. (Default: 0.9)"),
        par_num_wrapper("-TR", "gas_som_vcf_TR", 2, "Maximum number of SV signatures allowed in control sample to call a somatic SV. (Default = 2)"),
        par_numfloat_wrapper("-TP", "gas_som_vcf_TP", 0.05, 0.01, "Minimum somatic p-value threshold to call a somatic SV. (Default: 0.05)"),
        par_numfloat_wrapper("-TH", "gas_som_vcf_TH", 0.001, 0.001, "Minimum somatic p-value threshold to call a high quality somatic SV. (Default: 0.001)"),
        ),
    )

def param_long():
    return ui.TagList(
    ui.h3("Common parameters"),
    par_text_wrapper("--region", "long_region", "# or #:#-#", "Region in format <chrom> or <chrom:start-stop> in which to call variants(1-based, inclusive)."),
    par_num_wrapper("--min_cov", "long_mincov", 6, "Minimum coverage (of reads passing filters) to consider position as a potential SNV. (Default: 6)"),
    par_num_wrapper("--max_cov", "long_maxcov", 8000, "Maximum coverage (of reads passing filters) to consider position as a potential SNV. [default: 8000]"),
    par_num_wrapper("--min_mapq", "long_minmapq", 20, "Minimum mapping quality to use a read. (Default: 20)"),
    par_num_wrapper("--min_alt_count", "long_minaltcount", 3, "Require a potential SNV to have at least this many alternate allele observations. (Default: 3)"),
    par_numfloat_wrapper("--min_alt_frac", "long_minaltfrac", 0.125, 0.001, "Require a potential SNV to have at least this fraction of alternate allele observations. [default: 0.125]"),
    advp("long_advp","longshot Manual","https://github.com/pjedge/longshot"),
    )

def param_nanoc():
    return ui.TagList(
    ui.h3("Configuration parameters"),
    par_sel_wrapper("--mode", "nanoc_mode", "all", ["snps", "indels", "all"], "NanoCaller mode to run. 'snps' mode quits NanoCaller without using WhatsHap for phasing. In this mode, if you want NanoCaller to phase SNPs and BAM files, use --phase argument additionally. (Default: all)"),
    par_num_wrapper("--mincov", "nanoc_mincov", 4, "Minimum coverage to call a variant (Default: 4)"),
    par_num_wrapper("--maxcov", "nanoc_maxcov", 160, "Maximum coverage of reads to use. If sequencing depth at a candidate site exceeds maxcov then reads are downsampled. (Default: 160)"),
    ui.h3("Variant calling region parameters"),
    par_datapath_wrapper("--bed", "nanoc_bed", "text_nanocbed_dtpt", "A BED file specifying regions for variant calling. (Default: None)"),
    #par_text_wrapper("--bed", "nanoc_bed", "path/to/bed/file", "A BED file specifying regions for variant calling. (Default: None)"),
    ui.h3("Phasing parameters"),
    par_switch_wrapper("--phase", "nanoc_phase", False, "Phase SNPs and BAM files if snps mode is selected. (Default: False)"),
    advp("nanoc_advp","NanoCaller Manual","https://github.com/WGLab/NanoCaller/blob/master/docs/Usage.md"),
    )

def param_cla3():
    return ui.TagList(
    ui.h3("Common parameters"),
    par_datapath_wrapper("--bed_fn", "cla3_bedfn", "text_cla3bed_dtpt", "Call variants only in the provided bed regions."),
    #par_text_wrapper("--bed_fn", "cla3_bedfn", "path/to/bed/file", "Call variants only in the provided bed regions."),
    par_num_wrapper("--qual", "cla3_qual", 0, "If set, variants with >$qual will be marked PASS, or LowQual otherwise."),
    par_numfloat_wrapper("--snp_min_af", "cla3_snpminaf", 0.08, 0.01, "Minimum SNP AF required for a candidate variant. Lowering the value might increase a bit of sensitivity in trade of speed and accuracy, (Default: 0.08)"),
    par_numfloat_wrapper("--indel_min_af", "cla3_indelminaf", 0.15, 0.01, "Minimum INDEL AF required for a candidate variant. Lowering the value might increase a bit of sensitivity in trade of speed and accuracy, (Default: 0.15"),
    par_num_wrapper("--min_mq", "cla3_minmq", 5, "EXPERIMENTAL: If set, reads with mapping quality with <$min_mq are filtered, default: 5."),
    par_switch_wrapper("--call_snp_only", "cla3_callsnponly", False, "EXPERIMENTAL: Call candidates pass SNP minimum AF only, ignore Indel candidates. (Default: disable)"),
    advp("cla3_advp","Clair3 Manual","https://github.com/HKU-BAL/Clair3#Usage"),
    )

def param_deep():
    return ui.TagList(
    ui.h3("General parameters"),
    par_text_wrapper("--region", "deep_region", "[contig_name:start-end]", "Region in [contig_name:start-end] format."),
    ui.h3("Pepper parameters"),
    par_num_wrapper("--pepper_min_mapq", "deep_pepperminmapq", 5, "Minimum mapping quality for read to be considered valid. (Default: 5)"),
    par_num_wrapper("--pepper_min_snp_baseq", "deep_pepperminsnpbaseq", 0, "Minimum base quality for base to be considered valid for SNP."),
    par_num_wrapper("--pepper_min_indel_baseq", "deep_pepperminindelbaseq", 0, "Minimum base quality for base to be considered valid for INDELs."),
    par_numfloat_wrapper("--pepper_snp_frequency", "deep_peppersnpfrequency", 0, 0.1, "Minimum SNP frequency for a site to be considered to have a variant."),
    par_numfloat_wrapper("--pepper_insert_frequency", "deep_pepperinsertfrequency", 0, 0.1, "Minimum insert frequency for a site to be considered to have a variant."),
    par_numfloat_wrapper("--pepper_delete_frequency", "deep_pepperdeletefrequency", 0, 0.1, "Minimum delete frequency for a site to be considered to have a variant."),
    par_switch_wrapper("--pepper_skip_indels", "deep_pepperskipindels", False, "If set then INDEL calling will be skipped."),
    ui.h3("DeepVariant parameters"),
    par_num_wrapper("--dv_min_mapping_quality", "deep_dvminmappingquality", 0, "DeepVariant minimum mapping quality."),
    par_num_wrapper("--dv_min_base_quality", "deep_dvminbasequality", 0, "DeepVariant minimum base quality."),
    advp("deep_advp","DeepVariant Manual","https://github.com/kishwarshafin/pepper/blob/r0.8/docs/usage/usage_and_parameters.md"),
    )

def param_ann():
    return ui.TagList(
        par_num_switch_wrapper("-SVinputInfo", "ann_svinputinfo", True, "To extract the additional SV input fields and insert the data in the outputfile Values: 1 (default) or 0"),
        par_sel_wrapper("-annotationMode", "ann_annotationmode", "both", ["both", "full", "split"], "Description of the types of lines produced by AnnotSV Values: both (default), full or split"),
        par_sel_wrapper("-tx", "ann_tx", "RefSeq", ["RefSeq", "ENSEMBL"], "Origin of the transcripts (RefSeq or ENSEMBL) Values: RefSeq (default) or ENSEMBL"),
        par_num_wrapper("-SVminSize", "ann_svminsize", 50, "SV minimum size (in bp) AnnotSV does not annotate small deletion, insertion and duplication from a VCF input file. Default = 50"),
        advp("ann_advp","annotSV Manual:", "https://lbgi.fr/AnnotSV/Documentation/README.AnnotSV_latest.pdf"),
    )

def param_vep():
    return ui.TagList(
        par_switchvar_wrapper("--everything", "vep_everything", True, "Shortcut flag to switch on all of the following: --sift b, --polyphen b, --ccds, --hgvs, --symbol, --numbers, --domains, --regulatory, --canonical, --protein, --biotype, --af, --af_1kg, --af_esp, --af_gnomade, --af_gnomadg, --max_af, --pubmed, --uniprot, --mane, --tsl, --appris, --variant_class, --gene_phenotype, --mirna. If False, manually enter the flags related to the databases of interest in the advanced options."),
        par_sel_wrapper("--cache/--database", "vep_cache", "--database", ["--database", "--cache"], "Cache: Enables use of the cache. Manually add --refseq or --merged in advanced options to use the refseq or merged cache, (if installed)./Database: Enable VEP to use local or remote databases."),
        #par_switch_wrapper("--cache", "vep_cache", False, "Enables use of the cache. Manually add --refseq or --merged in advanced options to use the refseq or merged cache, (if installed). "),
        ui.panel_conditional("input.vep_cache.indexOf('--cache') > -1", 
                             par_datapath_wrapper("--dir_cache", "vep_dir_cache", "text_vep_dircache_dtpt", "Specify the cache directory to use. Default = '$HOME/.vep/'"),
                             par_switchvar_wrapper("--offline","vep_offline", True ,"Enable offline mode. No database connections will be made, and a cache file or GFF/GTF file is required for annotation. Add --refseq to use the refseq cache (if installed).")),
        par_switch_wrapper("--coding_only", "vep_codingonly", False, "Only return consequences that fall in the coding regions of transcripts. Not used by default"),
        par_switch_wrapper("--no_intergenic", "vep_nointergenic", False, "Do not include intergenic consequences in the output. Not used by default"),
        advp("vep_advp","VEP Manual:", "https://www.ensembl.org/info/docs/tools/vep/script/vep_options.html#opt_genomes"),
    )

#UI-SIDE ETC ETC: