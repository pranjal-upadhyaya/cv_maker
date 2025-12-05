import subprocess

def compress_pdf_ghostscript(input_path: str, output_path: str = None, quality: str = "default"):
    """
    Aggressively compress a PDF using Ghostscript.
    Args:
        input_path: Path to input PDF file
        output_path: Path to save compressed PDF file. If None, will append '_compressed' to input filename
        quality: One of 'screen', 'ebook', 'printer', 'prepress', or 'default'
            - 'screen'   (72 dpi, smallest)
            - 'ebook'    (150 dpi)
            - 'printer'  (300 dpi)
            - 'prepress' (300 dpi, color preserved)
            - 'default'  (usually 300 dpi)
    """
    if output_path is None:
        name_parts = input_path.rsplit('.', 1)
        output_path = f"{name_parts[0]}_compressed.{name_parts[1]}"
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    subprocess.run(gs_command, check=True)

if __name__ == "__main__":
    compress_pdf_ghostscript("output.pdf", "cv_compressed.pdf", "default")