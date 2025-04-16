import exiftool


file_name = r"C:\Users\Jackc\Desktop\镜头\DSC04780.ARW"

with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata(file_name)

# write to a txt file
with open("metadata_arw.txt", "w") as f:
    for item in metadata:
        for key, value in item.items():
            f.write(f"{key}: {value}\n")
        f.write("\n")  # Add a blank line between items
