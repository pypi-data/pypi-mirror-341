import os
import shutil
import hashlib
import logging
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def calculate_md5(file_path: Path, chunk_size: int = 8192) -> str:
        """
        Calculate MD5 hash of a file.
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks to read at a time
            
        Returns:
            MD5 hash as hexadecimal string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class FolderMerger:
    """Class for merging folders while handling conflicts."""
    
    def __init__(self, source_root: Path, destination_root: Path):
        """
        Initialize FolderMerger.
        
        Args:
            source_root: Root directory of source files
            destination_root: Root directory where files will be merged
        """
        self.source_root = Path(source_root)
        self.destination_root = Path(destination_root)

    def _resolve_conflict(self, target_file: Path) -> Path:
        """
        Resolve file conflict by creating a new path with '_conflict' suffix.
        
        Args:
            target_file: Path of the conflicting file
            
        Returns:
            New path for the conflicting file
        """
        conflict_path = target_file.with_name(target_file.name + "_conflict")
        logging.warning(f"Conflict detected, saving as: {conflict_path}")
        return conflict_path

    def _should_skip(self, source_file: Path, target_file: Path) -> bool:
        """
        Determine if a file should be skipped during merge.
        
        Args:
            source_file: Path to source file
            target_file: Path to target file
            
        Returns:
            True if file should be skipped, False otherwise
        """
        if not target_file.exists():
            return False
        if source_file.stat().st_size != target_file.stat().st_size:
            return False
        if FileUtils.calculate_md5(source_file) == FileUtils.calculate_md5(target_file):
            logging.info(f"Skipped duplicate: {target_file}")
            return True
        return False

    def merge(self):
        """Merge source directory into destination directory."""
        file_tasks = []
        for root, _, files in os.walk(self.source_root):
            rel_path = os.path.relpath(root, self.source_root)
            target_dir = self.destination_root / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                source_file = Path(root) / file
                target_file = target_dir / file
                file_tasks.append((source_file, target_file))

        for source_file, target_file in tqdm(file_tasks, desc=f"Merging: {self.source_root.name}", unit="file"):
            if self._should_skip(source_file, target_file):
                continue

            if target_file.exists():
                conflict_path = self._resolve_conflict(target_file)
                shutil.copy2(source_file, conflict_path)
            else:
                shutil.copy2(source_file, target_file)


class MergeManager:
    """Manager class for handling multiple folder merges."""
    
    def __init__(self, unzipped_root: Path, output_path: Path):
        """
        Initialize MergeManager.
        
        Args:
            unzipped_root: Root directory containing folders to merge
            output_path: Directory where merged files will be placed
        """
        self.unzipped_root = Path(unzipped_root)
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def merge_all(self):
        """Merge all folders in the source directory."""
        logging.info(f"Starting merge from: {self.unzipped_root} → {self.output_path}")
        folders = [f for f in self.unzipped_root.iterdir() if f.is_dir()]
        for folder in tqdm(folders, desc="Merging folders", unit="folder"):
            logging.info(f"Processing folder: {folder.name}")
            merger = FolderMerger(folder, self.output_path)
            merger.merge()
        logging.info("✅ All folders merged successfully.") 