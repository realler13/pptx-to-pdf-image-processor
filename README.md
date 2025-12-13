# macos-pptx-to-pdf-image-extractor

Part of a larger project (initial)


1. input directory to process
2. iterate through the subdirs ofthe input dir
3. creates dir tree in output/ 
     . subdir
     | - filename 1
     | - filename 2
     | ...
     | - filename n
4. inside each dir creates:
     . filename n
     | - pdf
     | - img
     | - txt
     | - tmp (to be deleted after the process finished)
5. runs pptx_processor on each of pptx found in each subfolder (normalize fonts)
6. saves converted pptx to tmp/
7. runs pptx_to_pdf_converter on all files in tmp/
8. runs image extractor on each processed saved pdf to extract images in accordance with provided template
9. runs text extractor on each saved pdf to extract text from each page of each pdf document
10. cleans tmp

Required libraries:
PyMuPDF>=1.23.0
Pillow>=10.0.0
python-pptx>=0.6.21


Usage: python main.py <directory>


