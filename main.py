import tkinter as tk

from ui.sidebar import Sidebar
from ui.job_circulars import JobCirculars
from ui.profile import Profile
from ui.cv import CV
from ui.skills import Skills
from ui.pathway import Pathway
from ui.login import LoginPage
from ui.register import RegisterPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Skill2BD")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(bg="white")

        #  Current logged-in user
        self.current_user = None

        #  Main container (right side)
        self.container = tk.Frame(self, bg="#eeeeee")
        self.container.pack(side="right", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Sidebar (initially hidden)
        self.sidebar = None

        self.pages = {}

        #  Start with Login Page
        self.show_login()

    # ================= LOGIN =================
    def show_login(self):
        for w in self.container.winfo_children():
            w.destroy()

        self.login_page = LoginPage(
            self.container,
            self.on_login_success,
            self.show_register
        )
        self.login_page.pack(fill="both", expand=True)

    def show_register(self):
        for w in self.container.winfo_children():
            w.destroy()

        self.register_page = RegisterPage(
            self.container,
            self.on_login_success,  # register → login success
            self.show_login
        )
        self.register_page.pack(fill="both", expand=True)


    def on_login_success(self, user):
        self.current_user = user

        # clear login UI
        for w in self.container.winfo_children():
            w.destroy()

        # create sidebar now
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        # load main UI
        self.load_pages()

        self.show_page("JobCirculars")

    # ================= LOAD PAGES =================
    def load_pages(self):
        uid = self.current_user["id"]

        self.pages = {
            "JobCirculars": JobCirculars(self.container, uid),
            "MyJob": JobCirculars(self.container, uid),
            "CV": CV(self.container, uid),
            "Skills": Skills(self.container, uid),
            "Pathway": Pathway(self.container, uid),
            "Profile": Profile(self.container, uid),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    # ================= PAGE SWITCH =================
    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()

    # ================= LOGOUT =================
    def logout(self):
        self.current_user = None
        self.pages = {}

        # clear UI
        for w in self.container.winfo_children():
            w.destroy()

        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None

        self.show_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()