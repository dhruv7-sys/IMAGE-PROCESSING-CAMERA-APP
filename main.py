import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            messagebox.showerror("Error", "Camera not found!")
            self.root.quit()

        self.capture_button = ttk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.pack_forget()

        self.bw_button = ttk.Button(root, text="Convert to Black & White", command=self.convert_to_bw)
        self.bw_button.pack_forget()

        self.erode_button = ttk.Button(root, text="Erode", command=self.erode_image)
        self.erode_button.pack_forget()

        self.dilate_button = ttk.Button(root, text="Dilate", command=self.dilate_image)
        self.dilate_button.pack_forget()

        self.hstack_button = ttk.Button(root, text="HSTACK", command=self.hstack_images)
        self.hstack_button.pack_forget()

        self.blur_button = ttk.Button(root, text="Blur", command=self.apply_blur)
        self.blur_button.pack_forget()

        self.button_combobox = ttk.Combobox(root, values=["Select an action", "Capture", "Convert to Black & White", "Erode", "Dilate", "HSTACK", "Blur"])
        self.button_combobox.pack(pady=10)
        self.button_combobox.set("Select an action")

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.update()

    def capture_image(self):
        ret, frame = self.camera.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            messagebox.showinfo("Image Captured", "Image saved as captured_image.jpg")

    def convert_to_bw(self):
        try:
            original_image = Image.open("captured_image.jpg")
            bw_image = original_image.convert("L")
            bw_image.save("bw_image.jpg")
            messagebox.showinfo("Conversion Complete", "Image converted to Black & White (bw_image.jpg)")
        except FileNotFoundError:
            messagebox.showerror("Error", "No image captured. Capture an image first.")

    def erode_image(self):
        try:
            image = cv2.imread("captured_image.jpg", cv2.IMREAD_GRAYSCALE)
            kernel = np.ones((5, 5), np.uint8)
            eroded_image = cv2.erode(image, kernel, iterations=1)
            cv2.imwrite("eroded_image.jpg", eroded_image)
            messagebox.showinfo("Erosion Complete", "Image eroded and saved as eroded_image.jpg")
        except FileNotFoundError:
            messagebox.showerror("Error", "No image captured. Capture an image first.")

    def dilate_image(self):
        try:
            image = cv2.imread("captured_image.jpg", cv2.IMREAD_GRAYSCALE)
            kernel = np.ones((5, 5), np.uint8)
            dilated_image = cv2.dilate(image, kernel, iterations=1)
            cv2.imwrite("dilated_image.jpg", dilated_image)
            messagebox.showinfo("Dilation Complete", "Image dilated and saved as dilated_image.jpg")
        except FileNotFoundError:
            messagebox.showerror("Error", "No image captured. Capture an image first.")

    def hstack_images(self):
        try:
            image1 = cv2.imread("captured_image.jpg")
            image2 = cv2.imread("bw_image.jpg")
            min_height = min(image1.shape[0], image2.shape[0])
            image1 = image1[:min_height]
            image2 = image2[:min_height]
            stacked_image = np.hstack((image1, image2))
            cv2.imwrite("hstacked_image.jpg", stacked_image)
            messagebox.showinfo("HSTACK Complete", "Images stacked horizontally and saved as hstacked_image.jpg")
        except FileNotFoundError:
            messagebox.showerror("Error", "One or both images not found. Capture and convert images first.")

    def apply_blur(self):
        try:
            image = cv2.imread("captured_image.jpg")
            blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
            cv2.imwrite("blur_image.jpg", blurred_image)
            messagebox.showinfo("Blur Complete", "Image blurred and saved as blur_image.jpg")
        except FileNotFoundError:
            messagebox.showerror("Error", "No image captured. Capture an image first.")

    def update(self):
        ret, frame = self.camera.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(10, self.update)

    def toggle_buttons(self, event):
        selected_action = self.button_combobox.get()
        if selected_action == "Capture":
            self.capture_button.pack()
            self.bw_button.pack_forget()
            self.erode_button.pack_forget()
            self.dilate_button.pack_forget()
            self.hstack_button.pack_forget()
            self.blur_button.pack_forget()
        elif selected_action == "Convert to Black & White":
            self.capture_button.pack_forget()
            self.bw_button.pack()
            self.erode_button.pack_forget()
            self.dilate_button.pack_forget()
            self.hstack_button.pack_forget()
            self.blur_button.pack_forget()
        elif selected_action == "Erode":
            self.capture_button.pack_forget()
            self.bw_button.pack_forget()
            self.erode_button.pack()
            self.dilate_button.pack_forget()
            self.hstack_button.pack_forget()
            self.blur_button.pack_forget()
        elif selected_action == "Dilate":
            self.capture_button.pack_forget()
            self.bw_button.pack_forget()
            self.erode_button.pack_forget()
            self.dilate_button.pack()
            self.hstack_button.pack_forget()
            self.blur_button.pack_forget()
        elif selected_action == "HSTACK":
            self.capture_button.pack_forget()
            self.bw_button.pack_forget()
            self.erode_button.pack_forget()
            self.dilate_button.pack_forget()
            self.hstack_button.pack()
            self.blur_button.pack_forget()
        elif selected_action == "Blur":
            self.capture_button.pack_forget()
            self.bw_button.pack_forget()
            self.erode_button.pack_forget()
            self.dilate_button.pack_forget()
            self.hstack_button.pack_forget()
            self.blur_button.pack()
        else:
            self.capture_button.pack_forget()
            self.bw_button.pack_forget()
            self.erode_button.pack_forget()
            self.dilate_button.pack_forget()
            self.hstack_button.pack_forget()
            self.blur_button.pack_forget()

    def __del__(self):
        if hasattr(self, "camera"):
            self.camera.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    app.button_combobox.bind("<<ComboboxSelected>>", app.toggle_buttons)
    root.mainloop()