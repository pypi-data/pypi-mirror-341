from io import BytesIO
from PIL import Image
from typing import Literal, TypedDict

from .text import render_mc_text


class TextOptions(TypedDict):
    font_size: int
    position: tuple[int, int]
    shadow_offset: tuple[int, int] | None
    align: Literal["left", "right", "center"]

    @staticmethod
    def default() -> 'TextOptions':
        return {
            "font_size": 16,
            "position": (0, 0),
            "shadow_offset": None,
            "align": "left"
        }


class ImageRender:
    def __init__(self, base_image: Image.Image):
        self._image: Image.Image = base_image.convert("RGBA")
        self.text = TextRender(self._image)     


    def overlay_image(self, overlay_image: Image.Image) -> None:
        self._image.alpha_composite(overlay_image.convert("RGBA"))


    def to_bytes(self) -> bytes:
        image_bytes = BytesIO()
        self._image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        return image_bytes     
     

    def save(self, filepath: str, **kwargs) -> None:
        self._image.save(filepath, **kwargs)


    @property
    def size(self) -> tuple[int, int]:
        return self._image.size



class TextRender:
    def __init__(self, image: Image.Image) -> None:
        self._image = image
         

    def draw(
        self,
        text: str,
        text_options: TextOptions=TextOptions.default()
    ) -> None:
        
        if "position" not in text_options:
            text_options["position"] = (0, 0)
        render_mc_text(text, image=self._image, **text_options)

   
    def draw_many(
        self,
        text_info: list[tuple[str, TextOptions]],
        default_text_options: TextOptions
    ) -> None:
        
        for text, text_options in text_info:
            self.draw(text, {**default_text_options, **text_options})  