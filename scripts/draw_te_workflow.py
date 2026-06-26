#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
draw_te_workflow.py

Gera uma figura vetorial de alta qualidade do workflow de identificação,
classificação, curadoria e análise de elementos transponíveis em
Angiostrongylus costaricensis.

Saídas:
  - PNG em alta resolução
  - TIFF em alta resolução com compressão LZW
  - SVG vetorial
  - PDF vetorial

Exemplo:
  python3 draw_te_workflow.py \
    --output-prefix "A_costaricensis_TE_workflow"

Dependências:
  pip install matplotlib pillow
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import (
  Circle,
  FancyArrowPatch,
  FancyBboxPatch
)
from PIL import Image


def parse_args():
  parser = argparse.ArgumentParser(
    description="Gera um workflow publicável para análise de TEs."
  )
  parser.add_argument(
    "--output-prefix",
    default="A_costaricensis_TE_workflow",
    help="Prefixo dos arquivos de saída."
  )
  parser.add_argument(
    "--dpi",
    type=int,
    default=600,
    help="Resolução do PNG e TIFF."
  )
  return parser.parse_args()


def add_round_box(
  ax,
  x,
  y,
  width,
  height,
  number,
  title,
  subtitle=None,
  edgecolor="#527DB8",
  facecolor="#F6FAFF",
  number_color="#103B73",
  title_color="#102A54",
  subtitle_color="#334E73",
  title_size=13.0,
  subtitle_size=10.2
):
  box = FancyBboxPatch(
    (x, y),
    width,
    height,
    boxstyle="round,pad=0.012,rounding_size=0.015",
    linewidth=1.35,
    edgecolor=edgecolor,
    facecolor=facecolor
  )
  ax.add_patch(box)

  circle_radius = height * 0.25
  circle_x = x + 0.043
  circle_y = y + height / 2

  number_circle = Circle(
    (circle_x, circle_y),
    circle_radius,
    facecolor=number_color,
    edgecolor=number_color,
    linewidth=1.0
  )
  ax.add_patch(number_circle)

  ax.text(
    circle_x,
    circle_y,
    str(number),
    ha="center",
    va="center",
    fontsize=10.5,
    color="white",
    fontweight="bold"
  )

  text_x = x + 0.093

  if subtitle:
    ax.text(
      text_x,
      y + height * 0.65,
      title,
      ha="left",
      va="center",
      fontsize=title_size,
      color=title_color,
      fontweight="bold"
    )

    ax.text(
      text_x,
      y + height * 0.31,
      subtitle,
      ha="left",
      va="center",
      fontsize=subtitle_size,
      color=subtitle_color
    )

  else:
    ax.text(
      text_x,
      y + height / 2,
      title,
      ha="left",
      va="center",
      fontsize=title_size,
      color=title_color,
      fontweight="bold"
    )


def add_arrow(
  ax,
  start,
  end,
  color="#274D7E",
  linewidth=1.6,
  linestyle="-",
  mutation_scale=15
):
  arrow = FancyArrowPatch(
    start,
    end,
    arrowstyle="-|>",
    mutation_scale=mutation_scale,
    linewidth=linewidth,
    linestyle=linestyle,
    color=color,
    shrinkA=0,
    shrinkB=0
  )
  ax.add_patch(arrow)


def save_tiff_from_png(
  png_path,
  tiff_path,
  dpi
):
  with Image.open(png_path) as image:
    if image.mode not in ("RGB", "RGBA"):
      image = image.convert("RGB")

    if image.mode == "RGBA":
      background = Image.new(
        "RGB",
        image.size,
        "white"
      )
      background.paste(
        image,
        mask=image.getchannel("A")
      )
      image = background

    image.save(
      tiff_path,
      format="TIFF",
      compression="tiff_lzw",
      dpi=(dpi, dpi)
    )


