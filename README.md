# *Angiostrongylus costaricensis* transposable-element landscape

This repository contains the source data and reproducible Python scripts used to generate the transposable-element repeat landscape and workflow figures for the manuscript **“First description of transposable elements of *Angiostrongylus costaricensis* – the causative agent of abdominal angiostrongyliasis in humans.”**

## Repository structure

```text
A-costaricensis-TE-landscape/
├── README.md
├── CITATION.cff
├── requirements.txt
├── scripts/
│   ├── plot_te_landscape.py
│   └── draw_te_workflow.py
├── data/
│   └── Descricao_das_familias.xlsx
└── figures/
    ├── Figure_1_repeat_landscape.png
    ├── Figure_1_repeat_landscape.svg
    ├── Figure_2_TE_workflow.png
    └── Figure_2_TE_workflow.svg
```

## Contents

- `scripts/plot_te_landscape.py`: reads the curated spreadsheet, aggregates confirmed transposable-element families by Kimura 2-parameter distance (K2P), and exports the repeat landscape.
- `scripts/draw_te_workflow.py`: generates the publication-quality workflow diagram.
- `data/Descricao_das_familias.xlsx`: source table containing the TE-family classification, copy number, genomic coverage, genome fraction, and K2P values.
- `figures/`: publication figures in high-resolution PNG and editable SVG formats.

## Installation

Python 3.9 or newer is recommended.

```bash
python3 -m venv te_figures_env
source te_figures_env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.\te_figures_env\Scripts\Activate.ps1
```

## Generate the repeat landscape

From the repository root, run:

```bash
python3 scripts/plot_te_landscape.py \
  --excel data/Descricao_das_familias.xlsx \
  --sheet "A. costaricensis" \
  --output-prefix figures/Figure_1_repeat_landscape
```

The script exports PNG, TIFF, SVG, PDF, and a summary CSV file.

## Generate the workflow

```bash
python3 scripts/draw_te_workflow.py \
  --output-prefix figures/Figure_2_TE_workflow
```

The script exports PNG, TIFF, SVG, and PDF files.

## Citation

Please cite this repository as:

> Pereira, L. de M. (2026). *A. costaricensis transposable-element landscape: scripts, source data and publication figures*. GitHub repository. https://github.com/mattoslmp/A-costaricensis-TE-landscape

Citation metadata are also available in `CITATION.cff`.

## Author and contact

**Leandro de Mattos Pereira**  
Databiomics, Bioinformatics and Data Science Laboratory, WBPEREIRA  
Itaperuna, Rio de Janeiro, Brazil  
GitHub: [@mattoslmp](https://github.com/mattoslmp)
