from shiny import App, ui, render, reactive
import shinyswatch
import ruamel.yaml
from ui_utils import insdatapath, condgo
from ui_toolparameters import param_nangen
from ui_pipelines import pipe_nangen
import server_utils
from server_launch import launch_gonangen

yaml = ruamel.yaml.YAML()

#CREATE LISTS
platforms=["","Nanopore","Illumina"]
reference=["","GRCh37/hg19","GRCh38/hg38"]
pipeline=["","Genomics","Transcriptomics", "Epigenomics"]
svnano=["SVIM","Sniffles2","cuteSV","Gasoline"]
snvnano=["Longshot","NanoCaller","Clair3","DeepVariant"]


#SHINY UI
app_ui = ui.page_fluid(
    #shinyswatch.theme.darkly(), #general theme
    ui.navset_pill_list(
        #STARTING UI PAGE
        ui.nav("Start", ui.h1("Initial Setup"), ui.hr(),
               ui.row(ui.column(9,ui.input_selectize("plat","Choose your Sequencing Platform: ", choices = platforms, selected = "Nanopore")),
                      ui.column(3, ui.input_numeric("threads_num", "Choose how many cores to use (30 max):", value=1, min=1, max=50))),
            ui.input_selectize("ref","Choose your Reference Version: ", choices = reference, selected = "GRCh37/hg19"),
            ui.panel_conditional("input.ref == 'GRCh37/hg19'",
            ui.row(ui.column(4, "Select the reference Datapath (needed only once for hg19 and hg38):"), ui.column(2, ui.input_action_button("ref_path_19", "Reference datapath")), ui.column(2,"Reference Genome stored in: "), ui.column(4, ui.output_text_verbatim("text_ref19_dtpt")))), #GRCh37/hg19
            ui.panel_conditional("input.ref == 'GRCh38/hg38'",
            ui.row(ui.column(4, "Select the reference Datapath (needed only once for hg19 and hg38):"), ui.column(2, ui.input_action_button("ref_path_38", "Reference datapath")), ui.column(2,"Reference Genome stored in: "), ui.column(4, ui.output_text_verbatim("text_ref38_dtpt")))), #GRCh38/hg38
            ui.input_selectize("pipe","Choose your Analysis: ", choices = pipeline, selected = "Genomics"), #Genomics
            "Do you have more than one sample?",
            ui.input_checkbox("sampsize","Yes", value = False, width = "100%")
        ),
        #PIPELINE DEFINITION UI PAGE
        ui.nav("Pipeline", ui.h1("Pipeline Definition"), ui.hr(),
               pipe_nangen("input.plat", "input.pipe", "input.plat == 'Nanopore' && input.pipe == 'Genomics'", svnano, snvnano),
               ),
        #TOOL PARAMETERS CUSTOMIZATION UI PAGE
        ui.nav("Parameters", ui.h1("Pipeline Customization"), ui.hr(),
               param_nangen(),
               ),
        #PIPELINE LAUNCH UI PAGE
        ui.nav("Launch", ui.h1("Final Settings"), ui.hr(),
               ui.panel_conditional("input.sampsize == 0",
                                    insdatapath("Select your input file:", "up_file", "text_in_dtpt","singcst_name_check", "input.singcst_name_check == 1", 
                                                "singcst_name", "custom_file_name")
                                                ),
               ui.panel_conditional("input.sampsize == 1",
                                    insdatapath("Select your input files:", "up_mul_file", "text_mul_in_dtpt", "mulcst_name_check", "input.mulcst_name_check == 1",
                                                "mulcst_name", "custom_file_name1, custom_name_file2, ...")
                                                ),
               ui.row(ui.column(4,"Select your working directory:"), ui.column(2, ui.input_action_button("wrk_dir", "Select Directory")), ui.column(2,"Working folder in: "), ui.column(4, ui.output_text_verbatim("text_dir_dtpt"))),
               ui.hr(),
        #DIFFERENT LAUNCH BUTTONS FOR THE VARIOUS PIPELINES
               condgo("input.plat", "input.pipe", "input.plat == 'Nanopore' && input.pipe == 'Genomics'", "go_nangen"),
               condgo("input.plat", "input.pipe", "input.plat == 'Nanopore' && input.pipe == 'Transcriptomics'", "go_nantrs"),
               condgo("input.plat", "input.pipe", "input.plat == 'Nanopore' && input.pipe == 'Epigenomics'", "go_nanepi"),
               condgo("input.plat", "input.pipe", "input.plat == 'Illumina' && input.pipe == 'Genomics'", "go_illgen"),
               condgo("input.plat", "input.pipe", "input.plat == 'Illumina' && input.pipe == 'Transcriptomics'", "go_illtrs"),
               condgo("input.plat", "input.pipe", "input.plat == 'Illumina' && input.pipe == 'Epigenomics'", "go_illepi"),
        ),
        widths = (1,11),
        id = "tabswitch"
    )
)


