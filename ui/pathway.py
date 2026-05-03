import tkinter as tk
import json
import os
from core.data_manager import get_user_by_id


class Pathway(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent, bg="white")

        self.user_id = user_id

        # ===== FILE PATH (IMPORTANT) =====
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE = os.path.join(BASE_DIR, "..", "data", "pathway.json")

        # ===== LOAD JOB DATA =====
        self.jobs = self.load_jobs()

        # ===== TITLE =====
        tk.Label(
            self,
            text="Career Pathway",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=15)

        # ===== SEARCH =====
        tk.Label(self, text="Search Job Role", bg="white").pack()

        self.job_entry = tk.Entry(self, width=35, font=("Segoe UI", 11))
        self.job_entry.pack(pady=5)

        tk.Button(
            self,
            text="Check Job",
            bg="#3498db",
            fg="white",
            width=20,
            command=self.check_job
        ).pack(pady=5)

        # ===== OUTPUT =====
        self.output = tk.Label(
            self,
            text="",
            font=("Segoe UI", 11),
            bg="white",
            fg="#2c3e50",
            wraplength=520,
            justify="left"
        )
        self.output.pack(pady=15)

    # ================= LOAD JSON =================
    def load_jobs(self):
        try:
            with open(self.FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading pathway.json:", e)
            return {}

    # ================= MATCH LOGIC =================
    def match_skills(self, user_skills, job_skills):
        matched = []
        missing = []

        for category, skills in job_skills.items():
            user_list = user_skills.get(category, [])

            for skill in skills:
                if skill.lower() in [s.lower() for s in user_list]:
                    matched.append(skill)
                else:
                    missing.append(skill)

        return matched, missing

    # ================= CHECK JOB =================
    def check_job(self):
        search = self.job_entry.get().strip().lower()

        if not search:
            self.output.config(text="⚠️ Enter a job name")
            return

        # ===== FIND JOB (case insensitive) =====
        job_key = None
        for job in self.jobs:
            if job.lower() == search:
                job_key = job
                break

        if not job_key:
            self.output.config(text="❌ Job not found")
            return

        job_skills = self.jobs[job_key]

        # ===== GET USER SKILLS =====
        user = get_user_by_id(self.user_id)
        user_skills = user.get("skills", {})

        matched, missing = self.match_skills(user_skills, job_skills)

        # ===== RESULT =====
        if not missing:
            result = f"✅ You are READY for {job_key} 🎉"
        else:
            result = (
                f"⚠️ You are NOT READY for {job_key}\n\n"
                f"✔ Matched Skills:\n- " + "\n- ".join(matched) + "\n\n"
                f"❌ Missing Skills:\n- " + "\n- ".join(missing)
            )

        self.output.config(text=result)
        self.job_entry.delete(0, tk.END)


# ===== TEST RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pathway Test")
    root.geometry("650x500")

    Pathway(root, user_id=1).pack(fill="both", expand=True)

    root.mainloop()