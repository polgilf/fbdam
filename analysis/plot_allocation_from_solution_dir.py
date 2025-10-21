
import sys
from pathlib import Path
from lib_alloc_plots import (
    aggregate_allocations_per_household,
    plot_allocated_food_bar,
    find_solution_csv,
)

def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print("Usage: python plot_from_solution_dir.py <solution_dir> [output_png]")
        return 1
    solution_dir = Path(argv[1])
    if len(argv) == 3:
        output_png = Path(argv[2])
    else:
        output_png = solution_dir / "allocated_food_by_household.png"

    csv_path = find_solution_csv(solution_dir)
    per_hh = aggregate_allocations_per_household(csv_path)
    plot_allocated_food_bar(per_hh, output_png)
    print(f"CSV: {csv_path}")
    print(f"Plot saved to: {output_png}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
