"""
Folder Merger - A utility for safely merging multiple folders while handling file conflicts.
"""

__version__ = "0.1.0"

from .merger import MergeManager, FolderMerger, FileUtils

__all__ = ["MergeManager", "FolderMerger", "FileUtils"] 