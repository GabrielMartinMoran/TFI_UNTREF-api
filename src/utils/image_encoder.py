from base64 import b64encode


class ImageEncoder:
    BASE_64_ENCODING_PREFIX = 'data:image/jpg;base64,'

    @staticmethod
    def to_base_64_str(image) -> str:
        if not image:
            return None
        return F'{ImageEncoder.BASE_64_ENCODING_PREFIX}{b64encode(image).decode("utf-8")}'
