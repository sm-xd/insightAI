"""
Script to download and build Tree-sitter grammars for InsightAI.

This script clones Tree-sitter grammar repositories and builds the shared libraries
for different programming languages.
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

# Map of language names to their Tree-sitter grammar repository URLs
GRAMMAR_REPOS = {
    "python": "https://github.com/tree-sitter/tree-sitter-python",
    "javascript": "https://github.com/tree-sitter/tree-sitter-javascript",
    "typescript": "https://github.com/tree-sitter/tree-sitter-typescript"
}

def ensure_git_available():
    """Check if Git is available."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Git is not available. Please install Git to continue.")
        return False

def clone_repo(repo_url, target_dir):
    """Clone a Git repository to a target directory."""
    print(f"Cloning {repo_url} to {target_dir}...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, target_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.SubprocessError as e:
        print(f"Failed to clone repository: {e}")
        return False

def build_grammar(language, source_dir, output_dir):
    """Build a Tree-sitter grammar and copy the shared library to output directory."""
    try:
        print(f"Building {language} grammar...")
        
        # Special case for TypeScript which has multiple grammars
        if language == "typescript":
            # First build the base TypeScript grammar
            build_dir = os.path.join(source_dir)
            subprocess.run(
                ["tree-sitter", "generate"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            subprocess.run(
                ["tree-sitter", "build-wasm"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            
            # Copy the shared library
            lib_name = f"tree-sitter-{language}.so"
            src_path = os.path.join(build_dir, "build", "Release", f"{language}.so")
            dst_path = os.path.join(output_dir, lib_name)
            shutil.copy(src_path, dst_path)
            
            # Now build TypeScript TSX grammar
            build_dir = os.path.join(source_dir, "tsx")
            subprocess.run(
                ["tree-sitter", "generate"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            subprocess.run(
                ["tree-sitter", "build-wasm"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            
            # Copy the shared library
            lib_name = f"tree-sitter-tsx.so"
            src_path = os.path.join(build_dir, "build", "Release", "tsx.so")
            dst_path = os.path.join(output_dir, lib_name)
            shutil.copy(src_path, dst_path)
        else:
            # Build regular grammar
            build_dir = source_dir
            subprocess.run(
                ["tree-sitter", "generate"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            subprocess.run(
                ["tree-sitter", "build-wasm"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE
            )
            
            # Copy the shared library
            lib_name = f"tree-sitter-{language}.so"
            src_path = os.path.join(build_dir, "build", "Release", f"{language}.so")
            dst_path = os.path.join(output_dir, lib_name)
            shutil.copy(src_path, dst_path)
        
        print(f"Successfully built {language} grammar")
        return True
    except subprocess.SubprocessError as e:
        print(f"Failed to build {language} grammar: {e}")
        return False
    except FileNotFoundError:
        print("tree-sitter CLI not found. Please install with: npm install -g tree-sitter-cli")
        return False
    except Exception as e:
        print(f"Error building {language} grammar: {e}")
        return False

def main():
    """Main function to build all Tree-sitter grammars."""
    if not ensure_git_available():
        return 1
    
    # Get the directory where the grammars will be stored
    project_root = Path(__file__).parent.parent
    grammar_dir = project_root / "parsers" / "grammars"
    os.makedirs(grammar_dir, exist_ok=True)
    
    # Create a temporary directory for cloning repositories
    with tempfile.TemporaryDirectory() as temp_dir:
        for language, repo_url in GRAMMAR_REPOS.items():
            language_temp_dir = os.path.join(temp_dir, language)
            
            # Clone the repository
            if clone_repo(repo_url, language_temp_dir):
                # Build the grammar
                build_grammar(language, language_temp_dir, grammar_dir)
    
    print("Grammar building process completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())