"""
Utility functions for InsightAI backend.
"""

import os
import shutil
import tempfile
from typing import List, Tuple
from pathlib import Path

def get_file_extension(filename: str) -> str:
    """
    Get the extension of a file.
    
    Args:
        filename: Name of the file
        
    Returns:
        Extension without dot
    """
    return Path(filename).suffix.lstrip('.')

def get_temp_dir() -> Tuple[str, tempfile._TemporaryFileWrapper]:
    """
    Create a temporary directory.
    
    Returns:
        Tuple of (directory path, temporary directory object)
    """
    temp_dir = tempfile.mkdtemp()
    temp_obj = tempfile.TemporaryDirectory(dir=temp_dir)
    return temp_dir, temp_obj

def extract_archive(file_path: str, extract_dir: str) -> str:
    """
    Extract an archive file.
    
    Args:
        file_path: Path to archive file
        extract_dir: Directory to extract to
        
    Returns:
        Path to extracted directory
        
    Raises:
        ValueError if file format is not supported
    """
    ext = get_file_extension(file_path).lower()
    
    if ext == 'zip':
        shutil.unpack_archive(file_path, extract_dir, 'zip')
    elif ext in ['gz', 'tgz']:
        shutil.unpack_archive(file_path, extract_dir, 'gztar')
    else:
        raise ValueError(f"Unsupported archive format: {ext}")
    
    return extract_dir

def is_safe_path(base_path: str, path: str) -> bool:
    """
    Check if a path is safe (doesn't escape base directory).
    
    Args:
        base_path: Base directory path
        path: Path to check
        
    Returns:
        True if path is safe, False otherwise
    """
    try:
        return os.path.abspath(path).startswith(os.path.abspath(base_path))
    except Exception:
        return False

def walk_files(directory: str, ignore_patterns: List[str] = None) -> List[str]:
    """
    Walk a directory and return all file paths.
    
    Args:
        directory: Directory to walk
        ignore_patterns: List of glob patterns to ignore
        
    Returns:
        List of file paths
    """
    ignore_patterns = ignore_patterns or []
    file_paths = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if file matches any ignore pattern
            skip = False
            for pattern in ignore_patterns:
                if Path(file_path).match(pattern):
                    skip = True
                    break
            
            if not skip:
                file_paths.append(file_path)
    
    return file_paths

def get_file_type(file_path: str) -> str:
    """
    Determine file type based on extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        File type string
    """
    ext = get_file_extension(file_path).lower()
    
    # Programming languages
    if ext in ['py']:
        return 'python'
    elif ext in ['js', 'jsx', 'ts', 'tsx']:
        return 'javascript'
    elif ext in ['java']:
        return 'java'
    elif ext in ['cpp', 'hpp', 'cc', 'hh', 'c', 'h']:
        return 'cpp'
    elif ext in ['go']:
        return 'go'
    elif ext in ['rs']:
        return 'rust'
    
    # Web files
    elif ext in ['html', 'htm']:
        return 'html'
    elif ext in ['css', 'scss', 'sass', 'less']:
        return 'css'
    elif ext in ['json']:
        return 'json'
    elif ext in ['xml']:
        return 'xml'
    elif ext in ['yaml', 'yml']:
        return 'yaml'
    
    # Documentation
    elif ext in ['md']:
        return 'markdown'
    elif ext in ['rst']:
        return 'restructuredtext'
    elif ext in ['txt']:
        return 'text'
    
    # Other
    else:
        return 'unknown'

def cleanup_temp_files(*paths: str) -> None:
    """
    Clean up temporary files and directories.
    
    Args:
        *paths: Paths to clean up
    """
    for path in paths:
        try:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {str(e)}")

def normalize_path(path: str) -> str:
    """
    Normalize a file path.
    
    Args:
        path: Path to normalize
        
    Returns:
        Normalized path
    """
    return os.path.normpath(path)