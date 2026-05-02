import tkinter as tk
from core.data_manager import register_user


class RegisterPage(tk.Frame):
    def __init__(self, parent, on_register, go_to_login):
        super().__init__(parent, bg="white")

        self.on_register = on_register
        self.go_to_login = go_to_login

        tk.Label(self, text="Create Account",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(pady=20)

        self.name = tk.Entry(self, width=30)
        self.name.insert(0, "Name")
        self.name.pack(pady=8)

        self.email = tk.Entry(self, width=30)
        self.email.insert(0, "Email")
        self.email.pack(pady=8)

        self.password = tk.Entry(self, width=30, show="*")
        self.password.insert(0, "Password")
        self.password.pack(pady=8)

        tk.Button(self,
                  text="Register",
                  width=20,
                  bg="#2196F3",
                  fg="white",
                  command=self.do_register).pack(pady=10)

        tk.Label(self, text="Already have an account?",
                 bg="white").pack(pady=5)

        tk.Button(self,
                  text="Login",
                  bd=0,
                  fg="blue",
                  bg="white",
                  cursor="hand2",
                  command=self.go_to_login).pack()

        self.msg = tk.Label(self, text="", fg="red", bg="white")
        self.msg.pack(pady=5)

    def do_register(self):
        user = register_user(
            self.name.get(),
            self.email.get(),
            self.password.get()
        )

        if user:
            self.on_register(user)
        else:
            self.msg.config(text="Email already exists")