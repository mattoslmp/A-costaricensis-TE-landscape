#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate a publication-quality repeat landscape from a curated in silico
transposable-element table containing genome fraction and K2P values.

Outputs: PNG, TIFF (LZW), SVG, PDF, and a summary CSV.
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy.ndimage import gaussian_filter1d


def parse_args():
  parser = argparse.ArgumentParser(
    description="Generate a repeat landscape using K2P divergence values."
  )
  parser.add_argument("--excel", required=True, help="Input Excel workbook.")
  parser.add_argument("--sheet", default="A. costaricensis", help="Worksheet name.")
  parser.add_argument(
    "--output-prefix",
    default="A_costaricensis_repeat_landscape",
    help="Output path and filename prefix."
  )
  parser.add_argument("--max-k2p", type=float, default=40.0)
  parser.add_argument("--bin-width", type=float, default=1.0)
  parser.add_argument("--smooth-sigma", type=float, default=1.0)
  parser.add_argument("--dpi", type=int, default=600)
  return parser.parse_args()


def parse_percent(value):
  if pd.isna(value):
    return np.nan
  text = str(value).strip().replace("%", "").replace(",", ".")
  try:
    return float(text)
  except ValueError:
    return np.nan


def read_te_table(excel_path, sheet_name):
  excel_path = Path(excel_path)
  if not excel_path.exists():
    raise FileNotFoundError(f"Input file not found: {excel_path}")

  raw = pd.read_excel(
    excel_path,
    sheet_name=sheet_name,
    header=None,
    engine="openpyxl"
  )

  if raw.shape[1] < 6:
    raise ValueError("The TE table must contain at least six columns.")

  data = raw.iloc[2:, 0:6].copy()
  data.columns = [
    "Family",
    "Classification",
    "Copies",
    "Genome_nts",
    "Genome_fraction",
    "K2P"
  ]

  data = data[data["Family"].notna()].copy()
  data["Family"] = data["Family"].astype(str).str.strip()
  data["Classification"] = data["Classification"].astype(str).str.strip()
  data["Copies"] = pd.to_numeric(data["Copies"], errors="coerce")
  data["Genome_nts"] = pd.to_numeric(data["Genome_nts"], errors="coerce")
  data["Genome_fraction"] = data["Genome_fraction"].apply(parse_percent)
  data["K2P"] = pd.to_numeric(
    data["K2P"].astype(str).str.replace(",", ".", regex=False),
    errors="coerce"
  )

  data = data.dropna(
    subset=["Classification", "Genome_fraction", "K2P"]
  ).copy()
  data = data[(data["Genome_fraction"] >= 0) & (data["K2P"] >= 0)].copy()

  if data.empty:
    raise ValueError("No valid TE records were found in the input table.")
  return data


def build_binned_matrix(data, max_k2p, bin_width):
  bins = np.arange(0, max_k2p + bin_width, bin_width)
  centers = (bins[:-1] + bins[1:]) / 2

  class_order = (
    data.groupby("Classification")["Genome_fraction"]
      .sum()
      .sort_values(ascending=False)
      .index
      .tolist()
  )

  matrix = np.zeros((len(class_order), len(centers)), dtype=float)
  for row_index, te_class in enumerate(class_order):
    subset = data[data["Classification"] == te_class]
    bin_indices = np.digitize(subset["K2P"].to_numpy(), bins) - 1
    for genome_fraction, bin_index in zip(
      subset["Genome_fraction"].to_numpy(),
      bin_indices
    ):
      if 0 <= bin_index < len(centers):
        matrix[row_index, bin_index] += genome_fraction

  return matrix, centers, class_order


def smooth_matrix(matrix, sigma):
  if sigma <= 0:
    return matrix.copy()
  return np.asarray([
    gaussian_filter1d(row, sigma=sigma, mode="nearest")
    for row in matrix
  ])


def get_colors(class_order):
  preferred = {
    "LINE/RTE-RTE": "#0B6EBD",
    "LINE/Penelope": "#F28E2B",
    "LTR/Unknown": "#2CA02C",
    "DNA/TcMar-Mariner": "#D62728",
    "LTR/Pao": "#9467BD",
    "DNA/PiggyBac": "#8C564B",
    "LINE/RTE-BovB": "#E377C2",
    "LTR/Gypsy": "#7F7F7F",
    "Retroposon/RTE-derived": "#BCBD22",
    "DNA/TcMar-Tc1": "#17BECF",
    "LTR/Copia": "#4E79A7",
    "LINE/L1": "#EDC948"
  }
  fallback = list(plt.get_cmap("tab20").colors)
  colors = []
  fallback_index = 0
  for te_class in class_order:
    if te_class in preferred:
      colors.append(preferred[te_class])
    else:
      colors.append(fallback[fallback_index % len(fallback)])
      fallback_index += 1
  return colors


