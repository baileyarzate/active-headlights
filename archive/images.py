import cv2
import matplotlib.pyplot as plt
import numpy as np

class FormatImages():
    def __init__(self, img: np.ndarray) -> None:
        self.img = img

    def _convert_to_gray(self, img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    def _format_dimensions_(self, img: np.ndarray, width:int = 512, height:int = 288) -> np.ndarray:
        self.width, self.height = width, height #these variables may need to be referenced outside this function
        return cv2.resize(img, (self.width, self.height))
    
    def _normalize_image_(self, img: np.ndarray) -> np.ndarray:
        return cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    def _blur_image_(self, img: np.ndarray, blur: str = 'light') -> np.ndarray:
        if blur == 'light': blurred_img = cv2.blur(img, (2, 2))
        elif blur == 'medium': blurred_img = cv2.blur(img, (5, 5))
        elif blur == 'strong': blurred_img = cv2.blur(img, (10, 10))
        else: blurred_img = cv2.blur(img, (2, 2))
        return blurred_img

class ShowImage(FormatImages):
    def __init__(self, img_path: str) -> None:
        self.img = cv2.imread(img_path)
        self.height = 512
        self.width = 288

    def slice_unfiltered_image(self, img:np.ndarray, density: str = 'light'):
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

class ActiveHeadlights(FormatImages):
    def __init__(self, img_path: str) -> None:
        #read the image
        self.img = cv2.imread(img_path)
        super().__init__(self.img)

        #this is here so format_dimensions() can refrence the variable
        self.resized_image = None 

    def format_image(self) -> np.ndarray:
        #format_image to grayscale
        gray_image = self._convert_to_gray(self.img)
        resized_image = self._format_dimensions_(gray_image)
        l, w = resized_image.shape
        #Use x = 130 in img[x:x+h, y,y+h] to not dim headlight for streetlamps
        resized_image = resized_image[140:l, 0:w]
        normalized_image = self._normalize_image_(resized_image)
        blurred_image = self._blur_image_(normalized_image, blur='light')
        self.formatted_image = blurred_image

        #threshold for too much brightness
        k = 1 # adjust this value to scale threshold
        self.threshold = np.mean(self.formatted_image) + k * np.std(self.formatted_image, ddof = 1)
        return self.formatted_image

    def slice_image(self, img: np.ndarray, density: str = 'light'):
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
    
    def adaptive_threshold_condition(self, sliced_imgs: np.ndarray) -> list:
        '''
        returns a list of booleans if a slice is above or below a threshold
        '''
        sliced_img_above_below_threshold_booleans = [None,]*len(sliced_imgs)
        for i, sliced_img in enumerate(sliced_imgs):
            mean_sliced_img_val = np.mean(sliced_img)
            if mean_sliced_img_val > self.threshold:
                sliced_img_above_below_threshold_booleans[i] = 1
            else:
                sliced_img_above_below_threshold_booleans[i] = 0
        return sliced_img_above_below_threshold_booleans

    def _plot_(self):
        '''
        Plots the original image on the left and the transformed image on the right.
        Purpose of this is to visualize the formatting done to the input image
        '''
        _, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(self.img)
        axs[0].set_title('Original')
        axs[0].axis('off')
        formatted_image = self.formatted_image.copy()
        axs[1].imshow(formatted_image)
        axs[1].set_title('Formatted')
        axs[1].axis('off')
        plt.tight_layout()
        plt.show()

# if  __name__ == "__main__":
#     img_path = r'C:\Users\baile\Documents\Software\Images_HeadlightOnOff\images\image1.webp'
#     img_ah = ActiveHeadlights(img_path)
#     img = img_ah.format_image()
#     img_slices = img_ah.slice_image(img, density='light')
#     threshold_conditions = img_ah.adaptive_threshold_condition(img_slices)

#     # #for displaying original image
#     original_img = ShowImage(img_path)
#     img_slices = original_img.slice_unfiltered_image(cv2.imread(img_path), density='light')

#     #_, axs = plt.subplots(1, 8, figsize=(10, 5))
#     for i,img in enumerate(img_slices): 
#         #axs[i].set_title(threshold_conditions[i])
#         if threshold_conditions[i] == 1:
#             img[:, :] = 0
#             img_slices[i][:,:] = 0
#         #axs[i].imshow(img)
#         #axs[i].axis('off')
#     reconstructed_img = np.hstack(img_slices)
#     plt.imshow(reconstructed_img)
#     plt.axhline(140, color = 'r')
#     plt.tight_layout()
#     plt.show()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Open default webcam (0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    img_ah = ActiveHeadlights(None)  # We'll assign frames dynamically

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Assign current frame to your object
            img_ah.img = frame

            # Process frame like before
            formatted_img = img_ah.format_image()
            img_slices = img_ah.slice_image(formatted_img, density='light')
            threshold_conditions = img_ah.adaptive_threshold_condition(img_slices)

            # Use unfiltered slices from original frame for display
            original_img = ShowImage(None)
            original_img.img = frame
            original_img.height, original_img.width = frame.shape[:2]
            original_img_slices = original_img.slice_unfiltered_image(original_img.img,density='light')

            # Black out slices where threshold condition is met
            for i, img_slice in enumerate(original_img_slices):
                if threshold_conditions[i] == 1:
                    img_slice[:, :] = 0
            
            # Reconstruct the image horizontally
            reconstructed_img = np.hstack(original_img_slices)

            # Show the result (convert BGR to RGB for matplotlib)
            plt.imshow(cv2.cvtColor(reconstructed_img, cv2.COLOR_BGR2RGB))
            plt.axhline(140, color='r')
            plt.axis('off')
            plt.pause(0.001)  # Small pause to update plot
            plt.clf()  # Clear the figure for next frame

            # Optional: stop on 'q' key press (using OpenCV window)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopped by user")

    cap.release()
    cv2.destroyAllWindows()