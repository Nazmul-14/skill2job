import tkinter as tk
from tkinter import filedialog
import json
import os
import tempfile

# IMAGE (ALL FORMAT SUPPORT)
from PIL import Image, ImageTk
from PIL import Image as PILImage

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

FILE = "cv_data.json"


# ================= LOAD =================
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}


# ================= SAVE =================
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


class CV(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.data = load_data()

        top = tk.Frame(self, bg="white")
        top.pack(fill="x", pady=10)

        tk.Button(top, text="View CV", command=self.view_cv, bg="#4CAF50", fg="white").pack(side="left", padx=10)
        tk.Button(top, text="Edit CV", command=self.edit_cv, bg="#2196F3", fg="white").pack(side="left")
        tk.Button(top, text="Save as PDF", command=self.export_pdf, bg="#FF5722", fg="white").pack(side="left", padx=10)

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.view_cv()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ================= VIEW =================
    def view_cv(self):
        self.clear()

        main = tk.Frame(self.container, bg="#3c4657")
        main.pack(fill="x")

        header = tk.Frame(main, bg="#3c4657")
        header.pack(pady=30)

        # ✅ IMAGE FIX
        if self.data.get("photo") and os.path.exists(self.data["photo"]):
            try:
                img = Image.open(self.data["photo"])
                img = img.resize((120, 120))
                img = ImageTk.PhotoImage(img)

                lbl = tk.Label(header, image=img, bg="#3c4657")
                lbl.image = img
                lbl.pack(side="left", padx=40)
            except Exception as e:
                print("Image error:", e)

        text = tk.Frame(header, bg="#3c4657")
        text.pack(side="left")

        tk.Label(text, text=self.data.get("name", ""), font=("Arial", 28, "bold"), fg="white", bg="#3c4657").pack(anchor="w")
        tk.Label(text, text=self.data.get("title", ""), font=("Arial", 16), fg="white", bg="#3c4657").pack(anchor="w")

        body = tk.Frame(self.container, bg="white")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="white", width=300)
        left.pack(side="left", fill="y", padx=20, pady=20)

        tk.Frame(body, width=2, bg="gray").pack(side="left", fill="y")

        right = tk.Frame(body, bg="white")
        right.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(left, text="CONTACT", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(left, text="📞 " + self.data.get("phone", "")).pack(anchor="w")
        tk.Label(left, text="✉️ " + self.data.get("email", "")).pack(anchor="w")
        tk.Label(left, text="🏠 " + self.data.get("address", ""), wraplength=250).pack(anchor="w")

        tk.Label(left, text="").pack()

        tk.Label(left, text="EDUCATION", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(left, text=self.data.get("education", ""), wraplength=250).pack(anchor="w")

        tk.Label(left, text="").pack()

        tk.Label(left, text="SKILLS", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(left, text=self.data.get("skills", ""), wraplength=250).pack(anchor="w")

        tk.Label(left, text="").pack()

        tk.Label(left, text="AWARDS", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(left, text=self.data.get("awards", "")).pack(anchor="w")

        tk.Label(right, text="PROFILE", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(right, text=self.data.get("profile", ""), wraplength=500).pack(anchor="w")

        tk.Label(right, text="").pack()

        tk.Label(right, text="WORK EXPERIENCE", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(right, text=self.data.get("experience", ""), wraplength=500).pack(anchor="w")

        tk.Label(right, text="").pack()

        tk.Label(right, text="REFERENCES", font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(right, text=self.data.get("references", "")).pack(anchor="w")

    # ================= EDIT =================
    def edit_cv(self):
        self.clear()

        frame = tk.Frame(self.container, bg="white")
        frame.pack(pady=20)

        self.entries = {}

        fields = [
            "name", "title", "phone", "email", "address",
            "profile", "education", "skills",
            "experience", "awards", "references"
        ]

        r = 0

        for f in fields:
            tk.Label(frame, text=f.capitalize()).grid(row=r, column=0, sticky="w")

            e = tk.Entry(frame, width=50)
            e.grid(row=r, column=1, pady=5)
            e.insert(0, self.data.get(f, ""))

            self.entries[f] = e
            r += 1

        tk.Button(frame, text="Upload Photo", command=self.upload).grid(row=r, column=0)
        tk.Button(frame, text="Save", bg="#4CAF50", fg="white", command=self.save).grid(row=r, column=1)

    def upload(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.data["photo"] = path

    def save(self):
        for k, e in self.entries.items():
            self.data[k] = e.get()

        save_data(self.data)
        self.view_cv()

    # ================= PDF EXPORT =================
    def export_pdf(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_path:
            return

        section_style = ParagraphStyle(name='section', fontSize=11, leading=14)

        content = []
        doc = SimpleDocTemplate(file_path)

        temp_file = None

        # ✅ FIXED IMAGE HANDLING
        if self.data.get("photo") and os.path.exists(self.data["photo"]):
            try:
                pil_img = PILImage.open(self.data["photo"]).convert("RGB")

                temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                pil_img.save(temp.name, "JPEG")
                temp_file = temp.name

                img = RLImage(temp_file, width=1.2*inch, height=1.2*inch)
            except Exception as e:
                print("PDF Image Error:", e)
                img = Spacer(1, 1)
        else:
            img = Spacer(1, 1)

        text_part = Paragraph(
            f"<b>{self.data.get('name','')}</b><br/>{self.data.get('title','')}",
            ParagraphStyle(
                name='header_text',
                fontSize=20,
                textColor=colors.white,
                leading=24
            )
        )

        header = Table([[img, text_part]], colWidths=[1.5*inch, 4.5*inch])

        header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#3c4657")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 20),
            ('RIGHTPADDING', (0,0), (-1,-1), 20),
            ('TOPPADDING', (0,0), (-1,-1), 20),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ]))

        content.append(header)
        content.append(Spacer(1, 15))

        left = f"""
        <b>CONTACT</b><br/>
        Phone: {self.data.get('phone','')}<br/>
        Email: {self.data.get('email','')}<br/>
        Address: {self.data.get('address','')}<br/><br/>

        <b>EDUCATION</b><br/>
        {self.data.get('education','')}<br/><br/>

        <b>SKILLS</b><br/>
        {self.data.get('skills','')}<br/><br/>

        <b>AWARDS</b><br/>
        {self.data.get('awards','')}
        """

        right = f"""
        <b>PROFILE</b><br/>
        {self.data.get('profile','')}<br/><br/>

        <b>WORK EXPERIENCE</b><br/>
        {self.data.get('experience','')}<br/><br/>

        <b>REFERENCES</b><br/>
        {self.data.get('references','')}
        """

        body = Table(
            [[Paragraph(left, section_style), Paragraph(right, section_style)]],
            colWidths=[2.5*inch, 3.5*inch]
        )

        body.setStyle(TableStyle([
            ('LINEAFTER', (0,0), (0,-1), 1, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ]))

        content.append(body)

        doc.build(content)

        # ✅ TEMP FILE DELETE
        if temp_file:
            try:
                os.remove(temp_file)
            except:
                pass


# ================= RUN =================
if __name__ == "__main__":

    root = tk.Tk()
    root.title("CV Builder")
    root.geometry("1200x700")

    app = CV(root)
    app.pack(fill="both", expand=True)

    root.mainloop()