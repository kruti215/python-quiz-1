import tkinter as tk
from tkinter import messagebox
import random

class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

class Quiz:
    def __init__(self):
        self.subjects = {}  # Dictionary to store subjects and their questions

    def add_subject(self, subject, questions):
        self.subjects[subject] = questions

class Attendance:
    def __init__(self, student_id, date, is_present=False):
        self.student_id = student_id
        self.date = date
        self.is_present = is_present

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")

        self.current_user = None
        self.students = [User("student1", "password1"), User("student2", "password2")]
        self.admin = User("admin", "adminpassword", is_admin=True)

        self.quiz_data = Quiz()
        self.quiz_data.add_subject("Math", [
            {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "correct_answer": "4"},
            {"question": "What is 5 * 5?", "options": ["20", "25", "30", "35"], "correct_answer": "25"},
            # Add more questions as needed
        ])
        self.quiz_data.add_subject("Science", [
            {"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correct_answer": "Paris"},
            {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Chloroplast", "Ribosome"], "correct_answer": "Mitochondria"},
            # Add more questions as needed
        ])

        self.attendance_data = []
        self.quiz_attempts = []

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")

        self.username_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.current_user:
            messagebox.showinfo("Logout", "You are already logged in.")
            return

        for user in self.students + [self.admin]:
            if user.username == username and user.password == password:
                self.current_user = user
                self.show_dashboard()
                return

        messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_dashboard(self):
        self.login_frame.destroy()

        dashboard_frame = tk.Frame(self.root)
        dashboard_frame.pack(padx=10, pady=10)

        tk.Label(dashboard_frame, text=f"Welcome, {self.current_user.username}!").pack()

        if self.current_user.is_admin:
            admin_button = tk.Button(dashboard_frame, text="Admin Panel", command=self.show_admin_panel)
            admin_button.pack(pady=10)
        else:
            quiz_button = tk.Button(dashboard_frame, text="Attempt Quiz", command=self.attempt_quiz)
            quiz_button.pack(pady=10)

        logout_button = tk.Button(dashboard_frame, text="Logout", command=self.logout)
        logout_button.pack()

    def show_admin_panel(self):
        admin_panel_frame = tk.Frame(self.root)
        admin_panel_frame.pack(padx=10, pady=10)

        tk.Label(admin_panel_frame, text="Admin Panel").pack()

        # Add admin panel functionality here

        back_button = tk.Button(admin_panel_frame, text="Back", command=self.show_dashboard)
        back_button.pack(pady=10)

    def attempt_quiz(self):
        if not self.current_user:
            messagebox.showinfo("Login Required", "Please log in to attempt the quiz.")
            return

        quiz_frame = tk.Frame(self.root)
        quiz_frame.pack(padx=10, pady=10)

        tk.Label(quiz_frame, text="Quiz").pack()

        # Choose a random subject
        subject = random.choice(list(self.quiz_data.subjects.keys()))

        # Shuffle the order of questions
        questions = random.sample(self.quiz_data.subjects[subject], len(self.quiz_data.subjects[subject]))

        # Initialize variables to store quiz results
        correct_answers = 0
        total_questions = len(questions)

        for idx, question in enumerate(questions, start=1):
            tk.Label(quiz_frame, text=f"Question {idx}/{total_questions}: {question['question']}").pack()

            # Display multiple-choice options
            for option in question['options']:
                tk.Radiobutton(quiz_frame, text=option, value=option, variable=tk.StringVar()).pack()

            submit_button = tk.Button(quiz_frame, text="Submit", command=lambda q=question: self.check_answer(q))
            submit_button.pack(pady=10)

            # Wait for the user to answer before proceeding to the next question
            quiz_frame.wait_window(quiz_frame)

        # Calculate the percentage
        percentage = (correct_answers / total_questions) * 100

        # Display the final score
        messagebox.showinfo("Quiz Completed", f"You answered {correct_answers} out of {total_questions} questions correctly.\nPercentage: {percentage}%")

        # Save the quiz attempt
        self.quiz_attempts.append({"user": self.current_user.username, "subject": subject, "score": correct_answers, "percentage": percentage})

        # Go back to the dashboard
        self.show_dashboard()

    def check_answer(self, question):
        # This function is called when the user submits an answer
        # You can implement the logic to check the selected option against the correct answer
        # For simplicity, this code assumes the first option is the correct answer
        selected_option = tk.StringVar().get()
        correct_answer = question['options'][0]  # Assume the first option is correct

        if selected_option == correct_answer:
            messagebox.showinfo("Quiz Result", "Correct! You answered the question correctly.")
            self.root.quit()  # Close the quiz frame and proceed to the next question
        else:
            messagebox.showinfo("Quiz Result", "Incorrect. Please review the question and try again.")

    def logout(self):
        self.current_user = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
