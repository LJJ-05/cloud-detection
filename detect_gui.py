import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import requests
import base64
import io

API_URL = "http://localhost:5000/detect"

class DetectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO能效标识检测GUI")
        self.root.geometry("800x600")
        self.image_path = None
        self.img_panel = None
        self.result_text = None
        self.create_widgets()

    def create_widgets(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="选择图片", command=self.select_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="检测", command=self.detect_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        self.img_panel = tk.Label(self.root)
        self.img_panel.pack(pady=10)

        self.result_text = tk.Text(self.root, height=10, width=90)
        self.result_text.pack(pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if path:
            self.image_path = path
            img = Image.open(path)
            img.thumbnail((500, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_panel.config(image=self.tk_img)
            self.result_text.delete(1.0, tk.END)

    def detect_image(self):
        if not self.image_path:
            messagebox.showwarning("提示", "请先选择图片！")
            return
        try:
            with open(self.image_path, "rb") as f:
                files = {"image": f}
                response = requests.post(API_URL, files=files)
            result = response.json()
            if not result.get("success"):
                self.result_text.insert(tk.END, f"检测失败: {result.get('error', '未知错误')}\n")
                return
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"检测到 {result['total_detections']} 个目标\n")
            for i, pred in enumerate(result["predictions"]):
                self.result_text.insert(tk.END, f"目标{i+1}: {pred['class_name']} 置信度: {pred['confidence']:.2f} 坐标: {pred['bbox']}\n")
            # 显示带框图片
            self.show_detected_image(result["predictions"])
        except Exception as e:
            self.result_text.insert(tk.END, f"检测失败: {e}\n")

    def show_detected_image(self, predictions):
        img = Image.open(self.image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        for pred in predictions:
            bbox = pred["bbox"]
            draw.rectangle(bbox, outline="red", width=3)
            draw.text((bbox[0], bbox[1]-10), f"{pred['class_name']} {pred['confidence']:.2f}", fill="red")
        img.thumbnail((500, 400))
        self.tk_img = ImageTk.PhotoImage(img)
        self.img_panel.config(image=self.tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectApp(root)
    root.mainloop() 