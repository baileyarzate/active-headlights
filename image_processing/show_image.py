from .format_images import FormatImages
from cv2 import imread
from numpy import ndarray
class ShowImage(FormatImages):
    def __init__(self, img_path: str) -> None:
        self.img = imread(img_path) if img_path else None
        self.height = 512
        self.width = 288

    def slice_unfiltered_image(self, img:ndarray, density: str = 'light'):
        density_dict = {'heavy':32, 'medium':16, 'light':8}
        sliced_images = [0,]*density_dict[density]
        img = self._format_dimensions_(img)
        for i in range(density_dict[density]):
            if density == 'light':
                sliced_images[i] = img[0:self.height, 64*(i):64*(i+1)]
            elif density == 'medium':
                sliced_images[i] = img[0:self.height, 32*(i):32*(i+1)]
            elif density == 'heavy':
                sliced_images[i] = img[0:self.height, 16*(i):16*(i+1)]
            else: 
                density = 'light'
                i = i - 1
        return sliced_images