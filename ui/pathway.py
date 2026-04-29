import tkinter as tk


class Pathway(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # ================= TITLE =================
        tk.Label(
            self,
            text="Career Pathway",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=20)

        # ================= MENU =================
        self.menu_options = [
            "1. Show Pathway",
            "2. Complete a Step",
            "3. Show Next Step",
            "4. Reset Progress"
        ]

        self.menu_label = tk.Label(
            self,
            text="\n".join(self.menu_options),
            font=("Arial", 12),
            bg="white",
            justify="left"
        )
        self.menu_label.pack(pady=10)

        # ================= INPUT =================
        self.entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.entry.pack(pady=5)

        tk.Button(
            self,
            text="Submit",
            width=15,
            command=self.handle_input
        ).pack(pady=5)

        # ================= OUTPUT =================
        self.output = tk.Label(
            self,
            text="",
            font=("Arial", 12),
            bg="white",
            fg="blue",
            wraplength=400,
            justify="left"
        )
        self.output.pack(pady=15)

        # ================= DATA =================
        self.pathway_steps = [
            "Learn Python Basics",
            "Learn Data Structures",
            "Learn Algorithms",
            "Build Projects",
            "Apply for Jobs"
        ]

        self.completed_steps = 0

        # ================= PROGRESS =================
        self.progress_label = tk.Label(
            self,
            text="Progress: 0%",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.progress_label.pack(pady=10)

    # ================= HANDLE INPUT =================
    def handle_input(self):
        choice = self.entry.get().strip()

        if choice == "1":
            self.show_pathway()

        elif choice == "2":
            self.complete_step()

        elif choice == "3":
            self.show_next_step()

        elif choice == "4":
            self.reset_progress()

        else:
            self.output.config(text="❌ Invalid choice")

        self.entry.delete(0, tk.END)

    # ================= FUNCTIONS =================

    def show_pathway(self):
        text = "📌 Full Pathway:\n\n"
        for i, step in enumerate(self.pathway_steps, 1):
            status = "✅" if i <= self.completed_steps else "⬜"
            text += f"{status} {i}. {step}\n"

        self.output.config(text=text)

    def complete_step(self):
        if self.completed_steps < len(self.pathway_steps):
            self.completed_steps += 1
            self.update_progress()
            self.output.config(text="✅ Step completed!")
        else:
            self.output.config(text="🎉 All steps completed!")

    def show_next_step(self):
        if self.completed_steps < len(self.pathway_steps):
            next_step = self.pathway_steps[self.completed_steps]
            self.output.config(text=f"➡ Next Step:\n{next_step}")
        else:
            self.output.config(text="🎉 You finished everything!")

    def reset_progress(self):
        self.completed_steps = 0
        self.update_progress()
        self.output.config(text="🔄 Progress reset!")

    def update_progress(self):
        percent = int((self.completed_steps / len(self.pathway_steps)) * 100)
        self.progress_label.config(text=f"Progress: {percent}%")