
self.sidebar = Sidebar(self, self.show_page)
self.sidebar.pack(side="left", fill="y")

self.container = tk.Frame(self, bg="white")
self.container.pack(side="right", fill="both", expand=True)

self.pages = {}

for Page in (JobCirculars, Profile, CV, Skills, Pathway):
    page_name = Page.__name__
    frame = Page(self.container)
    self.pages[page_name] = frame
    frame.grid(row=0, column=0, sticky="nsew")

self.show_page("JobCirculars")

def show_page(self, page_name):
    page = self.pages[page_name]
    page.tkraise()
