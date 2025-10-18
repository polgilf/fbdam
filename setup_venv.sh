#!/usr/bin/env bash
# ============================================================
# FBDAM Experiment Environment Setup Script
# ------------------------------------------------------------
# Creates an isolated Python environment, installs dependencies,
# and registers a Jupyter kernel for interactive use.
# ============================================================

set -e  # stop on first error

# --- CONFIG -------------------------------------------------
VENV_NAME=".venv"
KERNEL_NAME="fbdam-venv"
DISPLAY_NAME="Python (fbdam)"
# ------------------------------------------------------------


echo "🔧 Creating virtual environment..."
python -m venv "$VENV_NAME"

# Activate venv
# source $VENV_NAME/bin/activate

$VENV_NAME\Scripts\Activate.ps1

echo "✅ Virtual environment activated: $VENV_NAME"

echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "📚 Installing project (editable) and extras..."
# installs your package + appsi_highs + Jupyter + ipykernel
pip install -e .[appsi_highs] jupyter ipykernel

echo "🧠 Registering Jupyter kernel..."
"${PYTHON_CMD[@]}" -m ipykernel install --user --name="$KERNEL_NAME" --display-name="$DISPLAY_NAME"
