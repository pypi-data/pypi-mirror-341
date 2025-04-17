import argparse
from pathlib import Path
from .merger import MergeManager

def main():
    parser = argparse.ArgumentParser(description="Merge multiple folders while handling conflicts")
    parser.add_argument("--source", required=True, help="Source directory containing folders to merge")
    parser.add_argument("--destination", required=True, help="Destination directory where files will be merged")
    
    args = parser.parse_args()
    
    source_root = Path(args.source)
    destination_root = Path(args.destination)
    
    if not source_root.exists():
        print(f"Error: Source directory '{source_root}' does not exist")
        return 1
        
    if not destination_root.exists():
        print(f"Error: Destination directory '{destination_root}' does not exist")
        return 1
    
    manager = MergeManager(source_root, destination_root)
    manager.merge_all()
    
    return 0

if __name__ == "__main__":
    exit(main()) 