from fastapi import UploadFile

IMAGE_MAX_SIZE_IN_MB = 5
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']


class ImageUploadValidation:
    @staticmethod
    def validate_image(value: UploadFile) -> UploadFile:
        ImageUploadValidation.validate_image_size(value)
        ImageUploadValidation.validate_image_extension(value)
        return value

    @staticmethod
    def validate_image_size(value: UploadFile) -> UploadFile:
        if value.file.seek(0, 2) > IMAGE_MAX_SIZE_IN_MB * 1024 * 1024:
            raise ValueError(
                f'Image size must be less than {IMAGE_MAX_SIZE_IN_MB} MB'
            )
        return value

    @staticmethod
    def validate_image_extension(value: UploadFile) -> UploadFile:
        extension = value.filename.split('.')[-1]
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(
                f'Image extension must be one of {ALLOWED_IMAGE_EXTENSIONS}'
            )
        return value
