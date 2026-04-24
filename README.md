# lnc_mRNA_analysis

Identification of mRNA isoforms with long non-coding RNA (lncRNA) properties in *Arabidopsis thaliana*.

This repository contains the analysis notebooks, results, and figures accompanying the EmpiAS paper, which identifies 2,016 candidate mRNA isoforms that behave as nuclear-retained, NMD-insensitive, non-translated lncRNAs. The statistical framework used to detect differential isoform usage from long-read (ONT) data is the companion package [EmpiAS](https://github.com/Lucas-Servi/Empirical_stats_AS).

## Repository contents

### Notebooks

- `lnc_RNA_filtering.ipynb` — Original analysis notebook. Loads SALMON quantifications (Illumina NMD + ONT fractionation + polyribosome data), applies the 4-criterion filter (not translated / not NMD-sensitive / nuclear-enriched / stable), and produces the initial candidate list.
- `New_analysis.ipynb` — Updated workflow with additional biological replicates for the NMD dataset. Generates the final 2,016-candidate list (`data/candidates_lncRNA_mRNA.csv`) and all paper figures.

### `data/`

Quantification matrices and analysis results used by the notebooks:

| File | Description |
|------|-------------|
| `AtRTDv2_1.csv` | Isoform-to-gene mapping from the AtRTDv2.1 reference (54,095 isoforms) |
| `AtRTDv2_1_QUASI.LS.parquet` | Same mapping in Parquet format for faster loading |
| `candidates_lncRNA_mRNA.csv` | **Primary result:** 2,016 candidate lncRNA-mRNA isoforms |
| `pval_ONT_nuc_L_O.csv` | EmpiAS p-values for ONT Nuclear (Light) vs cytoplasm/other |
| `pval_table_Chx_Mock.csv` | EmpiAS p-values for cycloheximide vs mock-treated Illumina |
| `pval_table_upf1_wt.csv` | EmpiAS p-values for UPF1 knockout vs wild-type |
| `pval_table_upf3_wt.csv` | EmpiAS p-values for UPF3 knockout vs wild-type |
| `pval_table_upf1upf3_wt.csv` | EmpiAS p-values for UPF1/UPF3 double KO vs wild-type |
| `GO_enrichment_candidates.csv` | GO term enrichment results for the candidate set |
| `Supplementary_Table_S1.csv` | Supplementary table referenced in the paper |

### `Figures/`

The 11 paper figures (Figs 1–11). Figures 1 and 2 (`Nuclear_NMD_Polyribosomes.png`, `NMD_and_polyribosome.png`) were regenerated with English labels.

### `utils.py`

Helper for concatenating SALMON `quant.sf` files from multiple sample directories and joining them with the reference transcriptome.

## External data required to re-run the GO enrichment step

Two publicly available annotation files are needed (not included in this repo due to size):

```bash
# Gene Ontology (basic, OBO format) — place in data/
wget -O data/go-basic.obo http://purl.obolibrary.org/obo/go/go-basic.obo

# TAIR GO annotation file — place in data/
wget -O data/tair.gaf.gz https://current.geneontology.org/annotations/tair.gaf.gz && gunzip data/tair.gaf.gz
```

## Running the analysis

```bash
# 1. Install the EmpiAS package (companion repo)
pip install -e ../Empirical_stats_AS/

# 2. Install analysis dependencies
pip install pandas numpy scipy matplotlib seaborn plotly jupyter goatools pyarrow

# 3. Run the notebooks
jupyter lab
```

The notebooks expect the upstream SALMON quantification outputs to live at:
`../../lnc_mrna/mapping/salmon/AtRTDv2_1_QUASI/` (see the `paper_doct/lnc_mrna/scripts/` directory for the quantification pipelines).

## Citation

Paper in preparation. Companion mechanistic paper: Rodríguez *et al.*, 2026 — *Alternative splicing of a coding gene produces a nuclear regulatory long non-coding RNA*.
