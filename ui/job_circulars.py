# pages/job_circulars.py
import tkinter as tk
from tkinter import messagebox
from database.db import get_all_jobs, save_job
import os


class JobCirculars(tk.Frame):
    def __init__(self, parent, uid):
        super().__init__(parent, bg="#F4F6F9")

        self.uid = uid

        self.jobs = get_all_jobs()
        self.active_filter = "All"

        self._build_top_bar()
        self._build_filter_bar()
        self._build_scroll_area()

        self.display_jobs(self.jobs)


    # TOP BAR — Title + Search

    def _build_top_bar(self):
        top = tk.Frame(self, bg="#1A73E8", pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Job Circulars",
                 font=("Arial", 18, "bold"),
                 bg="#1A73E8", fg="white").pack(side="left", padx=20)

        # Search box (right side)
        search_frame = tk.Frame(top, bg="#1A73E8")
        search_frame.pack(side="right", padx=20)

        self.search_entry = tk.Entry(search_frame,
                                     font=("Arial", 11),
                                     width=28,
                                     relief="flat",
                                     bd=5)
        self.search_entry.pack(side="left", ipady=4)
        self.search_entry.insert(0, "Search jobs...")
        self.search_entry.bind("<FocusIn>", self._clear_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_placeholder)
        self.search_entry.bind("<KeyRelease>", lambda e: self._apply_filters())

        tk.Button(search_frame, text="🔍",
                  font=("Arial", 14),
                  relief="flat",
                  bg="white",
                  command=self._apply_filters).pack(side="left")

    def _clear_placeholder(self, event):
        if self.search_entry.get() == "Search jobs...":
            self.search_entry.delete(0, "end")

    def _restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search jobs...")


    # FILTER BAR — Full-time / Part-time / All

    def _build_filter_bar(self):
        bar = tk.Frame(self, bg="#E8EDF3", pady=8)
        bar.pack(fill="x", padx=10)

        tk.Label(bar, text="Filter:",
                 font=("Arial", 10, "bold"),
                 bg="#E8EDF3").pack(side="left", padx=10)

        self.filter_buttons = {}
        filters = ["All", "Full-time", "Part-time"]

        for f in filters:
            btn = tk.Button(bar, text=f,
                            font=("Arial", 9),
                            relief="flat",
                            padx=12, pady=4,
                            cursor="hand2",
                            command=lambda x=f: self._set_filter(x))
            btn.pack(side="left", padx=4)
            self.filter_buttons[f] = btn

        self._highlight_filter("All")

    def _set_filter(self, filter_name):
        self.active_filter = filter_name
        self._highlight_filter(filter_name)
        self._apply_filters()

    def _highlight_filter(self, active):
        colors = {
            "active_bg": "#1A73E8",
            "active_fg": "white",
            "inactive_bg": "white",
            "inactive_fg": "#333"
        }
        for name, btn in self.filter_buttons.items():
            if name == active:
                btn.config(bg=colors["active_bg"], fg=colors["active_fg"])
            else:
                btn.config(bg=colors["inactive_bg"], fg=colors["inactive_fg"])


    # SCROLL AREA

    def _build_scroll_area(self):
        container = tk.Frame(self, bg="#F4F6F9")
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="#F4F6F9", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical",
                                  command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.content_frame = tk.Frame(self.canvas, bg="#F4F6F9")
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    # FILTER LOGIC

    def _apply_filters(self):
        query = self.search_entry.get().lower()
        if query == "search jobs...":
            query = ""

        filtered = []
        for job in self.jobs:
            # Search filter
            match_search = (
                query in job["title"].lower() or
                query in job["company"].lower() or
                query in job["location"].lower() or
                query in job["skills_required"].lower()
            )
            # Type filter
            match_type = (
                self.active_filter == "All" or
                job["job_type"] == self.active_filter
            )

            if match_search and match_type:
                filtered.append(job)

        self.display_jobs(filtered)


    # DISPLAY CARDS

    def display_jobs(self, jobs_list):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not jobs_list:
            tk.Label(self.content_frame,
                     text="No jobs found.",
                     font=("Arial", 13),
                     bg="#F4F6F9", fg="gray").pack(pady=50)
            return

        cols = 3
        for i in range(cols):
            self.content_frame.columnconfigure(i, weight=1)

        for i, job in enumerate(jobs_list):
            card = self._job_card(self.content_frame, job)
            card.grid(row=i // cols, column=i % cols,
                      padx=15, pady=15, sticky="nsew")


    # JOB CARD

    def _job_card(self, parent, job):
        card = tk.Frame(parent, bg="white", width=260, height=220,
                        highlightbackground="#DADCE0", highlightthickness=1)
        card.pack_propagate(False)
        card.grid_propagate(False)

        # Job type badge (top-right)
        badge_color = "#1A73E8" if job["job_type"] == "Full-time" else "#F29900"
        tk.Label(card, text=job["job_type"],
                 bg=badge_color, fg="white",
                 font=("Arial", 7, "bold"),
                 padx=6, pady=2).place(relx=1.0, x=-5, y=5, anchor="ne")

        # Company image
        try:
            from tkinter import PhotoImage
            img = PhotoImage(file=os.path.abspath(job["image"]))
            img_label = tk.Label(card, image=img, bg="white")
            img_label.image = img
            img_label.pack(pady=(12, 4))
        except:
            tk.Label(card, text="🏢", font=("Arial", 24), bg="white").pack(pady=(12, 4))

        # Title
        tk.Label(card, text=job["title"],
                 font=("Arial", 10, "bold"),
                 bg="white", fg="#1A1A1A",
                 wraplength=220).pack()

        # Company
        tk.Label(card, text=job["company"],
                 font=("Arial", 9), bg="white", fg="#555").pack()

        # Location + Salary row
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(pady=4)

        tk.Label(info_frame, text=f"📍 {job['location']}",
                 font=("Arial", 8), bg="white", fg="#777").pack(side="left", padx=5)

        tk.Label(info_frame, text=f"💰 {job['salary']}",
                 font=("Arial", 8), bg="white", fg="#2E7D32").pack(side="left", padx=5)

        # Deadline
        tk.Label(card, text=f"⏰ Deadline: {job['deadline']}",
                 font=("Arial", 8), bg="white", fg="#C62828").pack()

        # Click to open details
        card.bind("<Button-1>", lambda e, j=job: self.show_details(j))
        card.config(cursor="hand2")
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, j=job: self.show_details(j))
            child.config(cursor="hand2")

        return card


    # DETAIL POPUP

    def show_details(self, job):
        win = tk.Toplevel(self)
        win.title(job["title"])
        win.geometry("480x600")
        win.configure(bg="white")
        win.resizable(False, False)

        # Scrollable detail window
        canvas = tk.Canvas(win, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Image
        try:
            from tkinter import PhotoImage
            img = PhotoImage(file=os.path.abspath(job["image"]))
            lbl = tk.Label(inner, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=15)
        except:
            tk.Label(inner, text="🏢", font=("Arial", 40), bg="white").pack(pady=15)

        # Header info
        tk.Label(inner, text=job["title"],
                 font=("Arial", 15, "bold"),
                 bg="white", fg="#1A1A1A").pack()

        tk.Label(inner, text=job["company"],
                 font=("Arial", 11), bg="white", fg="#555").pack()

        # Divider
        tk.Frame(inner, bg="#DADCE0", height=1).pack(fill="x", padx=20, pady=10)

        # Info grid
        details = [
            ("📍 Location", job["location"]),
            ("💰 Salary", job["salary"]),
            ("⏰ Deadline", job["deadline"]),
            ("💼 Job Type", job["job_type"]),
            ("👥 Vacancy", str(job["vacancy"])),
        ]

        for label, value in details:
            row = tk.Frame(inner, bg="white")
            row.pack(fill="x", padx=25, pady=3)
            tk.Label(row, text=label, font=("Arial", 9, "bold"),
                     bg="white", fg="#555", width=14, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 9),
                     bg="white", fg="#1A1A1A", anchor="w").pack(side="left")

        # Divider
        tk.Frame(inner, bg="#DADCE0", height=1).pack(fill="x", padx=20, pady=10)

        # Skills
        tk.Label(inner, text="🛠 Required Skills",
                 font=("Arial", 11, "bold"),
                 bg="white", fg="#1A73E8").pack(anchor="w", padx=25)

        skills = job["skills_required"].split(",")
        skill_frame = tk.Frame(inner, bg="white")
        skill_frame.pack(fill="x", padx=25, pady=6)

        for skill in skills:
            tk.Label(skill_frame, text=skill.strip(),
                     bg="#E8F0FE", fg="#1A73E8",
                     font=("Arial", 9),
                     padx=8, pady=3,
                     relief="flat").pack(side="left", padx=3, pady=3)

        # Description
        tk.Label(inner, text="📋 Job Description",
                 font=("Arial", 11, "bold"),
                 bg="white", fg="#1A73E8").pack(anchor="w", padx=25, pady=(10, 4))

        tk.Label(inner, text=job["description"],
                 wraplength=420, justify="left",
                 font=("Arial", 10), bg="white", fg="#333").pack(padx=25)

        # Buttons
        btn_frame = tk.Frame(inner, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Save Job",
                  font=("Arial", 10, "bold"),
                  bg="#1A73E8", fg="white",
                  padx=16, pady=6,
                  relief="flat",
                  cursor="hand2",
                  command=lambda: self._save_job(job["id"], win)).pack(side="left", padx=8)

        tk.Button(btn_frame, text="🚀 Apply Now",
                  font=("Arial", 10, "bold"),
                  bg="#2E7D32", fg="white",
                  padx=16, pady=6,
                  relief="flat",
                  cursor="hand2").pack(side="left", padx=8)


    # SAVE JOB

    def _save_job(self, job_id, win):
        saved = save_job(job_id)
        if saved:
            messagebox.showinfo("Saved!", "Job saved to My Jobs ✅", parent=win)
        else:
            messagebox.showinfo("Already Saved", "This job is already in My Jobs.", parent=win)