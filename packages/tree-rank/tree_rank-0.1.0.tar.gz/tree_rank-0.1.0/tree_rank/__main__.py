from .core import print_tree
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Tree Rank - Print a clean directory structure")
    parser.add_argument("path", nargs="?", default=".", help="Root directory to start from (default: current directory)")
    args = parser.parse_args()

    print(f"\n📁 Directory Tree for: {os.path.abspath(args.path)}\n")
    print_tree(args.path)

if __name__ == "__main__":
    main()
