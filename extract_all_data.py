import zipfile
import os
import glob
from pathlib import Path

def safe_extract(zip_path, target_dir):
    """Extract ZIP file with sanitized filenames"""
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in z.namelist():
            # Replace forbidden characters in filenames
            safe_name = member.replace(':', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            dest_path = os.path.join(target_dir, safe_name)
            # Make parent dirs if necessary
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            # Extract the file
            with z.open(member) as src, open(dest_path, "wb") as dst:
                dst.write(src.read())

def list_directory_contents(path, indent=0):
    """Recursively list all files and directories"""
    try:
        items = os.listdir(path)
        for item in sorted(items):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print("  " * indent + f"📁 {item}/")
                list_directory_contents(item_path, indent + 1)
            else:
                size = os.path.getsize(item_path)
                print("  " * indent + f"📄 {item} ({size:,} bytes)")
    except PermissionError:
        print("  " * indent + "❌ Permission denied")
    except Exception as e:
        print("  " * indent + f"❌ Error: {e}")

def main():
    # Define paths
    data_folder = "Data-20250728T195457Z-1-001/Data"
    output_base = "extracted_data"
    
    print("=" * 60)
    print("COMPLETE DATA EXTRACTION AND LISTING")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(output_base, exist_ok=True)
    
    # Find all ZIP files
    zip_files = glob.glob(os.path.join(data_folder, "*.zip"))
    print(f"\nFound {len(zip_files)} ZIP files:")
    for zip_file in zip_files:
        print(f"  📦 {os.path.basename(zip_file)}")
    
    # Extract all ZIP files
    print(f"\n📂 Extracting all files to '{output_base}/' directory...")
    for zip_path in zip_files:
        base_name = os.path.splitext(os.path.basename(zip_path))[0]
        out_dir = os.path.join(output_base, base_name)
        print(f"  🔄 Extracting {os.path.basename(zip_path)} → {out_dir}/")
        try:
            safe_extract(zip_path, out_dir)
            print(f"  ✅ Successfully extracted {os.path.basename(zip_path)}")
        except Exception as e:
            print(f"  ❌ Error extracting {os.path.basename(zip_path)}: {e}")
    
    # List all contents
    print(f"\n📋 COMPLETE FILE LISTING:")
    print("=" * 60)
    
    # List original data folder
    print(f"\n📁 Original Data Folder ({data_folder}):")
    list_directory_contents(data_folder)
    
    # List extracted contents
    print(f"\n📁 Extracted Data Folder ({output_base}):")
    if os.path.exists(output_base):
        list_directory_contents(output_base)
    else:
        print("  ❌ Extracted folder not found")
    
    # Summary statistics
    print(f"\n📊 SUMMARY:")
    print("=" * 60)
    
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk(output_base):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_files += 1
                total_size += size
            except:
                pass
    
    print(f"  📄 Total files extracted: {total_files:,}")
    print(f"  💾 Total size: {total_size:,} bytes ({total_size / (1024*1024):.2f} MB)")
    
    # List all directories created
    print(f"\n📁 Directory Structure:")
    for root, dirs, files in os.walk(output_base):
        level = root.replace(output_base, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for file in sorted(files)[:10]:  # Show first 10 files per directory
            print(f"{subindent}📄 {file}")
        if len(files) > 10:
            print(f"{subindent}... and {len(files) - 10} more files")

if __name__ == "__main__":
    main() 