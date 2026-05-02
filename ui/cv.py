import tkinter as tk
from tkinter import filedialog
import json, os, tempfile

import self
from PIL import Image, ImageTk, ImageDraw
from PIL import Image as PILImage

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

FILE = "cv_data.json"


def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


class CV(tk.Frame):

    def __init__(self, parent,user_id):
        super().__init__(parent, bg="white")
        self.user_id = user_id

        self.data = load_data()

        for k in ["education","skills","experience","awards","references"]:
            if not isinstance(self.data.get(k), list):
                self.data[k] = []

        self.selected_key = None
        self.selected_index = None

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        self.display = tk.Frame(container, bg="white")
        self.display.pack(side="left", fill="both", expand=True, padx=20)

        right = tk.Frame(container, bg="#ecf0f1", width=260)
        right.pack(side="right", fill="y")

        tk.Label(right, text="Edit CV", font=("Segoe UI", 14, "bold"), bg="#ecf0f1").pack(pady=10)

        self.section = tk.StringVar(value="education")
        tk.OptionMenu(right, self.section,
                      "name","title","phone","email","address","profile",
                      "education","skills","experience","awards","references"
                      ).pack(pady=5)

        self.entry = tk.Entry(right)
        self.entry.pack(pady=5)

        tk.Button(right,text="Add",bg="#27ae60",fg="white",command=self.add_item).pack(pady=2)
        tk.Button(right,text="Update",bg="#f39c12",fg="white",command=self.update_item).pack(pady=2)
        tk.Button(right,text="Delete",bg="#e74c3c",fg="white",command=self.delete_item).pack(pady=2)

        tk.Button(right,text="Upload Photo",command=self.upload).pack(pady=5)
        tk.Button(right,text="Save PDF",bg="#FF5722",fg="white",command=self.export_pdf).pack(pady=5)

        self.refresh_display()

    # ================= SELECT =================
    def select_basic(self, key, value):
        self.selected_key = key
        self.selected_index = None
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.section.set(key)

    def select_list(self, key, index, value):
        self.selected_key = key
        self.selected_index = index
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.section.set(key)

    # ================= DISPLAY =================
    def refresh_display(self):
        for w in self.display.winfo_children():
            w.destroy()

        main = tk.Frame(self.display, bg="#3c4657")
        main.pack(fill="x")

        header = tk.Frame(main, bg="#3c4657")
        header.pack(pady=20)

        # ===== CIRCLE IMAGE =====
        if self.data.get("photo") and os.path.exists(self.data["photo"]):
            img = Image.open(self.data["photo"]).resize((120,120))

            mask = Image.new("L", (120,120), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0,0,120,120), fill=255)

            img.putalpha(mask)
            img = ImageTk.PhotoImage(img)

            lbl = tk.Label(header, image=img, bg="#3c4657")
            lbl.image = img
            lbl.pack(side="left", padx=30)

        text = tk.Frame(header, bg="#3c4657")
        text.pack(side="left")

        name_lbl = tk.Label(text,text=self.data.get("name",""),
                            font=("Arial",28,"bold"),
                            fg="white",bg="#3c4657",cursor="hand2")
        name_lbl.pack(anchor="w")
        name_lbl.bind("<Button-1>",lambda e:self.select_basic("name",self.data.get("name","")))

        title_lbl = tk.Label(text,text=self.data.get("title",""),
                             font=("Arial",16),
                             fg="white",bg="#3c4657",cursor="hand2")
        title_lbl.pack(anchor="w")
        title_lbl.bind("<Button-1>",lambda e:self.select_basic("title",self.data.get("title","")))

        body = tk.Frame(self.display, bg="white")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body,bg="white",width=300)
        left.pack(side="left",fill="y",padx=20,pady=20)

        tk.Frame(body,width=2,bg="gray").pack(side="left",fill="y")

        right = tk.Frame(body,bg="white")
        right.pack(side="left",fill="both",expand=True,padx=20,pady=20)

        # CONTACT
        tk.Label(left,text="CONTACT",font=("Arial",14,"bold")).pack(anchor="w")

        for field,label in [("phone","Phone: "),("email","Email: "),("address","Address: ")]:
            lbl=tk.Label(left,text=label+self.data.get(field,""),cursor="hand2",wraplength=250)
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>",lambda e,f=field:self.select_basic(f,self.data.get(f,"")))

        tk.Label(left,text="").pack()

        self.draw(left,"EDUCATION","education")
        self.draw(left,"SKILLS","skills")
        self.draw(left,"AWARDS","awards")

        tk.Label(right,text="PROFILE",font=("Arial",14,"bold")).pack(anchor="w")

        profile_lbl=tk.Label(right,text=self.data.get("profile",""),
                             wraplength=500,cursor="hand2")
        profile_lbl.pack(anchor="w")
        profile_lbl.bind("<Button-1>",lambda e:self.select_basic("profile",self.data.get("profile","")))

        tk.Label(right,text="").pack()

        self.draw(right,"WORK EXPERIENCE","experience")
        self.draw(right,"REFERENCES","references")

    def draw(self,parent,title,key):
        tk.Label(parent,text=title,font=("Arial",14,"bold")).pack(anchor="w")

        for i,item in enumerate(self.data.get(key,[])):
            lbl=tk.Label(parent,text="• "+item,cursor="hand2")
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>",lambda e,k=key,i=i,val=item:self.select_list(k,i,val))

        tk.Label(parent,text="").pack()

    # ================= CRUD =================
    def add_item(self):
        key=self.section.get()
        val=self.entry.get()

        if key in ["education","skills","experience","awards","references"]:
            if val:
                self.data[key].append(val)
        else:
            self.data[key]=val

        self.entry.delete(0,tk.END)
        save_data(self.data)
        self.refresh_display()

    def update_item(self):
        if self.selected_key is None:
            return

        val=self.entry.get()

        if self.selected_key in ["education","skills","experience","awards","references"]:
            self.data[self.selected_key][self.selected_index]=val
        else:
            self.data[self.selected_key]=val

        save_data(self.data)
        self.refresh_display()

    def delete_item(self):
        if self.selected_key is None:
            return

        if self.selected_key in ["education","skills","experience","awards","references"]:
            del self.data[self.selected_key][self.selected_index]
        else:
            self.data[self.selected_key]=""

        self.selected_key=None
        self.selected_index=None
        self.entry.delete(0,tk.END)

        save_data(self.data)
        self.refresh_display()

    def upload(self):
        path=filedialog.askopenfilename(filetypes=[("Image","*.png *.jpg *.jpeg")])
        if path:
            self.data["photo"]=path
            save_data(self.data)
            self.refresh_display()

    # ================= PDF =================
    def export_pdf(self):
        path=filedialog.asksaveasfilename(defaultextension=".pdf")
        if not path:
            return

        doc=SimpleDocTemplate(path)
        content=[]

        temp_file=None

        # circle image for PDF
        if self.data.get("photo") and os.path.exists(self.data["photo"]):
            pil=PILImage.open(self.data["photo"]).convert("RGB")
            size=min(pil.size)
            pil=pil.crop((0,0,size,size))

            mask=PILImage.new("L",(size,size),0)
            draw=ImageDraw.Draw(mask)
            draw.ellipse((0,0,size,size),fill=255)
            pil.putalpha(mask)

            temp=tempfile.NamedTemporaryFile(delete=False,suffix=".png")
            pil.save(temp.name,"PNG")
            temp_file=temp.name

            img=RLImage(temp_file,width=1.3*inch,height=1.3*inch)
        else:
            img=Spacer(1,1)

        header_text=Paragraph(
            f"<b>{self.data.get('name','')}</b><br/><font size=12>{self.data.get('title','')}</font>",
            ParagraphStyle(name='h',fontSize=18,leading=22,textColor=colors.white)
        )

        header=Table([[img,header_text]],colWidths=[1.6*inch,4.4*inch])
        header.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#3c4657")),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),20),
            ('TOPPADDING',(0,0),(-1,-1),15),
            ('BOTTOMPADDING',(0,0),(-1,-1),15),
        ]))

        content.append(header)
        content.append(Spacer(1,15))

        def make(k):
            return "<br/>".join("• "+x for x in self.data.get(k,[]))

        left=Paragraph(f"""
        <b>CONTACT</b><br/>
        Phone: {self.data.get('phone','')}<br/>
        Email: {self.data.get('email','')}<br/>
        Address: {self.data.get('address','')}<br/><br/>

        <b>EDUCATION</b><br/>{make('education')}<br/><br/>
        <b>SKILLS</b><br/>{make('skills')}<br/><br/>
        <b>AWARDS</b><br/>{make('awards')}
        """,ParagraphStyle(name='l',leading=14))

        right=Paragraph(f"""
        <b>PROFILE</b><br/>{self.data.get('profile','')}<br/><br/>
        <b>WORK EXPERIENCE</b><br/>{make('experience')}<br/><br/>
        <b>REFERENCES</b><br/>{make('references')}
        """,ParagraphStyle(name='r',leading=14))

        table=Table([[left,right]],colWidths=[2.5*inch,3.5*inch])
        table.setStyle(TableStyle([
            ('LINEAFTER',(0,0),(0,-1),1,colors.grey),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))

        content.append(table)

        doc.build(content)

        if temp_file:
            os.remove(temp_file)


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1200x700")
    CV(root).pack(fill="both",expand=True)
    root.mainloop()