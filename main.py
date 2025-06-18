from image_processing import ActiveHeadlights, ShowImage
from cv2 import VideoCapture, COLOR_BGR2RGB, waitKey, destroyAllWindows, line, imshow, rectangle, flip
from numpy import hstack
from datetime import datetime

if __name__ == "__main__":
    threshold_value = 0.3
    cap = VideoCapture(0)  # Open default webcam (0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    img_ah = ActiveHeadlights(None)
    original_img = ShowImage(None) 
    density = 'medium'

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Assign current frame to object
            img_ah.img = frame

            # Process frame 
            formatted_img = img_ah.format_image(threshold_scalar=threshold_value)
            img_slices = img_ah.slice_image(formatted_img, density=density)
            threshold_conditions = img_ah.adaptive_threshold_condition(img_slices)

            # Use unfiltered slices from original frame for display
            original_img.img = frame
            original_img.height, original_img.width = frame.shape[:2]
            original_img_slices = original_img.slice_unfiltered_image(original_img.img,density=density)

            # bound slices where threshold condition is met
            for i, img_slice in enumerate(original_img_slices):
                if threshold_conditions[i] == 1:
                    rectangle(img_slice, (0, 0), (img_slice.shape[1] - 1, img_slice.shape[0] - 1), (0, 255, 0), 2)
                    
            if sum(threshold_conditions) > 0:
                current_time = datetime.now().strftime('%H:%M:%S')
                try:
                    if current_time != old_currtime:
                        print(f"Bright spots detected at {current_time}")
                except NameError as error:
                    print(f"Bright spots detected at {current_time}")
                old_currtime = current_time
            
            # Reconstruct the image
            reconstructed_img = hstack(original_img_slices)

            # Optional: draw the horizontal line on the image where streetlamps would be
            line(reconstructed_img, (0, 140), (reconstructed_img.shape[1], 140), (0, 0, 255), 2)
            imshow("Processed Frame", flip(reconstructed_img,1))

            # Press 'q' to quit
            if waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopped by user")
    
    cap.release()
    destroyAllWindows()