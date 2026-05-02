import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, show_page_callback):
        super().__init__(parent, bg="#1f2937", width=250)
        self.show_page = show_page_callback

        self.pack_propagate(False)

        title = tk.Label(
            self,
            text="Skill2BD",
            bg="#1f2937",
            fg="white",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        self._create_button("Job Circulars")
        self._create_button("MyJob")
        self._create_button("CV")
        self._create_button("Skills")
        self._create_button("Pathway")

    def _create_button(self, name):
        btn = tk.Button(
            self,
            text=name,
            bg="#374151",
            fg="white",
            font=("Arial", 12),
            relief="flat",
            command=lambda: self.show_page(name)
        )
        btn.pack(fill="x", pady=5, padx=15)
