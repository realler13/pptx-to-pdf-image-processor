import sys
import fitz
from PIL import Image
import pathlib
import shutil

from src.text_extractor import extract_all_page_text
from src.image_extractor import extract_all_pdf_images
from src.pptx_processor import find_pptx_files, change_all_pptx_fonts, convert_pptx_to_pdf_with_powerpoint
from src.pdf_handler import find_all_pdf_fies


if len(sys.argv) < 2:
    print("Usage: python main.py <directory>")
    sys.exit(1)

source = pathlib.Path(sys.argv[1])

if not source.exists():
    print(f"Error: '{source}' does not exist")
    sys.exit(1)

if not source.is_dir():
    print(f"Error: '{source}' is not a directory")
    sys.exit(1)




def main():
    subdirs = [d for d in source.iterdir() if d.is_dir()]
    print(f"Found {len(subdirs)} subdirectories") ##DEBUG

    for subdir in subdirs:
        print(f"\n=== Processing {subdir.name} ===") ##DEBUG
        pdf_ag_module_name = subdir.name
        print(f"Output will go to: output/{pdf_ag_module_name}") ##DEBUG
        base_dir = pathlib.Path("output") / pdf_ag_module_name
        img_dir = base_dir / "img"
        txt_dir = base_dir / "txt"
        tmp_dir = base_dir / "temp"
        pdf_dir = base_dir / "pdf"
        
        base_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)
        txt_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        pdf_dir.mkdir(parents=True, exist_ok=True)
        


        pptx_files = find_pptx_files(subdir)
        print(f"Found {len(pptx_files)} PPTX files") ##DEBUG
        for file in pptx_files:
            output_filename = file.name
            output_path = tmp_dir / output_filename
            print(f"  Changing fonts in: {file.name}") ##DEBUG
            change_all_pptx_fonts(file, "Helvetica Neue", output_path)
        
        updated_pptx_files = find_pptx_files(tmp_dir)
        print(f"Found {len(updated_pptx_files)} updated PPTX files") ##DEBUG
        for updated_file in updated_pptx_files:
                print(f"  Processing pptx --> pdf: {updated_file.name}") ##DEBUG
                pdf_filename = updated_file.stem + ".pdf"
                print(f"  New pdf file name: {pdf_filename}") ##DEBUG
                pdf_path = pdf_dir / pdf_filename
                print(f"  Pdf outut to: {pdf_path}") ##DEBUG
                convert_pptx_to_pdf_with_powerpoint(updated_file, pdf_path)                       
    
        pdf_files_to_process = find_all_pdf_fies(pdf_dir)
        print(f"Found {len(pdf_files_to_process)} PDF files") ##DEBUG
        for pdf_file in pdf_files_to_process:
            print(f"  Processing pdf: {pdf_file.name}") ##DEBUG
            tmp_sub_dir = tmp_dir / pdf_file.stem
            tmp_sub_dir.mkdir(parents=True, exist_ok=True)
            img_sub_dir = img_dir / pdf_file.stem
            img_sub_dir.mkdir(parents=True, exist_ok=True)
            txt_sub_dir = txt_dir / pdf_file.stem
            txt_sub_dir.mkdir(parents=True, exist_ok=True)
            extract_all_pdf_images(pdf_file, img_sub_dir, tmp_sub_dir)
            extract_all_page_text(pdf_file, txt_sub_dir)

        shutil.rmtree(tmp_dir)  # Delete temp folder
       
if __name__ == "__main__":
    main()