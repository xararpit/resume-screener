import PyPDF2

def extract_text_from_pdf(pdf_source):
    text = ""
    # If the source is a string/Path, open it as a file. If it's already a file-like object, use it directly.
    if isinstance(pdf_source, (str, bytes)) or hasattr(pdf_source, 'is_file') and pdf_source.is_file():
        file = open(pdf_source, "rb")
        close_file = True
    else:
        file = pdf_source
        close_file = False

    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    finally:
        if close_file:
            file.close()

    return text