import tkinter as tk
from tkinter import messagebox
from core.data_manager import get_user_by_id, update_user


class Skills(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent, bg="#2f3e4e")

        self.user_id = user_id
        self.user = get_user_by_id(user_id)

        # ===== LOAD USER SKILLS =====
        raw_skills = self.user.get("skills", [])

        # old list → convert to category dict
        if isinstance(raw_skills, list):
            self.skills = {
                "Programming Languages": raw_skills,
                "Database": [],
                "Tools": []
            }
        else:
            self.skills = raw_skills

        self.selected_category = None
        self.selected_index = None

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== LEFT SIDE =====
        left = tk.Frame(container, bg="white")
        left.pack(side="left", fill="both", expand=True, padx=20)

        tk.Label(left, text="SKILL",
                 font=("Segoe UI", 16, "bold"),
                 bg="white", fg="#2c3e50").pack(anchor="w", pady=10)

        self.display_frame = tk.Frame(left, bg="white")
        self.display_frame.pack(fill="both", expand=True)

        # ===== RIGHT SIDE =====
        right = tk.Frame(container, bg="#ecf0f1", width=250)
        right.pack(side="right", fill="y", padx=10)

        tk.Label(right, text="Edit Skills",
                 font=("Segoe UI", 14, "bold"),
                 bg="#ecf0f1").pack(pady=15)

        # safe category init
        default_cat = list(self.skills.keys())[0] if self.skills else "Programming Languages"
        self.category = tk.StringVar(value=default_cat)

        tk.OptionMenu(right, self.category, *self.skills.keys()).pack(pady=10)

        self.entry = tk.Entry(right)
        self.entry.pack(pady=10)

        tk.Button(right, text="Add",
                  bg="#27ae60", fg="white",
                  width=18, command=self.add_skill).pack(pady=5)

        tk.Button(right, text="Update",
                  bg="#f39c12", fg="white",
                  width=18, command=self.update_skill).pack(pady=5)

        tk.Button(right, text="Delete",
                  bg="#e74c3c", fg="white",
                  width=18, command=self.delete_skill).pack(pady=5)

        self.refresh_display()

    # ===== SAVE USER =====
    def save_user(self):
        self.user["skills"] = self.skills
        update_user(self.user)

    # ===== DISPLAY =====
    def refresh_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        for category, items in self.skills.items():
            tk.Label(self.display_frame,
                     text=category.upper(),
                     font=("Segoe UI", 11, "bold"),
                     bg="white",
                     fg="#34495e").pack(anchor="w", pady=(10, 2))

            for i, item in enumerate(items):
                lbl = tk.Label(self.display_frame,
                               text="• " + item,
                               font=("Segoe UI", 10),
                               bg="white",
                               fg="#555",
                               cursor="hand2")

                lbl.pack(anchor="w", padx=10)

                lbl.bind("<Button-1>",
                         lambda e, c=category, idx=i, val=item:
                         self.select_skill(c, idx, val))

    # ===== SELECT =====
    def select_skill(self, category, index, value):
        self.selected_category = category
        self.selected_index = index

        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.category.set(category)

    # ===== ADD =====
    def add_skill(self):
        cat = self.category.get()
        skill = self.entry.get().strip()

        if not skill:
            messagebox.showwarning("Warning", "Enter skill")
            return

        if skill not in self.skills[cat]:
            self.skills[cat].append(skill)
            self.save_user()
            self.refresh_display()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Info", "Already exists")

    # ===== UPDATE =====
    def update_skill(self):
        if self.selected_category is None:
            messagebox.showwarning("Warning", "Select a skill")
            return

        new_value = self.entry.get().strip()

        if not new_value:
            messagebox.showwarning("Warning", "Enter new value")
            return

        self.skills[self.selected_category][self.selected_index] = new_value
        self.save_user()
        self.refresh_display()

    # ===== DELETE =====
    def delete_skill(self):
        if self.selected_category is None:
            messagebox.showwarning("Warning", "Select a skill")
            return

        skill = self.skills[self.selected_category][self.selected_index]

        confirm = messagebox.askyesno("Confirm", f"Delete {skill}?")
        if confirm:
            del self.skills[self.selected_category][self.selected_index]
            self.save_user()
            self.refresh_display()
            self.entry.delete(0, tk.END)
            self.selected_category = None
            self.selected_index = None


# ===== TEST RUN (optional) =====
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Skills Test")
    root.geometry("900x600")

    Skills(root, user_id=1).pack(fill="both", expand=True)

    root.mainloop()