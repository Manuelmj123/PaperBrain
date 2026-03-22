TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".json",
    ".csv",
    ".log",
    ".yaml",
    ".yml"
}

DOCX_EXTENSIONS = {
    ".docx"
}

PDF_EXTENSIONS = {
    ".pdf"
}

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".webp"
}

SUPPORTED_EXTENSIONS = (
    TEXT_EXTENSIONS
    | DOCX_EXTENSIONS
    | PDF_EXTENSIONS
    | IMAGE_EXTENSIONS
)