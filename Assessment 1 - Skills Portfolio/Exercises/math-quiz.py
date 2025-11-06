import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuiz:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Math Quiz Game")
        self.window.geometry("500x400")
        self.window.configure(bg='#f0f8ff')  # Light blue background
        
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.difficulty = None
        self.attempt = 1
        
        self.display_menu()
    
    def display_menu(self):
        """Show difficulty level menu"""
        self.clear_window()
        
        # Title
        title_label = tk.Label(self.window, text="MATH QUIZ", font=("Arial", 24, "bold"), 
                              bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.window, text="Select Difficulty Level", 
                                 font=("Arial", 14), bg='#f0f8ff', fg='#34495e')
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons with better styling
        button_style = {
            'font': ("Arial", 12, "bold"),
            'width': 15,
            'height': 2,
            'bd': 0,
            'relief': 'raised'
        }
        
        easy_btn = tk.Button(self.window, text="🎯 Easy", 
                            command=lambda: self.start_quiz("easy"),
                            bg='#2ecc71', fg='white', **button_style)
        easy_btn.pack(pady=8)
        
        moderate_btn = tk.Button(self.window, text="🎯 Moderate", 
                               command=lambda: self.start_quiz("moderate"),
                               bg='#f39c12', fg='white', **button_style)
        moderate_btn.pack(pady=8)
        
        advanced_btn = tk.Button(self.window, text="🎯 Advanced", 
                               command=lambda: self.start_quiz("advanced"),
                               bg='#e74c3c', fg='white', **button_style)
        advanced_btn.pack(pady=8)
    
    def start_quiz(self, difficulty):
        """Start the quiz with selected difficulty"""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.next_question()
    
    def random_int(self):
        """Generate random numbers based on difficulty"""
        if self.difficulty == "easy":
            return random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)
    
    def decide_operation(self):
        """Randomly choose addition or subtraction"""
        return '+' if random.randint(0, 1) == 0 else '-'
    
    def next_question(self):
        """Display next question or show results"""
        if self.current_question >= self.total_questions:
            self.display_results()
            return
        
        self.clear_window()
        self.current_question += 1
        self.attempt = 1
        
        # Generate numbers and operation
        self.num1 = self.random_int()
        self.num2 = self.random_int()
        self.operation = self.decide_operation()
        
        # Make sure subtraction doesn't give negative result
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        # Header with progress
        header_frame = tk.Frame(self.window, bg='#f0f8ff')
        header_frame.pack(pady=10)
        
        progress_label = tk.Label(header_frame, text=f"Question {self.current_question}/{self.total_questions}", 
                                 font=("Arial", 12, "bold"), bg='#f0f8ff', fg='#7f8c8d')
        progress_label.pack()
        
        score_label = tk.Label(header_frame, text=f"Score: {self.score}", 
                              font=("Arial", 12, "bold"), bg='#f0f8ff', fg='#27ae60')
        score_label.pack()
        
        # Question display
        question_frame = tk.Frame(self.window, bg='#f0f8ff')
        question_frame.pack(pady=30)
        
        question_text = f"{self.num1} {self.operation} {self.num2} = ?"
        question_label = tk.Label(question_frame, text=question_text, 
                                 font=("Arial", 28, "bold"), bg='#f0f8ff', fg='#2c3e50')
        question_label.pack()
        
        # Answer entry with better styling
        entry_frame = tk.Frame(self.window, bg='#f0f8ff')
        entry_frame.pack(pady=20)
        
        self.answer_entry = tk.Entry(entry_frame, font=("Arial", 20), width=10, 
                                   justify='center', bd=2, relief='sunken')
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda event: self.check_answer())
        
        # Submit button with better styling
        submit_btn = tk.Button(self.window, text="Submit Answer", 
                              command=self.check_answer,
                              font=("Arial", 12, "bold"),
                              bg='#3498db', fg='white',
                              width=15, height=2, bd=0)
        submit_btn.pack(pady=10)
    
    def check_answer(self):
        """Check if answer is correct"""
        try:
            user_answer = int(self.answer_entry.get())
        except:
            user_answer = None
        
        # Calculate correct answer
        if self.operation == '+':
            correct_answer = self.num1 + self.num2
        else:
            correct_answer = self.num1 - self.num2
        
        if user_answer == correct_answer:
            # Award points based on attempt
            if self.attempt == 1:
                points = 10
                self.score += 10
                messagebox.showinfo("Correct! 🎉", f"Perfect! +10 points\nYour score: {self.score}")
            else:
                points = 5
                self.score += 5
                messagebox.showinfo("Correct! 👍", f"Good! +5 points\nYour score: {self.score}")
            
            # Move to next question
            self.next_question()
        else:
            # Wrong answer
            self.attempt += 1
            if self.attempt > 2:
                # Two attempts used
                messagebox.showerror("Wrong! ❌", f"Correct answer was: {correct_answer}\nNo points awarded")
                self.next_question()
            else:
                # Second attempt
                messagebox.showwarning("Wrong! ⚠️", "Try one more time!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
    
    def display_results(self):
        """Show final results and ask to play again"""
        self.clear_window()
        
        # Calculate grade
        if self.score >= 90:
            grade = "A+ 🏆"
            color = "#f1c40f"
        elif self.score >= 80:
            grade = "A 🎯"
            color = "#27ae60"
        elif self.score >= 70:
            grade = "B 👍"
            color = "#2980b9"
        elif self.score >= 60:
            grade = "C ✅"
            color = "#8e44ad"
        else:
            grade = "D 📚"
            color = "#e74c3c"
        
        # Results display
        results_frame = tk.Frame(self.window, bg='#f0f8ff')
        results_frame.pack(expand=True)
        
        title_label = tk.Label(results_frame, text="Quiz Complete!", 
                              font=("Arial", 20, "bold"), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        score_label = tk.Label(results_frame, text=f"Final Score: {self.score}/100", 
                              font=("Arial", 18, "bold"), bg='#f0f8ff', fg='#27ae60')
        score_label.pack(pady=10)
        
        grade_label = tk.Label(results_frame, text=f"Grade: {grade}", 
                              font=("Arial", 16), bg='#f0f8ff', fg=color)
        grade_label.pack(pady=10)
        
        # Play again button
        again_btn = tk.Button(results_frame, text="Play Again", 
                             command=self.display_menu,
                             font=("Arial", 12, "bold"),
                             bg='#9b59b6', fg='white',
                             width=15, height=2, bd=0)
        again_btn.pack(pady=30)
    
    def clear_window(self):
        """Remove all widgets from window"""
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Create and run the quiz
if __name__ == "__main__":
    quiz = ArithmeticQuiz()
    quiz.run()