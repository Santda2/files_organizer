import os
import shutil
from typing import Optional
from pathlib import Path

imageTypes:list[str]  = [".png",".jpg",".jpeg"]
pdgType = ".pdf"
exelType = ".xlsx"
compressedTypes = [".zip",".rar"]
execuatablesTypes = ".exe"


def ensure_downloads_subfolder(folder_name: str, verbose: bool = True) -> Optional[str]:
    """
    Ensure a subfolder exists in the Downloads directory.
    If it doesn't exist, creates it.
    
    Args:
        folder_name: Name of the folder to check/create
        verbose: Whether to print status messages (default: True)
    
    Returns:
        Full path to the folder if successful, None otherwise
    
    Raises:
        OSError: If folder creation fails for reasons other than already existing
    """
    # Get the Downloads folder path
    downloads_path: str = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Create the full path for our target folder
    target_folder: str = os.path.join(downloads_path, folder_name)
    
    try:
        # Check if folder exists, if not create it
        if not os.path.exists(target_folder):
            os.makedirs(target_folder, exist_ok=True)
            if verbose:
                print(f"Created folder: {target_folder}")
        elif verbose:
            print(f"Folder already exists: {target_folder}")
        
        return target_folder
    
    except OSError as e:
        if verbose:
            print(f"Error accessing folder '{target_folder}': {e}")
        return None


import shutil
from pathlib import Path
from typing import Optional

def move_file_to_folder(target_folder: str, filename: str, downloads_folder: str = None) -> Optional[str]:
    """
    Move a file from the downloads folder to the specified target folder.
    
    Args:
        target_folder: Path to the destination folder (from ensure_downloads_subfolder)
        filename: Name of the file to be moved (must be in downloads folder)
        downloads_folder: Path to downloads folder (defaults to system downloads if None)
    
    Returns:
        New path of the moved file if successful, None otherwise
    """
    try:
        # Set up paths
        folder_path = Path(target_folder)
        
        # Determine downloads folder path
        if downloads_folder is None:
            downloads_path = Path.home() / 'Downloads'  # Default to user's Downloads folder
        else:
            downloads_path = Path(downloads_folder)
        
        file_path = downloads_path / filename
        
        # Verify inputs
        if not folder_path.is_dir():
            print(f"Error: Target folder doesn't exist: {folder_path}")
            return None
            
        if not file_path.is_file():
            print(f"Error: Source file doesn't exist in downloads: {file_path}")
            return None
            
        # Create destination path
        destination = folder_path / filename
        
        # Handle case where file already exists in destination
        if destination.exists():
            print(f"Warning: File already exists in destination: {destination}")
            # Optional: Add logic to rename or overwrite here
            
        # Perform the move
        shutil.move(str(file_path), str(destination))
        print(f"Moved '{filename}' from downloads to '{folder_path}'")
        return str(destination)
        
    except shutil.Error as e:
        print(f"Error moving file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    files = [f for f in os.listdir(download_folder) 
        if os.path.isfile(os.path.join(download_folder, f))]
    

    folders = {
        "imagesFolder":ensure_downloads_subfolder("images"),
        "pdfFolder":ensure_downloads_subfolder("pdfFolder"),
        "compressedFolder":ensure_downloads_subfolder("compressedFolder"),
        "exelFolder":ensure_downloads_subfolder("exelFolder"),
        "execuatablesFolder":ensure_downloads_subfolder("execuatablesFolder")
    }
    for file in files:

        
        if any(file.endswith(imageTpe) for imageTpe in imageTypes):
            move_file_to_folder(folders["imagesFolder"],file)
        
        if file.endswith(pdgType):
            move_file_to_folder(folders["pdfFolder"],file)

        if file.endswith(exelType):
            move_file_to_folder(folders["exelFolder"],file)

        if any(file.endswith(compressed) for compressed in compressedTypes):
            move_file_to_folder(folders["compressedFolder"],file)
        
        if file.endswith(execuatablesTypes):
            move_file_to_folder(folders["execuatablesFolder"],file)


if __name__== "__main__":
    main()