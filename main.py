from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from datetime import datetime
import os


class Watermarker:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("850x550")
        self.canvas = Canvas(self.window, width=807, height=400)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.window.title("Image Watermarker")
        self.window.config(padx=10, pady=10, bg="gray64")

        self.frame = Frame(self.window, width=600, height=400)
        self.frame.place(anchor='center', relx=0.5, rely=0.5)
        self.label = Label(self.frame)
        self.label.grid()

        frm = ttk.Frame(self.window, padding=10)
        frm.grid(row=1, column=0, )
        ttk.Label(frm, ).grid(column=0, row=0)
        ttk.Button(frm, text="Quit", command=self.window.destroy).grid(column=10, row=0)
        self.load_image_button = ttk.Button(frm, text="Load Image", command=self.load_image)
        self.load_image_button.grid(column=0, row=0)

        self.get_button = ttk.Button(frm, text="Watermark", command=self.water_mark, )
        self.get_button.grid(column=3, row=0)
        self.get_button = ttk.Button(frm, text='Save', command=self.save)
        self.get_button.grid(column=5, row=0)

        self.watermark_input = Label(text="Enter watermark:", font=("Ariel", 12, "italic"), bg="gray64")
        self.watermark_input.grid(column=0, row=2)
        self.watermark_input = Entry(width=16, font=("Arial", 12, "bold"), bg="antiquewhite")
        self.watermark_input.grid(column=0, row=3, columnspan=3)

        self.original_image = None
        self.image = None
        self.photo = None
        self.text = None
        self.draw = None
        self.current_dateTime = None
        self.font = None

    def load_image(self):
        image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image",
                                                filetypes=(
                                                    ("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                    ("All files", "*.*")))
        if image_path:
            self.original_image = Image.open(image_path)
            self.image = self.original_image.copy()
            self.update_canvas()

    def save(self):
        try:
            if self.image:
                save_path = filedialog.asksaveasfilename()
                # messagebox.showinfo("Help", "Save the image in its parent extension. eg., hello.png")
                if save_path:
                    self.original_image.save(save_path)
                    messagebox.showinfo("Saved", "Image saved successfully.")
            else:
                messagebox.showerror("Error", "No image to save.")

        except ValueError as e:
            messagebox.showerror("Error",
                                 "Save the image in its parent extension; "
                                 "\nname followed by the extension. eg., hello.png")
        except OSError as e:
            messagebox.showerror("Error",
                                 "Save the image in its parent extension; "
                                 "\nname followed by the extension. eg., hello.png")

    def update_canvas(self):
        if self.image:
            self.image = self.image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor='center',
                                     image=self.photo)
            self.canvas.update()

    def water_mark(self):

        if self.watermark_input.get() == "":
            messagebox.showerror("Error",
                                 "Enter watermark!!!")

        else:
            try:
                try:
                    x = self.original_image.width // 2
                    y = self.original_image.height // 2
                    self.draw = ImageDraw.Draw(self.original_image)
                    self.current_dateTime = datetime.now()
                    self.text = f"{self.watermark_input.get()} (c) {self.current_dateTime.year}"
                    self.font = ImageFont.truetype("arial.ttf", 40)
                    self.draw.text((x, y), self.text, fill=(179, 150, 148), font=self.font, align='center')

                except AttributeError as e:
                    messagebox.showerror("Error",
                                         "Load the image!")

            finally:
                try:
                    x_ = self.image.width / 2
                    y_ = self.image.height / 2
                    self.draw = ImageDraw.Draw(self.image)
                    self.current_dateTime = datetime.now()
                    self.text = f"{self.watermark_input.get()} (c) {self.current_dateTime.year}"
                    self.font = ImageFont.truetype("arial.ttf", 25)
                    self.draw.text((x_, y_), self.text, fill=(179, 150, 148), font=self.font, align='center')

                except:
                    pass

            self.update_canvas()

    def run(self):
        self.window.mainloop()


app = Watermarker()
app.run()
