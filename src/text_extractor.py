
import pathlib
import fitz

def extract_all_page_text(pdf_name, txt_dir):
    text_sourse = fitz.open(pdf_name)

    # Get all text from the page and save it
    for page_index in range(len(text_sourse)):
        page = text_sourse[page_index]

        full_text = page.get_text()
        with open(txt_dir / f"{page_index}.txt", "w") as f:
            f.write(full_text)