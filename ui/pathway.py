import tkinter as tk

class PathwaySystem:
    def __init__(self):
        self.steps = [
            "Learn Basics (Python / C / Java)",
            "Intermediate Skills (DSA, OOP)",
            "Projects + GitHub",
            "Advanced Skills (MySQL, Django/Flask)",
            "Job Ready (CV + Apply)"
        ]
        self.completed = [False] * len(self.steps)

    def complete_step(self, index):
        if 0 <= index < len(self.steps):
            self.completed[index] = True
            return f"✅ {self.steps[index]} completed!"
        return "❌ Invalid step number"

    def complete_all_steps(self):
        self.completed = [True] * len(self.steps)
        return "🎉 All steps completed!"

    def get_progress(self):
        total = len(self.steps)
        done = sum(self.completed)
        return int((done / total) * 100)

    def get_next_step(self):
        for i in range(len(self.completed)):
            if not self.completed[i]:
                return f"➡ Next Step: {self.steps[i]}"
        return "🎉 All steps completed!"

    def reset(self):
        self.completed = [False] * len(self.steps)
        return "🔄 Progress Reset!"

    def show_all(self):
        text = ""
        for i, step in enumerate(self.steps):
            status = "✅" if self.completed[i] else "❌"
            text += f"{i+1}. {step} {status}\n"
        return text


# ===== GUI =====
app = PathwaySystem()

def submit_action():
    try:
        choice = int(choice_entry.get())

        if choice == 1:
            output.set(app.show_all())

        elif choice == 2:
            step = int(step_entry.get()) - 1
            output.set(app.complete_step(step))

        elif choice == 3:
            output.set(app.get_next_step())

        elif choice == 4:
            output.set(app.reset())

        else:
            output.set("❌ Invalid choice")

    except:
        output.set("⚠ Enter valid numbers!")

    progress_label.config(text=f"Progress: {app.get_progress()}%")


def complete_all_action():
    output.set(app.complete_all_steps())
    progress_label.config(text=f"Progress: {app.get_progress()}%")


# Window
root = tk.Tk()
root.title("Skill2BD - Career Pathway")
root.geometry("500x420")

# Title
tk.Label(root, text="Career Pathway", font=("Arial", 16, "bold")).pack(pady=10)

# Options
tk.Label(root, text="1. Show Pathway\n2. Complete a Step\n3. Show Next Step\n4. Reset Progress").pack()

# Input fields
tk.Label(root, text="Enter Choice:").pack()
choice_entry = tk.Entry(root)
choice_entry.pack()

tk.Label(root, text="Enter Step (for option 2):").pack()
step_entry = tk.Entry(root)
step_entry.pack()

# Buttons
tk.Button(root, text="Submit", command=submit_action).pack(pady=8)
tk.Button(root, text="Complete All (100%)", command=complete_all_action, bg="green", fg="white").pack(pady=5)

# Output
output = tk.StringVar()
tk.Label(root, textvariable=output, fg="blue").pack()

# Progress
progress_label = tk.Label(root, text="Progress: 0%", font=("Arial", 12, "bold"))
progress_label.pack(pady=10)

root.mainloop()
