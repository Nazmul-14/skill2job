import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os


class Profile(tk.Frame):

    def __init__(self, parent, user_id):
        super().__init__(parent, bg="#eeeeee")

        self.user_id = user_id
        self.entries = {}
        self.photo_path = None
        self.profile_img = None

        #  USER-WISE FILE PATH
        self.DATA_DIR = os.path.join("data", "profiles")
        self.DATA_FILE = os.path.join(
            self.DATA_DIR, f"profile_{self.user_id}.json"
        )

        self._build_scroll_layout()
        self._build_card()
        self._load_profile()

    # ================= SCROLL SYSTEM =================
    def _build_scroll_layout(self):

        self.canvas = tk.Canvas(self, bg="#eeeeee", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.wrapper = tk.Frame(self.canvas, bg="#eeeeee")

        self.window = self.canvas.create_window(
            (0, 0), window=self.wrapper, anchor="n"
        )

        self.wrapper.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.window, width=e.width)
        )

        #   MOUSE SCROLL
        self._bind_mousewheel()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_mousewheel(self):
        self.canvas.bind(
            "<Enter>",
            lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        )
        self.canvas.bind(
            "<Leave>",
            lambda e: self.canvas.unbind_all("<MouseWheel>")
        )

    # ================= CARD =================
    def _build_card(self):

        self.wrapper.columnconfigure(0, weight=1)

        self.card = tk.Frame(
            self.wrapper,
            bg="white",
            padx=60,
            pady=40
        )
        self.card.grid(row=0, column=0,
                       pady=40, padx=40, sticky="nsew")

        # -------- PHOTO --------
        self.photo_label = tk.Label(self.card, bg="#8d7777")
        self.photo_label.pack(pady=20)

        placeholder = Image.new("RGB", (200, 200), "#8d7777")
        self.profile_img = ImageTk.PhotoImage(placeholder)
        self.photo_label.config(image=self.profile_img)

        tk.Button(
            self.card,
            text="Change Photo",
            command=self._change_photo
        ).pack(pady=10)

        # -------- BASIC INFO --------
        self._section("Basic Information")

        fields = [
            "Full Name", "Email", "Phone", "Location",
            "Date of Birth", "LinkedIn URL",
            "GitHub URL", "Portfolio URL"
        ]

        for field in fields:
            self._entry(field)

        # -------- EDUCATION --------
        self._section("Education")

        edu_fields = [
            "Degree", "Institution",
            "Department", "Passing Year", "CGPA"
        ]

        for field in edu_fields:
            self._entry(field)

        tk.Button(
            self.card,
            text="Save Profile",
            bg="#8d7777",
            fg="white",
            command=self._save_profile
        ).pack(pady=30)

    # ================= UI COMPONENTS =================
    def _section(self, text):
        tk.Label(
            self.card,
            text=text,
            bg="white",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(30, 10))

    def _entry(self, label):

        tk.Label(
            self.card,
            text=label,
            bg="white",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=20)

        entry = tk.Entry(self.card, font=("Arial", 11))
        entry.pack(fill="x", pady=6)

        self.entries[label] = entry

    # ================= PHOTO =================
    def _change_photo(self):

        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if path:
            self.photo_path = path

            img = Image.open(path)
            img = img.resize((200, 200))

            self.profile_img = ImageTk.PhotoImage(img)
            self.photo_label.config(image=self.profile_img)

    # ================= SAVE =================
    def _save_profile(self):

        data = {k: v.get() for k, v in self.entries.items()}
        data["photo"] = self.photo_path

        os.makedirs(self.DATA_DIR, exist_ok=True)

        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ================= LOAD =================
    def _load_profile(self):

        if not os.path.exists(self.DATA_FILE):
            return

        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return

        for k, entry in self.entries.items():
            if k in data:
                entry.insert(0, data[k])

        if data.get("photo") and os.path.exists(data["photo"]):
            self.photo_path = data["photo"]

            img = Image.open(self.photo_path)
            img = img.resize((200, 200))

            self.profile_img = ImageTk.PhotoImage(img)
            self.photo_label.config(image=self.profile_img)