def save_tiff_from_png(png_path, tiff_path, dpi):
  with Image.open(png_path) as image:
    if image.mode not in ("RGB", "RGBA"):
      image = image.convert("RGB")
    if image.mode == "RGBA":
      background = Image.new("RGB", image.size, "white")
      background.paste(image, mask=image.getchannel("A"))
      image = background
    image.save(
      tiff_path,
      format="TIFF",
      compression="tiff_lzw",
      dpi=(dpi, dpi)
    )


def create_figure(
  centers,
  matrix,
  class_order,
  colors,
  output_prefix,
  max_k2p,
  dpi
):
  plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.linewidth": 1.1,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none"
  })

  fig, ax = plt.subplots(figsize=(13.2, 8.2), constrained_layout=False)
  ax.stackplot(
    centers,
    matrix,
    labels=class_order,
    colors=colors,
    alpha=0.98,
    linewidth=0.30
  )

  ax.set_xlim(0, max_k2p)
  ax.set_ylim(bottom=0)
  ax.set_xlabel("Kimura 2-parameter distance (K2P, %)", fontsize=15, labelpad=10)
  ax.set_ylabel("Genome fraction (%)", fontsize=15, labelpad=10)
  ax.set_xticks(np.arange(0, max_k2p + 1, 5))
  ax.tick_params(axis="both", which="major", labelsize=11, width=1.0, length=5)
  ax.grid(
    axis="both",
    linestyle=(0, (3, 3)),
    linewidth=0.6,
    alpha=0.42
  )
  ax.set_axisbelow(True)
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)

  fig.suptitle(
    "Repeat landscape of transposable elements",
    fontsize=20,
    fontweight="bold",
    y=0.98
  )
  ax.set_title(
    r"$\it{Angiostrongylus\ costaricensis}$",
    fontsize=17,
    pad=14
  )

  legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.015, 1.0),
    frameon=False,
    fontsize=10.2,
    handlelength=2.6,
    labelspacing=0.72,
    borderaxespad=0
  )
  for text in legend.get_texts():
    text.set_fontsize(10.2)

  plt.subplots_adjust(left=0.10, right=0.73, top=0.86, bottom=0.13)

  output_prefix = Path(output_prefix)
  output_prefix.parent.mkdir(parents=True, exist_ok=True)
  png_path = output_prefix.with_suffix(".png")
  tiff_path = output_prefix.with_suffix(".tiff")
  svg_path = output_prefix.with_suffix(".svg")
  pdf_path = output_prefix.with_suffix(".pdf")

  fig.savefig(png_path, dpi=dpi, bbox_inches="tight", facecolor="white")
  fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
  fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
  plt.close(fig)
  save_tiff_from_png(png_path, tiff_path, dpi)

  return png_path, tiff_path, svg_path, pdf_path


def save_summary(data, output_prefix):
  summary = (
    data.groupby("Classification", as_index=False)
      .agg(
        Families=("Family", "count"),
        Total_copies=("Copies", "sum"),
        Total_genome_nts=("Genome_nts", "sum"),
        Genome_fraction_percent=("Genome_fraction", "sum"),
        Mean_K2P=("K2P", "mean"),
        Min_K2P=("K2P", "min"),
        Max_K2P=("K2P", "max")
      )
      .sort_values("Genome_fraction_percent", ascending=False)
  )
  csv_path = Path(f"{output_prefix}_summary.csv")
  summary.to_csv(csv_path, index=False)
  return csv_path


def main():
  args = parse_args()
  try:
    data = read_te_table(args.excel, args.sheet)
    matrix, centers, class_order = build_binned_matrix(
      data,
      args.max_k2p,
      args.bin_width
    )
    matrix = smooth_matrix(matrix, args.smooth_sigma)
    colors = get_colors(class_order)
    outputs = create_figure(
      centers,
      matrix,
      class_order,
      colors,
      args.output_prefix,
      args.max_k2p,
      args.dpi
    )
    summary = save_summary(data, args.output_prefix)
    for output in outputs:
      print(output)
    print(summary)
  except Exception as error:
    print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()
