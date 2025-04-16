SERVICES = ["clash", "pamnet", "lociparse", "3drnascore",
            "tb-mcq", "barnaba", "cgrnasp",
            "dfire", "mcq", "lcs", "cad_score", "tm-score",
            "lddt", "rasp", "rs-rnasp", "rmsd", "inf",
            "p_value", "di", "gdt-ts", "cad_score", "ares", "rna3dcnn", "rna-briq"]
ALL = SERVICES
ALL_METRICS = ["barnaba", "mcq", "lcs", "cad-score", "tm-score",
           "lddt", "rmsd", "inf", "p-value", "di",
           "gdt-ts", "cad_score", "clash"]
ALL_SF = ["pamnet", "lociparse", "3drnascore",
          "tb-mcq", "barnaba", "cgrnasp", "dfire", "rasp",
          "rs-rnasp", "ares", "rna3dcnn", "rna-briq"]

SERVICES_DICT = {key: {"args": {
    }} for key in SERVICES}