#SHINY SERVER
def server(input, output, session):

    #USEFUL REACTIVES AND GLOBAL VARIABLES
    with open('/data2/mbaragli/python_app/app_python/config_def.yaml') as fp:
        data = yaml.load(fp)
    hg19_path = reactive.Value(data["ref_hg19_path"])
    hg38_path = reactive.Value(data["ref_hg38_path"])
    in_path = reactive.Value("")
    workdir = reactive.Value("")
    gas_som_path = reactive.Value("")
    gas_bed_path = reactive.Value("")
    nanoc_bed_path = reactive.Value("")
    clair3_mod_path = reactive.Value("")
    clair3_bed_path = reactive.Value("")
    vep_cache_path = reactive.Value("")
    cnct_bttn = reactive.Value(None)
    tmp_IP = reactive.Value("")
    tmp_user = reactive.Value("")
    
    #WARNING IF IN STARTING PAGE SOMETHING IS NOT SELECTED or IF THE REFERENCE FILE IS NOT SPECIFIED
    @reactive.Effect
    @reactive.event(input.tabswitch, ignore_init = True)
    def warnfill():
        server_utils.warnfill(input.tabswitch(), input.plat(), input.pipe(), input.ref(), hg19_path, hg38_path)
        
    #MUTUAL EXCLUSION IN THE SELECTION OF MINIMAP (IN_FILE = .fastq) OR SAM->BAM CONVERSION (IN_FILE = .sam)
    @reactive.Effect
    @reactive.event(input.DORADO, input.ALNANO, input.SAMBAM) #input.MULINP
    def reset_sambam_minmap():
        server_utils.reset_sambam_minmap(input.DORADO(), input.ALNANO(), input.SAMBAM())
      
    #ANNOTATION-VARIANT CALLING TOOLS MUTUAL CONNECTION and ONLY ANNOTATION OPERATION RESET
    @reactive.Effect
    @reactive.event(input.SVNANO, input.SNVNANO, input.ANNANO)
    def reset_annosev():
        server_utils.reset_annosev(input.ANNANO(), input.SVNANO(), input.SNVNANO())
       
    #NOTIFICATION IF USER SELECTS BOTH VEP AND ANNOTSV (IN_FILE = .vcf)
    @reactive.Effect
    @reactive.event(input.ONLYANNANO)
    def nodb_tool():
        server_utils.nodb_tool(input.ONLYANNANO())
      
    #SERVER-CONNECTION DIFFERENT BUTTONS
    @reactive.Effect
    @reactive.event(input.ref_path_19)
    def _():
        cnct_bttn.set("connect_ref_path_19")

    @reactive.Effect
    @reactive.event(input.ref_path_38)
    def _():
        cnct_bttn.set("connect_ref_path_38")

    @reactive.Effect
    @reactive.event(input.up_file)
    def _():
        cnct_bttn.set("connect_up_file")

    @reactive.Effect
    @reactive.event(input.wrk_dir)
    def _():
        cnct_bttn.set("connect_wrk_dir")

    @reactive.Effect
    @reactive.event(input.gas_som_ref)
    def _():
        cnct_bttn.set("connect_gas_som_ref")

    @reactive.Effect
    @reactive.event(input.gas_pars_T)
    def _():
        cnct_bttn.set("connect_gas_pars_T")

    @reactive.Effect
    @reactive.event(input.nanoc_bed)
    def _():
        cnct_bttn.set("connect_nanoc_bed")

    @reactive.Effect
    @reactive.event(input.cla3_mod)
    def _():
        cnct_bttn.set("connect_cla3_mod")

    @reactive.Effect
    @reactive.event(input.cla3_bedfn)
    def _():
        cnct_bttn.set("connect_cla3_bedfn")

    @reactive.Effect
    @reactive.event(input.vep_dir_cache)
    def _():
        cnct_bttn.set("connect_vep_cache")

    #SERVER CONNECTION AUTHENTICATOR
    @reactive.Effect
    @reactive.event(cnct_bttn, ignore_init=True, ignore_none=True,)
    def conn_ssh():
        server_utils.conn_ssh(tmp_IP, tmp_user, cnct_bttn)

    #DATAPATH SAVING FUNCTIONS FROM DIFFERENT SERVER BUTTONS
    @reactive.Effect
    @reactive.event(input.connect_ref_path_19)
    def ref19_dtpt():
        server_utils.ref_dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, hg19_path, "ref_hg19_path", data, '/data2/mbaragli/python_app/app_python/config_def.yaml')

    @reactive.Effect
    @reactive.event(input.connect_ref_path_38)
    def ref38_dtpt():
        server_utils.ref_dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, hg38_path, "ref_hg38_path", data, '/data2/mbaragli/python_app/app_python/config_def.yaml')

    @reactive.Effect
    @reactive.event(input.connect_up_file)
    def up_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, in_path)
    
    @reactive.Effect
    @reactive.event(input.connect_wrk_dir)
    def dir_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, workdir)
        
    @reactive.Effect
    @reactive.event(input.connect_gas_som_ref)
    def gassomref_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, gas_som_path)
        
    @reactive.Effect
    @reactive.event(input.connect_gas_pars_T)
    def gasparsT_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, gas_bed_path)
        
    @reactive.Effect
    @reactive.event(input.connect_nanoc_bed)
    def nanocbed_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, nanoc_bed_path)
       
    @reactive.Effect
    @reactive.event(input.connect_cla3_mod)
    def cla3mod_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, clair3_mod_path)
        
    @reactive.Effect
    @reactive.event(input.connect_cla3_bedfn)
    def cla3bedfn_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, clair3_bed_path)

    @reactive.Effect
    @reactive.event(input.connect_vep_cache)
    def vepcache_dtpt():
        server_utils.dtpt(input.ssh(), input.user(), input.password(), tmp_IP, tmp_user, vep_cache_path)
    
    #VERBATIM TEXT OUTPUT FOR SELECTED FILE DATAPATHS
    @render.text
    def text_ref19_dtpt():
        return server_utils.text_dtpt(hg19_path, "WARNING: undefined reference file")
    
    @render.text
    def text_ref38_dtpt():
        return server_utils.text_dtpt(hg38_path, "WARNING: undefined reference file")
     
    @render.text
    def text_in_dtpt():
        return server_utils.text_dtpt(in_path, "Authentication Failed") 
        
    @render.text
    def text_dir_dtpt():
        return server_utils.text_dtpt(workdir, "Authentication Failed")
      
    @render.text
    def text_gassomref_dtpt():
        return server_utils.text_dtpt(gas_som_path, "Authentication Failed")
   
    @render.text
    def text_gasbed_dtpt():
        return server_utils.text_dtpt(gas_bed_path, "Authentication Failed")
     
    @render.text
    def text_nanocbed_dtpt():
        return server_utils.text_dtpt(nanoc_bed_path, "Authentication Failed")
       
    @render.text
    def text_cla3mod_dtpt():
        return server_utils.text_dtpt(clair3_mod_path, "Authentication Failed")
        
    @render.text
    def text_cla3bed_dtpt():
        return server_utils.text_dtpt(clair3_bed_path, "Authentication Failed")
    
    @render.text
    def text_vep_dircache_dtpt():
        return server_utils.text_dtpt(vep_cache_path, "Authentication Failed")
        
    #NANGEN PIPELINE CORE LAUNCH BUTTON
    @reactive.Effect
    @reactive.event(input.go_nangen)
    def gonangen():
        launch_gonangen(data, workdir, in_path, input.threads_num(), input.sampsize(), input.ref(), hg19_path, hg38_path, svnano, snvnano,
                    input.up_mul_file(), input.mulcst_name_check(), input.mulcst_name(), input.singcst_name_check(), input.singcst_name(),
                    input.DORADO(), input.ALNANO(), input.SAMBAM(), input.SRTBAM(), input.IDXBAM(), input.ANNANO(), input.ONLYANNANO(), input.SVNANO(), input.SNVNANO(), 
                    input.def_dorado(), input.def_alnano(), input.def_sambam(), input.def_srtbam(), input.def_idxbam(), input.def_svim(), input.def_snif(), input.def_cut(), input.def_gas(), input.def_long(), input.def_nanoc(), input.def_cla3(), input.def_deep(), input.def_ann(), input.def_vep(),
                    input.alnano_advp(), input.sambam_advp(), input.srtbam_advp(), input.idxbam_advp(),
                    input.dorado_model(), input.dorado_device(), input.dorado_modifiedbases(), input.dorado_advp(),
                    input.svim_minmapq(), input.svim_minsvsize(), input.svim_maxsvsize(), input.svim_skipgenotyping(), input.svim_minimumscore(), input.svim_minimumdepth(), input.svim_advp(),
                    input.snif_phase(), input.snif_minsupport(), input.snif_minsvlen(), input.snif_mapq(), input.snif_noqc(), input.snif_advp(),
                    input.cut_minmapq(), input.cut_minreadlen(), input.cut_minsupport(), input.cut_minsize(), input.cut_maxsize(), input.cut_genotype(), input.cut_advp(),
                    input.gas_som_check(), gas_som_path, gas_bed_path, input.gas_pars_Q(), input.gas_germ_NS(), input.gas_germ_Q(), input.gas_germ_MS(), input.gas_germ_OT(), input.gas_germ_vcf_TS(), input.gas_germ_vcf_TC(), input.gas_germ_vcf_TI(), input.gas_germ_vcf_TO(), 
                    input.gas_som_NS(), input.gas_som_Q(), input.gas_som_MS(), input.gas_som_OV(), input.gas_som_vcf_TS(), input.gas_som_vcf_TC(), input.gas_som_vcf_TI(), input.gas_som_vcf_TO(), input.gas_som_vcf_TR(), input.gas_som_vcf_TP(), input.gas_som_vcf_TH(),
                    input.long_region(), input.long_mincov(), input.long_maxcov(), input.long_minmapq(), input.long_minaltcount(), input.long_minaltfrac(), input.long_advp(),
                    input.nanoc_mode(), input.nanoc_mincov(), input.nanoc_maxcov(), nanoc_bed_path, input.nanoc_phase(), input.nanoc_advp(),
                    input.cla3_callsnponly(), clair3_mod_path, clair3_bed_path, input.cla3_qual(), input.cla3_snpminaf(), input.cla3_indelminaf(), input.cla3_minmq(), input.cla3_advp(),
                    input.deep_region(), input.deep_pepperminmapq(), input.deep_pepperminsnpbaseq(), input.deep_pepperminindelbaseq(), input.deep_peppersnpfrequency(), input.deep_pepperinsertfrequency(), input.deep_pepperdeletefrequency(), 
                    input.deep_pepperskipindels(), input.deep_dvminmappingquality(), input.deep_dvminbasequality(), input.deep_advp(),
                    input.ann_svinputinfo(), input.ann_annotationmode(), input.ann_tx(), input.ann_svminsize(), input.ann_advp(),
                    input.vep_cache(), vep_cache_path, input.vep_everything(), input.vep_codingonly(), input.vep_nointergenic(), input.vep_offline(), input.vep_advp(),
                    )

    @output
    @render.text
    def t_alnano():
        if input.ALNANO() == 1:
            return f"Alignment will be performed with minimap2"
        else:
            return f" --- "
        
    @output
    @render.text
    def t_dorado():
        if input.DORADO() == 1:
            return f"Base Calling will be performed with Dorado"
        else:
            return f" --- "
        
    @output
    @render.text
    def t_blank():
            return f" --- "
    


#Shiny APP
app = App(app_ui, server)

#### CSS STYLE: https://www.w3schools.com/css/default.asp