def create_workflow(
  output_prefix,
  dpi
):
  print("[1/4] Preparando workflow...", flush=True)

  plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none"
  })

  fig = plt.figure(
    figsize=(13.4, 10.4)
  )

  ax = fig.add_axes(
    [0, 0, 1, 1]
  )

  ax.set_xlim(
    0,
    1
  )

  ax.set_ylim(
    0,
    1
  )

  ax.axis(
    "off"
  )

  dark_blue = "#103B73"
  blue_edge = "#527DB8"
  blue_fill = "#F6FAFF"
  orange = "#E36F3D"
  orange_edge = "#E58B63"
  orange_fill = "#FFF7F2"

  ax.text(
    0.5,
    0.967,
    "Workflow for transposable element annotation and landscape analysis",
    ha="center",
    va="center",
    fontsize=19.5,
    color=dark_blue,
    fontweight="bold"
  )

  ax.text(
    0.5,
    0.932,
    r"$\it{Angiostrongylus\ costaricensis}$",
    ha="center",
    va="center",
    fontsize=16.5,
    color=dark_blue
  )

  main_x = 0.075
  main_w = 0.635
  box_h = 0.066

  y_positions = [
    0.842,
    0.748,
    0.654,
    0.560,
    0.466,
    0.372,
    0.278,
    0.184,
    0.090
  ]

  steps = [
    (
      "1",
      "A. costaricensis genome assembly",
      "Reference assembly: GCA_900624975.1"
    ),
    (
      "2",
      "De novo TE discovery with RepeatModeler2",
      "Recon + RepeatScout + structural discovery of LTR elements"
    ),
    (
      "3",
      "Initial genome mapping with the de novo TE library",
      None
    ),
    (
      "4",
      "TE classification using RepeatClassifier",
      "Comparison with Repbase and Dfam reference libraries"
    ),
    (
      "5",
      "Structural and domain-based refinement",
      "PASTEC + Pfam + GypsyDB"
    ),
    (
      "6",
      "Manual curation of consensus sequences",
      "Removal of non-TE sequences, artifacts, redundancy and unsupported repeats"
    ),
    (
      "7",
      "Genome remapping with the curated TE library",
      "RepeatMasker in sensitive mode (-s)"
    ),
    (
      "8",
      "Estimation of TE family abundance",
      "Copy number, total nucleotide coverage and genome fraction"
    ),
    (
      "9",
      "K2P divergence and repeat landscape analysis",
      "Kimura 2-parameter distance with CpG adjustment"
    )
  ]

  for index, (
    number,
    title,
    subtitle
  ) in enumerate(steps):
    is_final = index >= 7

    add_round_box(
      ax=ax,
      x=main_x,
      y=y_positions[index],
      width=main_w,
      height=box_h,
      number=number,
      title=title,
      subtitle=subtitle,
      edgecolor=(
        orange_edge
        if is_final
        else blue_edge
      ),
      facecolor=(
        orange_fill
        if is_final
        else blue_fill
      ),
      number_color=(
        orange
        if is_final
        else dark_blue
      ),
      title_color=(
        "#3C2418"
        if is_final
        else "#102A54"
      ),
      subtitle_color=(
        "#6A3E2A"
        if is_final
        else "#334E73"
      )
    )

  for index in range(
    len(y_positions) - 1
  ):
    center_x = (
      main_x + main_w / 2
    )

    start_y = y_positions[index]
    end_y = (
      y_positions[index + 1] +
      box_h
    )

    add_arrow(
      ax=ax,
      start=(center_x, start_y),
      end=(center_x, end_y),
      color=dark_blue,
      linewidth=1.5
    )

  optional_x = 0.765
  optional_y = 0.258
  optional_w = 0.195
  optional_h = 0.105

  optional_box = FancyBboxPatch(
    (
      optional_x,
      optional_y
    ),
    optional_w,
    optional_h,
    boxstyle="round,pad=0.012,rounding_size=0.015",
    linewidth=1.4,
    edgecolor=orange_edge,
    facecolor=orange_fill
  )

  ax.add_patch(
    optional_box
  )

  optional_circle = Circle(
    (
      optional_x + 0.035,
      optional_y + optional_h / 2
    ),
    optional_h * 0.18,
    facecolor=orange,
    edgecolor=orange
  )

  ax.add_patch(
    optional_circle
  )

  ax.text(
    optional_x + 0.035,
    optional_y + optional_h / 2,
    "7a",
    ha="center",
    va="center",
    fontsize=10,
    color="white",
    fontweight="bold"
  )

  ax.text(
    optional_x + 0.07,
    optional_y + optional_h * 0.69,
    "BLAST+ screening for",
    ha="left",
    va="center",
    fontsize=11.5,
    color="#4A2A1A",
    fontweight="bold"
  )

  ax.text(
    optional_x + 0.07,
    optional_y + optional_h * 0.47,
    "potential horizontal",
    ha="left",
    va="center",
    fontsize=11.5,
    color="#4A2A1A",
    fontweight="bold"
  )

  ax.text(
    optional_x + 0.07,
    optional_y + optional_h * 0.25,
    "transfer against host genomes",
    ha="left",
    va="center",
    fontsize=10.2,
    color="#6A3E2A"
  )

  ax.text(
    0.727,
    optional_y + optional_h * 0.79,
    "Optional analysis",
    ha="left",
    va="center",
    fontsize=10.5,
    color=orange,
    fontweight="bold"
  )

  add_arrow(
    ax=ax,
    start=(
      main_x + main_w,
      y_positions[6] + box_h / 2
    ),
    end=(
      optional_x,
      optional_y + optional_h / 2
    ),
    color=orange,
    linewidth=1.5,
    linestyle=(0, (4, 3))
  )

  ax.text(
    0.5,
    0.035,
    "Curated TE library → genome masking → abundance estimation → evolutionary age profile",
    ha="center",
    va="center",
    fontsize=11.5,
    color="#425466"
  )

  output_prefix = Path(
    output_prefix
  )

  output_prefix.parent.mkdir(
    parents=True,
    exist_ok=True
  )

  png_path = output_prefix.with_suffix(
    ".png"
  )

  tiff_path = output_prefix.with_suffix(
    ".tiff"
  )

  svg_path = output_prefix.with_suffix(
    ".svg"
  )

  pdf_path = output_prefix.with_suffix(
    ".pdf"
  )

  print("[2/4] Salvando PNG, SVG e PDF...", flush=True)

  fig.savefig(
    png_path,
    dpi=dpi,
    bbox_inches="tight",
    facecolor="white",
    edgecolor="none"
  )

  fig.savefig(
    svg_path,
    bbox_inches="tight",
    facecolor="white",
    edgecolor="none"
  )

  fig.savefig(
    pdf_path,
    bbox_inches="tight",
    facecolor="white",
    edgecolor="none"
  )

  plt.close(
    fig
  )

  print("[3/4] Convertendo PNG para TIFF LZW...", flush=True)

  save_tiff_from_png(
    png_path=png_path,
    tiff_path=tiff_path,
    dpi=dpi
  )

  print("[4/4] Concluído.", flush=True)
  print(f"      PNG:  {png_path}", flush=True)
  print(f"      TIFF: {tiff_path}", flush=True)
  print(f"      SVG:  {svg_path}", flush=True)
  print(f"      PDF:  {pdf_path}", flush=True)


def main():
  args = parse_args()

  try:
    create_workflow(
      output_prefix=args.output_prefix,
      dpi=args.dpi
    )

  except Exception as error:
    print(
      f"\nERRO: {error}",
      file=sys.stderr,
      flush=True
    )
    sys.exit(1)


if __name__ == "__main__":
  main()
