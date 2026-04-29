import tkinter as tk

from ui.sidebar import Sidebar
from ui.job_circulars import JobCirculars
from ui.profile import Profile
from ui.cv import CV
from ui.skills import Skills
from ui.pathway import Pathway   # FIXED


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Skill2BD")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(bg="white")

        # Sidebar
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        # Container
        self.container = tk.Frame(self, bg="#eeeeee")
        self.container.pack(side="right", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self.load_pages()

        self.show_page("JobCirculars")

    def load_pages(self):
        self.pages = {
            "JobCirculars": JobCirculars(self.container),
            "MyJob": JobCirculars(self.container),
            "CV": CV(self.container),
            "Skills": Skills(self.container),
            "Pathway": Pathway(self.container),   # FIXED
            "Profile": Profile(self.container),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()