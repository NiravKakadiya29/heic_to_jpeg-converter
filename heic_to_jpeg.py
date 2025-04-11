from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog
import os

def convert_heic_to_jpeg():
    # Initialize Tkinter for file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select HEIC files (allow multiple selection)
    print("Select one or more HEIC image files (or cancel to select a folder)...")
    heic_paths = filedialog.askopenfilenames(
        title="Select HEIC Images",
        filetypes=[("HEIC files", "*.heic *.HEIC")]
    )

    # If no files selected, ask for a folder
    if not heic_paths:
        print("No files selected. Select a folder to process all HEIC files in it...")
        folder_path = filedialog.askdirectory(title="Select Folder Containing HEIC Files")
        if not folder_path:
            print("No folder selected. Exiting.")
            return
        # Find all HEIC files in the folder
        heic_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                      if f.lower().endswith('.heic')]

    if not heic_paths:
        print("No HEIC files found. Exiting.")
        return

    # Set default output folder
    default_output = os.path.join(os.getcwd(), "output")
    print(f"Output will be saved to: {default_output}")
    print("Select output folder (or cancel to use default)...")
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    output_folder = output_folder or default_output

    # Ensure pillow_heif is registered
    pillow_heif.register_heif_opener()

    # Process each HEIC file
    success_count = 0
    error_count = 0

    for heic_path in heic_paths:
        try:
            # Debug: Print input path
            print(f"Processing input: {heic_path}")

            # Open HEIC image
            image = Image.open(heic_path)

            # Convert to RGB if necessary (JPEG requires RGB)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Build output path
            base_name = os.path.basename(os.path.splitext(heic_path)[0])
            jpeg_path = os.path.join(output_folder, f"{base_name}.jpg")

            # Debug: Print output path
            print(f"Output path: {jpeg_path}")

            # Ensure output directory exists
            os.makedirs(output_folder, exist_ok=True)

            # Save as JPEG with maximum quality
            image.save(jpeg_path, "JPEG", quality=100, subsampling=0)
            print(f"Converted: {os.path.basename(heic_path)} -> {os.path.basename(jpeg_path)}")
            success_count += 1

        except Exception as e:
            print(f"Error converting {os.path.basename(heic_path)}: {e}")
            error_count += 1

    # Summary
    print(f"\nBatch conversion complete: {success_count} files converted successfully, {error_count} errors.")

if __name__ == "__main__":
    convert_heic_to_jpeg()