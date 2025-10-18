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

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=(python3)
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=(python)
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=(py -3)
else
  echo "❌ Python interpreter not found. Please install Python 3.8+ and ensure it is on your PATH."
  exit 1
fi

echo "🔧 Creating virtual environment..."
"${PYTHON_CMD[@]}" -m venv "$VENV_NAME"

# Activate venv
source $VENV_NAME/bin/activate

echo "✅ Virtual environment activated: $VENV_NAME"

echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "📚 Installing project (editable) and extras..."
# installs your package + appsi_highs + Jupyter + ipykernel
pip install -e .[appsi_highs] jupyter ipykernel

echo "🧠 Registering Jupyter kernel..."
"${PYTHON_CMD[@]}" -m ipykernel install --user --name="$KERNEL_NAME" --display-name="$DISPLAY_NAME"
