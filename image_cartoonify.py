import cv2
import easygui
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

image_path_global = None
cartoon_image_global = None

def upload_image():
    global image_path_global
    image_path = easygui.fileopenbox(filetypes=[["*.jpg;*.png;*.jpeg", "*.jpg;*.png;*.jpeg"]])
    if image_path:
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to load image.\nPlease select a valid image file.")
            return
        image_path_global = image_path
        img_resized = cv2.resize(img, (600, 400))
        cv2.imshow("Original Image", img_resized)
        cartoon_btn.config(state=tk.NORMAL)
        save_btn.config(state=tk.DISABLED)


def cartoonify_image():
    global cartoon_image_global
    img = cv2.imread(image_path_global)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    cartoon_image_global = cartoon
    cartoon_resized = cv2.resize(cartoon, (600, 400))
    cv2.imshow("Cartoonified Image", cartoon_resized)
    save_btn.config(state=tk.NORMAL)

def save_image():
    if cartoon_image_global is None:
        messagebox.showerror("Error", "No cartoon image to save!")
        return
    path = os.path.dirname(image_path_global)
    filename = "cartoonified_output.png"
    full_path = os.path.join(path, filename)
    cv2.imwrite(full_path, cv2.cvtColor(cartoon_image_global, cv2.COLOR_RGB2BGR))
    messagebox.showinfo("Success", f"Saved cartoon image at:\n{full_path}")

top = tk.Tk()
top.geometry("400x400")
top.title("Cartoonify App")
top.configure(bg='white')

title = tk.Label(top, text="Cartoonify Image!", font=("Arial", 18, 'bold'), bg='white')
title.pack(pady=10)

upload_btn = tk.Button(top, text="📁 Upload Image", command=upload_image,
                       bg='#0066CC', fg='white', font=('Arial', 14), padx=10, pady=5)
upload_btn.pack(pady=10)

cartoon_btn = tk.Button(top, text="🎨 Cartoonify", command=cartoonify_image,
                        bg='#28a745', fg='white', font=('Arial', 14), padx=10, pady=5,
                        state=tk.DISABLED)
cartoon_btn.pack(pady=10)

save_btn = tk.Button(top, text="💾 Save Image", command=save_image,
                     bg='#800000', fg='white', font=('Arial', 14), padx=10, pady=5,
                     state=tk.DISABLED)
save_btn.pack(pady=10)

footer = tk.Label(top, text="Made by Mehwish", bg='white', fg='gray')
footer.pack(side=tk.BOTTOM, pady=20)

top.mainloop()
