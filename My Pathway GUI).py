import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

class Pathway(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title
        Label(self, text="My Pathway", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        # Goal Selection
        Label(self, text="Select Your Goal:", bg="white").pack()
        self.goal = StringVar()
        goals = ["Web Developer", "Graphic Designer", "Digital Marketer"]

        self.goal_menu = OptionMenu(self, self.goal, *goals)
        self.goal_menu.pack(pady=5)

        # Show Pathway Button
        Button(self, text="Show Pathway", command=self.show_pathway).pack(pady=10)

        # Pathway Display
        self.path_label = Label(self, text="", bg="white", justify="left")
        self.path_label.pack(pady=10)

        # Upload Section
        Label(self, text="Upload Your Work:", bg="white").pack()
        Button(self, text="Upload File", command=self.upload_file).pack(pady=5)

        # Progress
        self.progress = 0
        self.progress_label = Label(self, text="Progress: 0%", bg="white")
        self.progress_label.pack(pady=10)

        Button(self, text="Complete Step", command=self.update_progress).pack()

    def show_pathway(self):
        goal = self.goal.get()

        if goal == "Web Developer":
            path = "HTML → CSS → JavaScript → React → Project"
        elif goal == "Graphic Designer":
            path = "Photoshop → Illustrator → Branding → Portfolio"
        elif goal == "Digital Marketer":
            path = "SEO → Social Media → Ads → Campaign"
        else:
            path = "Please select a goal!"

        self.path_label.config(text=path)

    def upload_file(self):
        file = filedialog.askopenfilename()
        if file:
            messagebox.showinfo("File Selected", f"File: {file}")

    def update_progress(self):
        if self.progress < 100:
            self.progress += 20
            self.progress_label.config(text=f"Progress: {self.progress}%")
        else:
            messagebox.showinfo("Done", "Pathway Completed!")

# Main Window
root = tk.Tk()
root.title("Skill2BD - My Pathway")
root.geometry("400x450")

app = Pathway(root)
app.pack(fill="both", expand=True)

root.mainloop()
