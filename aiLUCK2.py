import cv2

def categorize_image(image_path):
    # Load the image in grayscale mode
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the average intensity of grayscale values
    average_intensity = image.mean()
    print(average_intensity)
    process_value = (average_intensity - 42)*100
    print(process_value)
    # Determine the category based on the average intensity
    if process_value < 60:
        category = "Bad"
    elif process_value < 40:
        category = "Okay"
    elif process_value < 20:
        category = "Good"
    else:
        category = "Great"

    return category

def main():
    # Replace 'your_image.png' with the path to your PNG image file
    image_path = '/Users/qiuweixiang/Desktop/waterrippledemo/Wave Propagation/waterscreenshot/fate_12.png'

    category = categorize_image(image_path)
    print(f"The image is categorized as: {category}")

if __name__ == "__main__":
    main()
