import pathlib

def find_all_pdf_fies(source_dir):
    return list(source_dir.glob("*.pdf"))