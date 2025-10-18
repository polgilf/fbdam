
### 1) Create & activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS (bash)**

```bash
python -m venv .venv
source .venv/bin/activate
```

If PowerShell complains about execution policy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2) Install in editable mode

pip install -e .[appsi_highs]
