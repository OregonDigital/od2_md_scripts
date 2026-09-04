"""Automatically zip files/ and metadata csv (and only these two values) from the filepaths.yaml"""
import yaml
import zipfile
from pathlib import Path

#FIXME: This will zip hidden files, like .DS_Store on mac. Users should just check that that doesn't show in the logs, or
# we could add a bigger fix by filtering for it in collect_files.

def collect_files(paths: list[Path]) -> list[Path]:
    """Return all files (counting recursively) from a given list of paths"""
    all_files = []

    # Loop through paths and add files to list
    for path in paths:
        if path.is_dir():
            all_files.extend(file for file in path.rglob('*') if file.is_file())
        else:
            all_files.append(path)
    return all_files

def zip_files(csv_and_metadata_files: list[Path], name: str, root_dir: Path) -> None:
    """Zip all files from a list of paths with given name inside the root directory"""
    # Add zip extension if missing in name argument
    if not name.endswith(".zip"):
        name += ".zip"

    # Make output path
    output_path = root_dir / name

    # Get file list before zipping so we can count progress
    all_files = collect_files(csv_and_metadata_files)
    total = len(all_files)

    # Zip the files into chosen location
    try:
        with zipfile.ZipFile(output_path, "x") as zipf:
            for idx, file in enumerate(all_files, start=1):
                print(f"Zipping {idx}/{total}: {file}")
                zipf.write(file, arcname=file.relative_to(root_dir))
    except FileExistsError:
        print(f"\nFailure: zip file already exists: {output_path}\n")
        return

    print("Done")

def main():
    # Get directory structure from filepaths.yaml
    with open('filepaths.yaml') as file:
        f = yaml.safe_load(file)
        f1 = Path(f['metadata'][0])
        print(f"F1: {f1}")
        f2 = Path(f['assets'])
        print(f"F2: {f2}")

    # Write where directory to put zip is (root of all our operations, likely the work folder)
    root_dir = f2.parent
    print(root_dir)

    # Guess desired zip name from the yaml file input
    zip_folder_name = f1.stem
    # Save assets/ and metadata csv (f1 and f2) to a folder in the root directory
    zip_files([f1, f2], zip_folder_name, root_dir)

if __name__ == "__main__":
    main()