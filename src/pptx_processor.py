from pptx import Presentation
from pptx.shapes.group import GroupShape
import subprocess
import pathlib

#Find all .pptx files in directory
def find_pptx_files(source_dir):
    return list(source_dir.glob("*.pptx"))
    
#Change all fonts in the pptx
def change_all_pptx_fonts(pptx_path, new_font_name, output_path):
    
    prs = Presentation(pptx_path)
    
    def process_shape(shape):
    
        # Handle grouped shapes
        if isinstance(shape, GroupShape):
            for sub_shape in shape.shapes:
                process_shape(sub_shape)
        
        # Handle text frames
        if hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                paragraph.font.name = new_font_name
                for run in paragraph.runs:
                    run.font.name = new_font_name
        
        # Handle tables
        if hasattr(shape, "table"):
            for row in shape.table.rows:
                for cell in row.cells:
                    for paragraph in cell.text_frame.paragraphs:
                        paragraph.font.name = new_font_name
                        for run in paragraph.runs:
                            run.font.name = new_font_name
    
    for slide in prs.slides:
        for shape in slide.shapes:
            process_shape(shape)
    
    prs.save(output_path or pptx_path)

#Conversion from pptx -> pdf for further processing
def convert_pptx_to_pdf_with_powerpoint(pptx_path, pdf_output_path):
    
    pptx_path = pathlib.Path(pptx_path).resolve()
    pdf_output_path = pathlib.Path(pdf_output_path).resolve()
    
    applescript = f'''
    tell application "Microsoft PowerPoint"
        open POSIX file "{pptx_path}"
        save active presentation in POSIX file "{pdf_output_path}" as save as PDF
        close active presentation saving no
    end tell
    '''
    
    result = subprocess.run(['osascript', '-e', applescript], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"  Created pdf file: {pdf_output_path}")

    return True