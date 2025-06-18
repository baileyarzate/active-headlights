from cv2 import COLOR_RGB2GRAY, cvtColor, resize, normalize, NORM_MINMAX, blur
from numpy import ndarray
class FormatImages():
    def __init__(self, img: ndarray) -> None:
        self.img = img

    def _convert_to_gray(self, img: ndarray) -> ndarray:
        return cvtColor(img, COLOR_RGB2GRAY)
    
    def _format_dimensions_(self, img: ndarray, width:int = 512, height:int = 288) -> ndarray:
        self.width, self.height = width, height #these variables may need to be referenced outside this function
        return resize(img, (self.width, self.height))
    
    def _normalize_image_(self, img: ndarray) -> ndarray:
        return normalize(img, None, alpha=0, beta=255, norm_type=NORM_MINMAX)

    def _blur_image_(self, img: ndarray, blur_str: str = 'light') -> ndarray:
        if blur_str == 'light': blurred_img = blur(img, (2, 2))
        elif blur_str == 'medium': blurred_img = blur(img, (5, 5))
        elif blur_str == 'strong': blurred_img = blur(img, (10, 10))
        else: blurred_img = blur(img, (2, 2))
        return blurred_img