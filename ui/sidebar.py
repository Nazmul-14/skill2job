import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent, width=230, bg="#e58b8b")
        self.callback = callback
        self.pack_propagate(False)

        # Logo
        tk.Label(
            self,
            text="Skill2BD",
            bg="#6b4c4c",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=20
        ).pack(fill="x", padx=10, pady=10)

        # Menu Buttons
        self.create_button("Job Circulars", "JobCirculars")
        self.create_button("My Job", "MyJob")
        self.create_button("CV", "CV")
        self.create_button("My Skills", "Skills")
        self.create_button("My Pathway", "Pathway")

        # Profile Button (Bottom)
        tk.Button(
            self,
            text="Profile",
            bg="#d9d9d9",
            font=("Arial", 12),
            command=lambda: self.callback("Profile")
        ).pack(side="bottom", fill="x", padx=20, pady=20)

    def create_button(self, text, page):
        tk.Button(
            self,
            text=text,
            anchor="w",
            bg="#e58b8b",
            activebackground="#d17f7f",
            bd=0,
            font=("Arial", 12),
            command=lambda: self.callback(page)
        ).pack(fill="x", padx=20, pady=6)