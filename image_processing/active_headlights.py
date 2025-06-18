from .format_images import FormatImages
from cv2 import imread, hconcat
from numpy import ndarray, mean, std
class ActiveHeadlights(FormatImages):
    def __init__(self, img_path: str) -> None:
        #read the image
        self.img = imread(img_path) if img_path else None
        super().__init__(self.img)

        #this is here so format_dimensions() can refrence the variable
        self.resized_image = None 

    def format_image(self, threshold_scalar: float = 1.0) -> ndarray:
        #format_image to grayscale
        gray_image = self._convert_to_gray(self.img)
        resized_image = self._format_dimensions_(gray_image)
        l, w = resized_image.shape
        #Use x = 140 in img[x:x+h, y,y+h] to not dim headlight for streetlamps
        resized_image = resized_image[140:l, 0:w]
        normalized_image = self._normalize_image_(resized_image)
        blurred_image = self._blur_image_(normalized_image, blur_str='light')
        self.formatted_image = blurred_image

        #threshold for too much brightness, higher threshold values are lead to stricter detections
        self.threshold = mean(self.formatted_image) + threshold_scalar * std(self.formatted_image, ddof = 1)
        return self.formatted_image

    def slice_image(self, img: ndarray, density: str = 'light'):
        density_dict = {'heavy':32, 'medium':16, 'light':8}
        sliced_images = [0,]*density_dict[density]
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
    
    def adaptive_threshold_condition(self, sliced_imgs: ndarray) -> list:
        '''
        returns a list of booleans if a slice is above or below a threshold
        '''
        # left_part = image[:, 0:x_remove_start]

        # # Get the part to the right of the slice
        # # All rows (:), from column x_remove_end to the end
        # right_part = image[:, x_remove_end:]

        # # Concatenate the left and right parts horizontally
        # stitched_image = cv2.hconcat([left_part, right_part])
        iter_img = self.formatted_image.copy()
        k = 1
        self.threshold = mean(iter_img) + k * std(iter_img, ddof=1)
        sliced_img_above_below_threshold_booleans = [0,]*len(sliced_imgs)
        slice_width = 64  
        # This offset tracks how many pixels have been removed from the image so far.
        offset = 0

        for i, sliced_img in enumerate(sliced_imgs):
            mean_sliced_img_val = mean(sliced_img)
            
            if mean_sliced_img_val > self.threshold:
                sliced_img_above_below_threshold_booleans[i] = 1
                
                # Define the slice boundaries in the *current*, potentially smaller, iter_img
                # We subtract the offset to find the correct, shifted position.
                start_x = slice_width * i - offset
                end_x = slice_width * (i + 1) - offset
                
                # Get the parts to the left and right of this adjusted slice
                left = iter_img[:, 0:start_x]
                right = iter_img[:, end_x:]
                
                # Recombine the image without the bright slice
                iter_img = hconcat([left, right])
                
                # IMPORTANT: Update the offset since we just removed a slice
                offset += slice_width

                #try is to catch if the image is fully omitted
                try:self.threshold = mean(iter_img) + k * std(iter_img, ddof=1)
                except:self.threshold = 255
            
        return sliced_img_above_below_threshold_booleans