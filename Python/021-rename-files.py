import os

def main(directory:str)->None:
    rename_files(directory)
    print("Done!\n")
    return None

def rename_files(directory:str)->None:
    """
    Made specificially for renaming .zip files from this format: Author - Album Title (Year), to: Year - Album Title.
    """
    files=os.listdir(directory)
    

    for old_folder in files:
        # _ is the author name, which we don't need.
        _,album_name=old_folder.strip(".zip").split("-",1)
        album_name=album_name.split()
        # The last item will always correspond to the year of release (assuming it is a folder that will be renamed).
        suffix=album_name.pop()

        has_parenthesis=suffix.startswith("(") and suffix.endswith(")")
        suffix=suffix.strip("()")
        if has_parenthesis and suffix.isnumeric():
            year=suffix
            new_folder=f"{year} - {" ".join(album_name)}.zip"

            new_path=os.path.join(directory,new_folder)
            old_path=os.path.join(directory,old_folder)
            
            os.rename(old_path,new_path)

            print(f"Renamed '{old_folder}' to '{new_folder}'")

    return None
if __name__=="__main__":
    DIRECTORY=rf"{input("Enter directory:\n")}"
    main(DIRECTORY)