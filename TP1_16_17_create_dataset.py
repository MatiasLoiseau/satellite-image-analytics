import cv2
import os

# Function to select and save areas from the image
def select_and_save_areas(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at {image_path}")
        return

    # Create a copy of the image to work on
    image_copy = image.copy()

    # Store selected areas
    areas = []

    # Mouse callback function to draw rectangles
    def draw_rectangle(event, x, y, flags, param):
        nonlocal x_start, y_start, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            x_start, y_start = x, y
            drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_temp = image_copy.copy()
                cv2.rectangle(img_temp, (x_start, y_start), (x, y), (0, 255, 0), 2)
                cv2.imshow('Image', img_temp)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x_end, y_end = x, y
            areas.append((x_start, y_start, x_end, y_end))
            cv2.rectangle(image_copy, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.imshow('Image', image_copy)

    # Initialize variables
    x_start, y_start = -1, -1
    drawing = False

    # Create a window and set the mouse callback
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_rectangle)

    print("Draw rectangles around the areas you want to save. Press 's' to save and exit.")

    while True:
        cv2.imshow('Image', image_copy)
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save the selected areas and exit
        if key == ord('s'):
            break
        # Press 'q' to exit without saving
        elif key == ord('q'):
            areas = []
            break

    cv2.destroyAllWindows()

    # Save each selected area as a separate image
    if areas:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_dir = "selected_areas"
        os.makedirs(output_dir, exist_ok=True)

        for i, (x_start, y_start, x_end, y_end) in enumerate(areas):
            # Ensure coordinates are positive and correctly ordered
            x_start, x_end = sorted([x_start, x_end])
            y_start, y_end = sorted([y_start, y_end])

            # Extract the area from the image
            area = image[y_start:y_end, x_start:x_end]

            # Save the area
            output_path = os.path.join(output_dir, f"{base_name}_area_{i + 1}.tif")
            cv2.imwrite(output_path, area)
            print(f"Saved: {output_path}")

# Path to the input image
image_path = 'output/NDVI.tif'
select_and_save_areas(image_path)
