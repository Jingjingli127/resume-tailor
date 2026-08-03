import argparse
from pathlib import Path

import fitz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(args.pdf)
    matrix = fitz.Matrix(2, 2)
    for index, page in enumerate(document):
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        pixmap.save(args.output_dir / f"page-{index + 1}.png")
    print(f"Rendered {len(document)} pages.")


if __name__ == "__main__":
    main()
