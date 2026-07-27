import yaml
import zipfile
from pathlib import Path


# Simpler version that doesn't give progress count

# def zip_files(files: list[Path], name: str, dir: Path) -> None:
#     """Create a zip from a list of file names. Input only names and not filepaths"""
#     # Add zip to end if no extension
#     if not name.endswith('.zip'):
#         name += '.zip'

#     output_path = dir / name

#     # Zip the files
#     with zipfile.ZipFile(output_path, "w") as zipf:
#         for path in files:
#             if path.is_dir():
#                 for file in path.rglob("*"):
#                     if file.is_file():
#                         print(f"Zipping files...")
#                         zipf.write(file, arcname=file.relative_to(dir))
#             else:
#                 print("Zipping files...")
#                 zipf.write(path, arcname=path.relative_to(dir))
#     print("Done")


# More complicated version that gives progress count
def collect_files(paths: list[Path]) -> list[Path]:
    all_files = []
    for path in paths:
        if path.is_dir():
            all_files.extend(file for file in path.rglob('*') if file.is_file())
        else:
            all_files.append(path)
    return all_files

def zip_files(files: list[Path], name: str, dir: Path) -> None:
    if not name.endswith(".zip"):
        name += ".zip"

    output_path = dir / name
    all_files = collect_files(files)
    total = len(all_files)

    with zipfile.ZipFile(output_path, "w") as zipf:
        for idx, file in enumerate(all_files, start=1):
            print(f"Zipping {idx}/{total}: {file}")
            zipf.write(file, arcname=file.relative_to(dir))

    print("Done")

def main():
    with open('filepaths.yaml') as file:
        f = yaml.safe_load(file)
        f1 = Path(f['metadata'][0])
        print(f"F1: {f1}")
        f2 = Path(f['assets'])
        print(f"F2: {f2}")

    target_dir = Path(str(f2).replace("\\files", ''))
    print(target_dir)

    # Can rename test to desired folder name. In future could have it be a filepaths field.
    # Could try to extract it from filepaths but this will be annoying and hard to verify
    zip_files([f1, f2], "test", target_dir)


if __name__ == "__main__":
    main()