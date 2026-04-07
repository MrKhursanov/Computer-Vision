import cv2
import numpy as np
import matplotlib.pyplot as plt


class PuttingBasedOnArea:
    def __init__(self, image, contours=None, size=10):  # ✅ size stored as attribute
        self.image = image
        self.contours = contours
        self.size = size                                 # ✅ reusable across all methods

    def get_contour_areas(self):
        all_areas = []
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            all_areas.append(area)
        return all_areas

    def sort_and_label(self):
        print('Contour areas before sorting...')
        print(self.get_contour_areas())

        sorted_contours = sorted(self.contours, key=cv2.contourArea, reverse=True)

        print('Contour areas after sorting...')

        for i, c in enumerate(sorted_contours):
            M = cv2.moments(c)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(self.image, str(i+1), (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.drawContours(self.image, [c], -1, (255, 0, 0), 3)
        self.imshow("Sorted & Labeled Shapes")

    def imshow(self, title="Image"):                     # ✅ uses self.size instead of param
        if self.image is None:
            print("No image to display.")
            return
        h, w = self.image.shape[0], self.image.shape[1]
        aspect_ratio = w / h
        plt.figure(figsize=(self.size * aspect_ratio, self.size))  # ✅ self.size
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.show()

    def gray_scaled(self):
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = self.image.shape[0], self.image.shape[1]
        aspect_ratio = w / h
        plt.figure(figsize=(self.size * aspect_ratio, self.size))  # ✅ self.size
        plt.imshow(image_gray, cmap='gray')                        # ✅ cmap='gray' for grayscale
        plt.title('Grayscaled Image')
        plt.show()
        return image_gray

    def get_canny_edged(self):
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # ✅ no side effect from gray_scaled
        edged = cv2.Canny(image_gray, 50, 255)
        h, w = self.image.shape[0], self.image.shape[1]
        aspect_ratio = w / h
        plt.figure(figsize=(self.size * aspect_ratio, self.size))  # ✅ self.size
        plt.imshow(edged, cmap='gray')                             # ✅ cmap='gray' for edges
        plt.title('Canny Edges')
        plt.show()
        return edged

    def finding_contours_using_canny(self):
        edged_image = self.get_canny_edged()
        contours, hierarchy = cv2.findContours(
            edged_image.copy(),
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_NONE
        )
        self.contours = contours
        output = self.image.copy()
        cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
        h, w = self.image.shape[0], self.image.shape[1]
        aspect_ratio = w / h
        plt.figure(figsize=(self.size * aspect_ratio, self.size))  # ✅ self.size
        plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        plt.title('Contours overlaid on the shapes')
        plt.show()


# --- Usage ---
# img = cv2.imread('your_image.png')
# processor = PuttingBasedOnArea(img, size=10)
# processor.imshow()
# processor.gray_scaled()
# processor.get_canny_edged()
# processor.finding_contours_using_canny()
# processor.sort_and_label()