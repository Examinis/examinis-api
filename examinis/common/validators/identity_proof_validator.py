from fastapi import UploadFile, HTTPException

PDF_MAX_SIZE_IN_MB = 5
ALLOWED_EXTENSION = "pdf"


class PDFUploadValidation:
    @staticmethod
    def validate_pdf(value: UploadFile) -> UploadFile:
        PDFUploadValidation.validate_pdf_size(value)
        PDFUploadValidation.validate_pdf_extension(value)
        return value

    @staticmethod
    def validate_pdf_size(value: UploadFile) -> UploadFile:
        value.file.seek(0, 2)
        file_size = value.file.tell()
        value.file.seek(0)

        if file_size > PDF_MAX_SIZE_IN_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail=f"O arquivo deve ter no máximo {PDF_MAX_SIZE_IN_MB} MB"
            )
        return value

    @staticmethod
    def validate_pdf_extension(value: UploadFile) -> UploadFile:
        extension = value.filename.split('.')[-1].lower()
        if extension != ALLOWED_EXTENSION:
            raise HTTPException(
                status_code=400, detail=f"O arquivo deve ser um PDF ({ALLOWED_EXTENSION})"
            )
        return value
