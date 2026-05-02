import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, show_page, logout_callback):
        super().__init__(parent, width=230, bg="#B9E8FF")

        self.show_page = show_page
        self.logout_callback = logout_callback

        self.pack_propagate(False)

        # ---------- LOGO ----------
        tk.Label(
            self,
            text="Skill2BD",
            bg="#42A5F5",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=20
        ).pack(fill="x", padx=10, pady=10)

        # ---------- MENU ----------
        self.create_button("Job Circulars", "JobCirculars")
        self.create_button("My Job", "MyJob")
        self.create_button("CV", "CV")
        self.create_button("My Skills", "Skills")
        self.create_button("My Pathway", "Pathway")

        # ---------- BOTTOM SECTION ----------
        bottom = tk.Frame(self, bg="#B9E8FF")
        bottom.pack(side="bottom", fill="x", pady=10)

        # Profile
        tk.Button(
            bottom,
            text="Profile",
            bg="#d9d9d9",
            font=("Arial", 12),
            command=lambda: self.show_page("Profile")
        ).pack(fill="x", padx=20, pady=5)

        # Logout
        tk.Button(
            bottom,
            text="Logout",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.logout
        ).pack(fill="x", padx=20, pady=5)

    # ---------- NAV BUTTON ----------
    def create_button(self, text, page):
        tk.Button(
            self,
            text=text,
            anchor="w",
            bg="#d9d9d9",
            activebackground="#42A5F5",
            bd=0,
            font=("Arial", 12),
            command=lambda: self.show_page(page)
        ).pack(fill="x", padx=20, pady=6)

    # ---------- LOGOUT ----------
    def logout(self):
        self.logout_callback()