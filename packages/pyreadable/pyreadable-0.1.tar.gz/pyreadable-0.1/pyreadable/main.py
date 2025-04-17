import fitz  
from .readablity import check_images_in_pdf, read_pdf, check_path


def get_text_areas_per_page(file_path):
    """
    Calculate the area occupied by text in a PDF file.
    """
    doc = fitz.open(file_path)
    text_areas = []

    for page in doc:
        blocks = page.get_text("blocks")  
        total_area = 0
        for block in blocks:
            x0, y0, x1, y1 = block[:4]
            width = x1 - x0
            height = y1 - y0
            area = width * height
            total_area += area
        text_areas.append(total_area)

    return text_areas

def get_image_areas_per_page(file_path, dpi=72):
    """
    Calculate the area occupied by images in a PDF file.
    """
    doc = fitz.open(file_path)

    image_areas = []

    for page in doc:
        page_images = page.get_images(full=True)
        page_area = 0

        for img in page_images:
            xref = img[0]
            rects = page.get_image_rects(xref)
            for r in rects:
                width = r.width
                height = r.height
                page_area += width * height

        image_areas.append(page_area)

    return image_areas

def get_margin_based_space(file_path, margin_pts=72):
    """
    Calculate the available space in a PDF file based on the page size and margins.
    """
    doc = fitz.open(file_path)


    width = doc[0].rect.width
    height = doc[0].rect.height

    available_width = width - 2 * margin_pts
    available_height = height - 2 * margin_pts

    return (available_width, available_height)  

def get_true_blank_space_per_page(file_path,margin_pts=72, dpi=72):
    """
    Calculate the blank space in a PDF file based on the available area and the areas occupied by text and images.
    """

    available_width, available_height = get_margin_based_space(file_path, margin_pts)
    available_area = available_width * available_height

    text_areas = get_text_areas_per_page(file_path)
    image_areas = get_image_areas_per_page(file_path,dpi)

    blank_spaces = []
    for text_area, img_area in zip(text_areas, image_areas):
        occupied_area = text_area + img_area
        blank_area = max(available_area - occupied_area, 0)
        blank_spaces.append(blank_area)

    return blank_spaces

def is_machine_readable(file_path,margin_pts=72, dpi=72):
    """
    Check if a PDF file is machine-readable based on the presence of images and text.
    Args:
        file_path (str): Path to the PDF file.
        margin_pts (int): Margin in points to consider for available space.
        dpi (int): Dots per inch for image resolution.
    
    Returns:
        bool: True if the PDF is machine-readable, False otherwise.
        float: Percentage of text in the PDF.
    """
    if check_path(file_path):
        pass
    
    text_percent = 0.0
    if not check_images_in_pdf(file_path):
        if len(read_pdf(file_path))==0:
            return False, text_percent
        else:
            text_percent = 1.0
            return True , text_percent
    else:
        if len(read_pdf(file_path))==0:
            return False, text_percent
        else:
            space_per_page = get_margin_based_space(file_path)
            available_area = space_per_page[0] * space_per_page[1]

            text_areas = get_text_areas_per_page(file_path)
            text_area = sum(text_areas)

            blank_spaces = get_true_blank_space_per_page(file_path,margin_pts,dpi)
            blank_area = sum(blank_spaces)

            if available_area == 0:
                return False, text_percent  

            text_percent = (text_area / ((len(text_areas)*available_area)-blank_area))


        return False, text_percent