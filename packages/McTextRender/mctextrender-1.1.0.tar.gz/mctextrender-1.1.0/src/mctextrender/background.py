from PIL import Image


class BackgroundImageLoader:
    def __init__(
        self,
        dir: str,
        default_filename: str = "base.png" 
    ) -> None:
        
        self._dir = dir
        self._default_filename = default_filename
        self._default_img_path = f"{dir}/{default_filename}"


    def __load_image(self, image_path: str) -> Image.Image:
        return Image.open(image_path)


    def load_image(self, image_path: str) -> Image.Image:
        return self.__load_image(image_path).copy()


    def load_default_background(self) -> Image.Image:
        return self.load_image(self._default_img_path)