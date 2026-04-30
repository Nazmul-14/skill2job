import tkinter as tk

from ui.sidebar import Sidebar
from ui.job_circulars import JobCirculars
from ui.my_job import MyJob
from ui.profile import Profile
from ui.cv import CV
from ui.skills import Skills
from ui.pathway import Pathway
from ui.login import LoginPage
from ui.register import RegisterPage

from database.db import create_table, insert_sample_data, connect_db


# ================= DB INIT =================
def init_database():
    create_table()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        insert_sample_data()


# ================= APP =================
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Skill2BD")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(bg="#D3D3D3")

        init_database()

        # session user
        self.current_user = None

        self.container = tk.Frame(self, bg="#eeeeee")
        self.container.pack(side="right", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.sidebar = None
        self.pages = {}

        self.show_login()

    # ================= LOGIN =================
    def show_login(self):
        self.clear()

        LoginPage(
            self.container,
            self.on_login_success,
            self.show_register
        ).pack(fill="both", expand=True)

    def show_register(self):
        self.clear()

        RegisterPage(
            self.container,
            self.on_login_success,
            self.show_login
        ).pack(fill="both", expand=True)

    def on_login_success(self, user):
        self.current_user = user

        self.clear()

        # sidebar
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        self.load_pages()
        self.show_page("JobCirculars")

    # ================= PAGES =================
    def load_pages(self):
        uid = self.current_user["id"]

        self.pages = {
            "JobCirculars": JobCirculars(self.container, uid),
            "MyJob": MyJob(self.container, uid),
            "CV": CV(self.container, uid),
            "Skills": Skills(self.container, uid),
            "Pathway": Pathway(self.container, uid),
            "Profile": Profile(self.container, uid),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    # ================= NAV =================
    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            page.tkraise()

    # ================= UTILS =================
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()


# ================= RUN =================
if __name__ == "__main__":
    app = App()
    app.mainloop()