# 📘 FBDAM — Catálogos y esquemas de configuración
### Uso y validación de los YAMLs de `src/fbdam/config/`

---

## 🧩 1. ¿Qué son los catálogos?
Los **catálogos** (`constraints_v1.1.yaml`, `objectives_v1.0.yaml`) definen bloques **reutilizables y versionados** del modelo:
restricciones y objetivos que luego se combinan en los **escenarios**.

Cada bloque incluye:
- `id`: identificador estable (`snake_case`) y equivalente al nombre registrado en código.
- `params`: parámetros configurables
- `description`: explicación semántica
- `uri` (opcional): enlace a una ontología o documento de referencia

---

## 🧭 2. Esquemas de validación
Los archivos en `schema/` (`constraints_schema.yaml`, `objectives_schema.yaml`) son **esquemas JSON Schema** expresados en YAML.  
Permiten validar automáticamente los catálogos con herramientas estándar:

```bash
pip install jsonschema
jsonschema -i src/fbdam/config/catalogs/constraints_v1.1.yaml src/fbdam/config/schema/constraints_schema.yaml
```

También puedes cargar y validar desde Python:

```python
from jsonschema import validate
import yaml

schema = yaml.safe_load(open('src/fbdam/config/schema/constraints_schema.yaml'))
data = yaml.safe_load(open('src/fbdam/config/catalogs/constraints_v1.1.yaml'))
validate(instance=data, schema=schema)
```

---

## ⚙️ 3. Cómo se usan dentro de un escenario

Cada **escenario YAML** importa por referencia las piezas del catálogo:

```yaml
model:
  constraints:
    - ref: nutrition_utility_mapping
    - ref: household_adequacy_floor
      override: { use_slack: true }
  objectives:
    - ref: sum_utility
```

El módulo `io.py`:
1. Carga el escenario principal.
2. Busca en los catálogos los bloques con `ref`.
3. Aplica `override` si hay parámetros personalizados.
4. Devuelve una estructura consolidada al *model builder*.

---

## 🔄 4. Cómo versionar catálogos

Cada catálogo incluye:
```yaml
version: v1.0
status: validated
maintainer: pol_gil
```
- **version:** sigue formato `vX.Y`
- **status:** `draft | validated | archived`
- **maintainer:** autor o responsable

Cuando cambies la lógica (no solo texto):
- crea `constraints_v1.2.yaml` o `objectives_v1.1.yaml`
- cambia `status: draft`
- documenta el cambio en el control de versiones WISER

---

## 🧱 5. Ejemplo rápido: añadir una restricción nueva

Supón que creas una nueva función en `constraints.py`:

```python
@register_constraint("household_adequacy_floor")
def add_household_floor(m, params):
    U_floor = float(params.get("U_floor", 0.85))
    def rule(m,h): return sum(m.u[n,h] for n in m.N) >= len(m.N) * U_floor
    m.HHFloor = pyo.Constraint(m.H, rule=rule)
```

Entonces en el catálogo:

```yaml
constraints:
  - id: household_adequacy_floor
    description: "Minimum average utility per household"
    params: { U_floor: 0.85 }
```

Y en un escenario, podrías modificarlo:

```yaml
- ref: household_adequacy_floor
  override: { U_floor: 0.90 }
```

---

## ✅ 6. Buenas prácticas
- Usa **IDs estables** y descriptivos (`snake_case`).
- No elimines versiones previas: **archívalas**.
- Valida siempre los catálogos antes de ejecutar el modelo.
- Documenta los cambios en el **governance log** (WISER).

---

## 🗂️ Estructura de referencia
```
src/
└─ fbdam/
   └─ config/
      ├─ catalogs/
      │  ├─ constraints_v1.1.yaml
      │  └─ objectives_v1.0.yaml
      └─ schema/
         ├─ constraints_schema.yaml
         └─ objectives_schema.yaml
```
