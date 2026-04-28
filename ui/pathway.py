class PathwaySystem:
    def __init__(self):
        self.steps = [
            "Learn Basics (Python / C / Java, Problem Solving)",
            "Intermediate Skills (DSA, OOP Concepts)",
            "Practical Skills (Projects + GitHub)",
            "Advanced Skills (MySQL, Django/Flask)",
            "Job Ready (CV + Apply for Jobs)"
        ]
        self.completed = [False] * len(self.steps)

    def show_pathway(self):
        print("\n📌 YOUR PATHWAY:\n")
        for i, step in enumerate(self.steps):
            status = "✔ Completed" if self.completed[i] else "❌ Not Done"
            print(f"{i+1}. {step} ---> {status}")

    def complete_step(self, step_no):
        if 1 <= step_no <= len(self.steps):
            self.completed[step_no - 1] = True
            print(f" Step {step_no} marked as completed!")
        else:
            print("❌ Invalid step number!")

    def next_step(self):
        for i, done in enumerate(self.completed):
            if not done:
                print(f"\n Next Step: {self.steps[i]}")
                return
        print("\n🎉 All steps completed! You are job ready!")

    def run(self):
        while True:
            print("\n===== MY PATHWAY SYSTEM =====")
            print("1. Show Pathway")
            print("2. Complete a Step")
            print("3. Show Next Step")
            print("4. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.show_pathway()

            elif choice == "2":
                step_no = int(input("Enter step number to complete: "))
                self.complete_step(step_no)

            elif choice == "3":
                self.next_step()

            elif choice == "4":
                print(" Exiting...")
                break

            else:
                print(" Invalid choice!")


# Run the system
app = PathwaySystem()
app.run()
