from .schemas import ImageGenProperties, VideoGenProperties, SubtitleGenProperties


class Settings:
    url_mapping = {
        "api_key_verification": "https://sso.pixy.ir/api_key/verify",
        "image": "https://media.pixy.ir/v1/apps/imagine/imagination/",
        "video": "https://media.pixy.ir/v1/apps/videogen/videos/",
        "subtitle": "https://media.pixy.ir/v1/apps/subtitle/subtitles/",
    }
    properties_mapping = {
        "image": ImageGenProperties,
        "video": VideoGenProperties,
        "subtitle": SubtitleGenProperties,
    }

    def __init__(self, url_mapping: dict = None, properties_mapping: dict = None):
        if url_mapping is not None:
            self.url_mapping = url_mapping
        if properties_mapping is not None:
            self.properties_mapping = properties_mapping
