import tkinter as tk
from core.data_manager import login_user


class LoginPage(tk.Frame):
    def __init__(self, parent, on_login, go_to_register):
        super().__init__(parent, bg="white")

        self.on_login = on_login
        self.go_to_register = go_to_register

        tk.Label(self, text="Login",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(pady=20)

        self.email = tk.Entry(self, width=30)
        self.email.insert(0, "Email")
        self.email.pack(pady=8)

        self.password = tk.Entry(self, width=30, show="*")
        self.password.insert(0, "Password")
        self.password.pack(pady=8)

        tk.Button(self,
                  text="Login",
                  width=20,
                  bg="#4CAF50",
                  fg="white",
                  command=self.do_login).pack(pady=10)

        # small switch
        tk.Label(self, text="Don't have an account?",
                 bg="white").pack(pady=5)

        tk.Button(self,
                  text="Register",
                  bd=0,
                  fg="blue",
                  bg="white",
                  cursor="hand2",
                  command=self.go_to_register).pack()

        self.msg = tk.Label(self, text="", fg="red", bg="white")
        self.msg.pack(pady=5)

    def do_login(self):
        email = self.email.get().strip()
        password = self.password.get().strip()

        if email in ["", "Email"] or password in ["", "Password"]:
            self.msg.config(text="Enter valid email & password")
            return

        user = login_user(email, password)

        if user:
            self.on_login(user)
        else:
            self.msg.config(text="Invalid email/password")