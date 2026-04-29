import tkinter as tk

class Skills(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent, bg="white")
        self.user_id = user_id

        tk.Label(
            self,
            text="My Skills",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=40)
