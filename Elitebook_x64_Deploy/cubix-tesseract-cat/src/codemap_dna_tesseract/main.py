# main.py

from .codemap_spiral import spiral_chain
from .codemap_viewer import print_spiral
from .spiral_pipeline import create_spiral
from .spiral_pipeline_viewer import print_spiral_pipeline, print_function_library, print_spiral_stats


def main(depth: int = 4, use_pipeline: bool = True, show_stats: bool = True):
	"""Main entry: create spiral (traditional or pipeline) and display."""
	if use_pipeline:
		# New: function-ordered spiral pipeline
		spiral = create_spiral()
		print("\n🔗 Function Spiral Pipeline (address-ordered functions)")
		print("=" * 80)
		print_spiral_pipeline(spiral)
		print_function_library(spiral)
		if show_stats:
			print_spiral_stats(spiral)
	else:
		# Original: symbolic spiral
		tesseract_root = spiral_chain(depth=depth)
		print_spiral(tesseract_root)


if __name__ == "__main__":
	main()