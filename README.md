# *Angiostrongylus costaricensis* transposable-element landscape

This repository contains the source table and reproducible Python scripts used to generate the transposable-element repeat landscape and workflow figures for the manuscript **“First description of transposable elements of *Angiostrongylus costaricensis* – the causative agent of abdominal angiostrongyliasis in humans.”**

The TE assignments reported here were obtained through an in silico annotation and curation workflow. Accordingly, the repository and figures use the neutral wording **transposable elements** rather than **confirmed transposable elements**.

## Repository structure

```text
A-costaricensis-TE-landscape/
├── README.md
├── CITATION.cff
├── requirements.txt
├── scripts/
│   ├── plot_te_landscape.py
│   └── draw_te_workflow.py
└── data/
    ├── README.md
    ├── A_costaricensis_TE_families.csv
    └── A_costaricensis_TE_families_full.csv
```

## Contents

- `scripts/plot_te_landscape.py`: aggregates the in silico-classified transposable-element families by Kimura 2-parameter distance (K2P) and exports the repeat landscape in PNG, TIFF, SVG and PDF formats.
- `scripts/draw_te_workflow.py`: generates the publication-quality workflow diagram in PNG, TIFF, SVG and PDF formats.
- `data/A_costaricensis_TE_families.csv`: TE families used to build the landscape.
- `data/A_costaricensis_TE_families_full.csv`: complete exported table, including classified TE families and unsupported unknown repeats.

## Installation

Python 3.9 or newer is recommended.

```bash
python3 -m venv te_figures_env
source te_figures_env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.\te_figures_env\Scripts\Activate.ps1
```

## Reconstruct the Excel input

```bash
python3 - <<'PY'
import pandas as pd

source = "data/A_costaricensis_TE_families.csv"
output = "data/Descricao_das_familias.xlsx"
df = pd.read_csv(source)
headers = [
    "Família",
    "Classificação",
    "Nº Cópias",
    "Total de nts no genoma",
    "Fração do genoma",
    "K2P",
]

with pd.ExcelWriter(output, engine="openpyxl") as writer:
    pd.DataFrame([["Consensos classificados como TEs"]]).to_excel(
        writer,
        sheet_name="A. costaricensis",
        index=False,
        header=False,
    )
    df[["Family", "Classification", "Copies", "Genome_nts", "Genome_fraction", "K2P"]].to_excel(
        writer,
        sheet_name="A. costaricensis",
        index=False,
        startrow=1,
        header=headers,
    )

print(f"Created: {output}")
PY
```

## Generate the repeat landscape

```bash
python3 scripts/plot_te_landscape.py \
  --excel data/Descricao_das_familias.xlsx \
  --sheet "A. costaricensis" \
  --output-prefix figures/Figure_1_repeat_landscape
```

## Generate the workflow

```bash
python3 scripts/draw_te_workflow.py \
  --output-prefix figures/Figure_2_TE_workflow
```

## Citation

> Pereira, L. de M. (2026). *A. costaricensis transposable-element landscape: scripts, source data and publication figures*. GitHub repository. https://github.com/mattoslmp/A-costaricensis-TE-landscape

## Author and contact

**Leandro de Mattos Pereira**  
Databiomics, Bioinformatics and Data Science Laboratory, WBPEREIRA  
Itaperuna, Rio de Janeiro, Brazil  
GitHub: [@mattoslmp](https://github.com/mattoslmp)
