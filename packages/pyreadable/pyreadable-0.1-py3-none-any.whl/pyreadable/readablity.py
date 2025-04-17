import PyPDF2
import fitz
import os


def read_pdf(file_path):
    lines = []

# Open the PDF file
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages
        num_pages = len(pdf_reader.pages)

        # Extract text from each page
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            lines.append(text)

    return " ".join(lines)


def check_images_in_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    has_images = False

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        if image_list:
            has_images = True
            break

    return has_images


def check_path(file_path):
    """
    Check if the file path is valid pdf file.
    """    
    if not os.path.isfile(file_path):
        raise ValueError("File path is not valid.")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("File is not a PDF file.")
    
    return True
