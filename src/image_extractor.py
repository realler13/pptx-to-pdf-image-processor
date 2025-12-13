import fitz
from PIL import Image


def extract_all_pdf_images(pdf_path, img_dir, tmp_dir):
    ##Extract and crop images from each PDF page
    
    pdf_sample = fitz.open(pdf_path)
    pdf_name = pdf_path.stem
    
    for page_index in range(len(pdf_sample)):
        page = pdf_sample[page_index]
        
        # Render full page at high resolution
        zoom = 3
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Save temp full page
        temp_filename = f"{page_index}_{pdf_name}_full.png"
        pix.save(tmp_dir / temp_filename)
        
        # Load and crop
        img = Image.open(tmp_dir / temp_filename)
        
        # Crop coordinates
        x0, y0, x1, y1 = 107, 187, 2910, 1586
        
        cropped = img.crop((x0, y0, x1, y1))
        cropped.save(img_dir / f"{page_index}.png")
     
    pdf_sample.close()
