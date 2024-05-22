import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from urllib.request import urlopen
from collections import deque

root = tk.Tk()
root.title("Job Application Form")
root.geometry("600x600")
root.minsize(600, 600)
root.maxsize(600, 600)

def apply_background_image(window, image_url):
    try:
        response = urlopen(image_url)
        if response.status == 200:
            bg_image = Image.open(response)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(window, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            messagebox.showerror("Error", f"Failed to retrieve image: {response.status}")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open background image: {e}")
apply_background_image(root, "https://i.imghippo.com/files/wqg7T1716156458.jpg")

form_frame = tk.Frame(root, bg="#ffe6f7", bd=5, relief="ridge")
form_frame.place(relx=0.5, rely=0.5, anchor='center', width=550, height=550)
label_font = ("SF Pro", 12)
entry_font = ("SF Pro", 12)
button_font = ("SF Pro", 12)
labels = ["Name:", "Age:", "Education:", "Experience (dalam tahun):", "Skills:", "Self Traits:", "Apply for:", "3x4 Photo:"]

entries = [(tk.Entry, {}), (tk.Entry, {}), (tk.Entry, {}), (tk.Entry, {}), (tk.Text, {"height": 5, "width": 30}), (tk.Text, {"height": 3, "width": 30})]
entry_widgets = []
for i, (text, (entry_class, entry_options)) in enumerate(zip(labels, entries)):
    label = tk.Label(form_frame, text=text, font=label_font, bg="#ffe6f7", relief="flat")
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    entry = entry_class(form_frame, font=entry_font, **entry_options)
    entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
    entry_widgets.append(entry)

label_pekerjaan = tk.Label(form_frame, text=labels[6], font=label_font, bg="#ffe6f7", relief="flat")
label_pekerjaan.grid(row=6, column=0, padx=10, pady=5, sticky='w')
var_pekerjaan = tk.StringVar(value="Creative Designer")
dropdown_pekerjaan = tk.OptionMenu(form_frame, var_pekerjaan, "Creative Designer", "Art Director", "Digital Marketing")
dropdown_pekerjaan.config(font=entry_font)
dropdown_pekerjaan.grid(row=6, column=1, padx=10, pady=5, sticky='w')

def select_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.jpeg; .png")])
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((60, 100))
            img = ImageTk.PhotoImage(img)
            label_foto.config(image=img)
            label_foto.image = img
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image: {e}")
label_foto_text = tk.Label(form_frame, text=labels[7], font=label_font, bg="#ffe6f7", relief="flat")
label_foto_text.grid(row=7, column=0, padx=10, pady=5, sticky='w')
button_foto = tk.Button(form_frame, text="Select Photo", font=button_font, command=select_photo)
button_foto.grid(row=10, column=1, padx=10, pady=5, sticky='w')
label_foto = tk.Label(form_frame, bg="#ffe6f7")
label_foto.grid(row=7, column=1, padx=10, pady=5, sticky='w')

queue = deque(maxlen=10)

def submit_form():
    for widget in entry_widgets:
        if isinstance(widget, tk.Entry) and not widget.get().strip():
            messagebox.showerror("Error", "Pastikan data sudah lengkap!")
            return
        elif isinstance(widget, tk.Text) and not widget.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Data belum lengkap.")
            return
    nama = entry_widgets[0].get()
    umur = entry_widgets[1].get()
    pendidikan = entry_widgets[2].get()
    work_experience = entry_widgets[3].get()
    skills = entry_widgets[4].get("1.0", tk.END).strip()
    self_traits= entry_widgets[5].get("1.0", tk.END).strip()
    jenis_pekerjaan = var_pekerjaan.get()
    try:
        umur = int(umur)
        if umur < 21:
            messagebox.showerror("Error", "Age-requirement minimum is 21 tahun.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid age. Isi dalam bentuk angka!")
        return
    if pendidikan.lower() not in ['d4', 's1', 's2', 's3'] and int(work_experience) < 2:
        messagebox.showerror("Error", "Minimal 2 tahun work experience or D4 degree required.")
        return
    applicant_data = f"Name: {nama}\nAge: {umur}\nEducation: {pendidikan}\nWork Experience: {work_experience}\nSkills: {skills}\nSelf Traits: {self_traits}\nApply for: {jenis_pekerjaan}"
    queue.appendleft(applicant_data)
    display_queue()
    messagebox.showinfo("Success", "Selamat, Kamu lolos tahap seleksi! We've sent you an email for further information.")
button_submit = tk.Button(form_frame, text="Submit", font=button_font, command=submit_form)
button_submit.grid(row=11, column=0, columnspan=3, pady=10)

def display_queue():
    queue_content = "\n\n".join(queue)
    messagebox.showinfo("Data Applicant", queue_content)

root.mainloop()