import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog  
import qrcode
from PIL import Image, ImageTk

logo_path = None  

def generate_qr():
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return
    fill = color_var.get() if color_var.get() else "black"
    back = bg_color_var.get() if bg_color_var.get() else "white"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")

    if logo_path:
        try:
            logo = Image.open(logo_path)
            basewidth = 200
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.LANCZOS)
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
        except Exception as e:
            messagebox.showerror("Logo Error", f"Could not add logo:\n{e}")

    img.save("qrcode.png")
    img = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img)
    qr_label.config(image=tk_img)
    qr_label.image = tk_img

root = tk.Tk()
root.title("QR Code Generator")

title_label = tk.Label(root, text="QR Code Generator", font=("Arial", 20, "bold"))
title_label.pack(pady=15)

color_var = tk.StringVar()
bg_color_var = tk.StringVar()

def pick_color():
    color_code = colorchooser.askcolor(title="Choose QR Color")
    if color_code[1]:
        color_var.set(color_code[1])
        color_label.config(text=f"Selected Color: {color_code[1]}", bg=color_code[1])

def pick_bg_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")
    if color_code[1]:
        bg_color_var.set(color_code[1])
        bg_color_label.config(text=f"Background Color: {color_code[1]}", bg=color_code[1])

def pick_logo():
    global logo_path
    filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    path = filedialog.askopenfilename(title="Select Logo Image", filetypes=filetypes)
    if path:
        logo_path = path
        logo_label.config(text=f"Logo: {path.split('/')[-1]}")

def set_color_from_entry():
    code = color_entry.get().strip()
    if code:
        color_var.set(code)
        color_label.config(text=f"Selected Color: {code}", bg=code)

def set_bg_color_from_entry():
    code = bg_color_entry.get().strip()
    if code:
        bg_color_var.set(code)
        bg_color_label.config(text=f"Background Color: {code}", bg=code)


tk.Button(root, text="Pick QR Color", command=pick_color).pack(pady=5)
color_label = tk.Label(root, text="Selected Color: black", bg="white")
color_label.pack(pady=5)
color_entry = tk.Entry(root, width=10)
color_entry.pack(pady=2)
tk.Button(root, text="Set QR Color Code", command=set_color_from_entry).pack(pady=2)

tk.Button(root, text="Pick Background Color", command=pick_bg_color).pack(pady=5)
bg_color_label = tk.Label(root, text="Background Color: white", bg="white")
bg_color_label.pack(pady=5)
bg_color_entry = tk.Entry(root, width=10)
bg_color_entry.pack(pady=2)
tk.Button(root, text="Set BG Color Code", command=set_bg_color_from_entry).pack(pady=2)


tk.Button(root, text="Pick Logo", command=pick_logo).pack(pady=5)
logo_label = tk.Label(root, text="Logo: None")
logo_label.pack(pady=5)

tk.Label(root, text="Enter Website URL:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

entry.bind("<Return>", lambda event: generate_qr())

tk.Button(root, text="Generate QR Code", command=generate_qr).pack(pady=10)
qr_label = tk.Label(root)
qr_label.pack(pady=10)

root.mainloop()
