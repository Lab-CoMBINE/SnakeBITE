from shiny import ui

#UI-SIDE GENERIC FUNCTIONS FOR PIPELINE TAB:

def pipe_row_wrapper(title, tool, txt):
    return ui.TagList(
        ui.row(ui.column(3,title), ui.column(6,ui.input_checkbox(tool, txt, value = False, width = "100%")))
    )

def pipe_info_wrapper(txt):
    return ui.TagList(
        ui.row(ui.column(3,""),
               ui.column(6, {"Style": "font-size:12px;font-weight:bold;color:red;font-style:italic;text-align:justified"}, txt)),
    )

def pipe_sidebar_wrapper(title, *rows):
    return ui.TagList(
        ui.layout_sidebar(
            ui.panel_sidebar(
                title,
                width = 2
            ),
            ui.panel_main(
                *rows
            )
        )
    )

def sing_tool_ui(opid, op, lbl_ui, txt_ui="t_blank"):
    return ui.layout_sidebar(
                    ui.panel_sidebar(
                        op,
                        width = 2),
                    ui.panel_main(
                        #{"Style": "font-size:20px;font-weight:underlined;color:blue;font-style:italic"},
                        lbl_ui,
                        ui.input_checkbox(opid, "Yes", value = False, width = "100%"),
                        ui.output_text(txt_ui)
                    )
                )


def mul_tool_ui(opid, op, tool_list,lbl_ui):
    return ui.layout_sidebar(
                    ui.panel_sidebar(
                        op,
                        width = 2
                    ),
                    ui.panel_main(
                        #{"Style": "font-size:20px;font-weight:underlined;color:blue;font-style:italic"},
                        lbl_ui,
                        ui.input_checkbox_group(opid,"", choices = tool_list, width = '100%')
                    )   
                )

#UI-SIDE NANOPORE GENOMICS PIPELINE:
def pipe_nangen(id1, id2, cond, lst1, lst2):
    return ui.TagList(ui.panel_conditional(cond,
                sing_tool_ui("DORADO", "Base Calling", "Do you need to perform Base Calling?", "t_dorado"),
                sing_tool_ui("ALNANO", "Alignment", "Do you need to perform alignment on your reads?", "t_alnano"),
                sing_tool_ui("SAMBAM", "SAM -> BAM", "Do you need to convert SAM to BAM format?"),
                pipe_sidebar_wrapper("Post-alignment configuration", 
                                     #pipe_row_wrapper("Merging", "MULINP", "Do you have more than one input file for your sample?"),
                                     pipe_row_wrapper("Sorting", "SRTBAM", "Do you need to sort your BAM file/s?"), 
                                     pipe_info_wrapper("This step needs to be performed for successive operations."),
                                     pipe_row_wrapper("Indexing", "IDXBAM", "Do you need to index your BAM file/s?"), 
                                     pipe_info_wrapper("This step needs to be performed for successive operations.")),
                mul_tool_ui("SVNANO", "Structural Variant calling", lst1,"Choose one or more tools to perform SV calling: "),
                mul_tool_ui("SNVNANO", "Single Nucleotide Variant calling", lst2, "Choose one or more tools to perform SNV/InDel calling: "),
                pipe_sidebar_wrapper("Annotation configuration",
                     pipe_row_wrapper("Annotation", "ANNANO", "Do you need to perform annotation of variants?"),
                     ui.panel_conditional("input.ANNANO == 1 && input.SVNANO.length == 0 && input.SNVNANO.length == 0", 
                                          ui.row(
                                              ui.column(3,"For Annotation only:"), 
                                              ui.column(9, ui.input_checkbox_group("ONLYANNANO", "Select a tool for variant annotation", choices = ["AnnotSV", "VEP"], selected=None, width = '100%')
                                                        ),
                                            ),
                                          pipe_info_wrapper("Use annotSV for Structural Variants and VEP for Single Nucleotide Variants only"),
                                          ),
                    ),
                ),
    )
