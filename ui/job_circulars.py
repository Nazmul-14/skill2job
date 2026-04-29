import tkinter as tk
from data.job_data import jobs

class JobCirculars(tk.Frame):
    def __init__(self, parent,user_id):
        super().__init__(parent, bg="white")
        self.user_id = user_id;
        self.jobs=jobs

        # Search bar (center top)
        search = tk.Entry(
            self,
            font=("Arial", 12),
            width=50
        )
        search.pack(pady=25)

        # Cards container
        grid = tk.Frame(self, bg="white")
        grid.pack(padx=30, pady=10, fill="both", expand=True)

        cols = 4
        for i, job in enumerate(self.jobs):
            card = self._job_card(grid, job)
            card.grid(row=i//cols, column=i%cols, padx=20, pady=20)

    def _job_card(self, parent, job_data):
        card = tk.Frame(
            parent,
            width=220,
            height=140,
            bg="white",
            highlightbackground="gray",
            highlightthickness=1
        )
        card.grid_propagate(False)

        tk.Label(card, text="Job", font=("Arial", 12, "bold"), bg="white").pack(pady=8)
        tk.Label(card, text=f"Post : {job_data['title']}", bg="white").pack()
        tk.Label(card, text=job_data['company'], font=("Arial", 10, "bold"), bg="white").pack()
        tk.Label(card, text=job_data['location'], bg="white").pack()

        return card
