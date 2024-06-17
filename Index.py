import random
import math
import tkinter as tk
from tkinter import messagebox, ttk, Canvas
import time
import winsound

class TrigonometryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Trig-Or-Treat?")
        self.score = 0
        self.level = 1
        self.time_limit = 30  # seconds for each question
        self.high_scores = []
        self.multiplier = 1
        self.question_types = ['function_value', 'find_angle', 'verify_identity', 'solve_equation', 'triangle_side']
        
        self.header = tk.Label(root, text="Trig-Or-Treat?", font=("Arial", 24))
        self.header.pack(pady=20)
        
        self.level_label = tk.Label(root, text=f"Level: {self.level}", font=("Arial", 16))
        self.level_label.pack(pady=5)
        
        self.question_label = tk.Label(root, text="", font=("Arial", 20))
        self.question_label.pack(pady=20)
        
        self.choices_frame = tk.Frame(root)
        self.choices_frame.pack(pady=20)
        
        self.choice_buttons = [tk.Button(self.choices_frame, text="", font=("Arial", 20), width=10) for _ in range(4)]
        for button in self.choice_buttons:
            button.pack(side=tk.LEFT, padx=5)
        
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=5)
        
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_limit}s", font=("Arial", 16))
        self.timer_label.pack(pady=5)
        
        self.hint_button = tk.Button(root, text="Hint", command=self.show_hint, font=("Arial", 16))
        self.hint_button.pack(pady=5)
        
        self.hint_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.hint_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        self.high_score_label = tk.Label(root, text="High Scores:", font=("Arial", 16))
        self.high_score_label.pack(pady=5)
        
        self.high_score_list = tk.Label(root, text="", font=("Arial", 14))
        self.high_score_list.pack(pady=5)
        
        self.canvas = Canvas(root, width=400, height=200)
        self.canvas.pack(pady=20)
        
        self.next_question()

    def generate_question(self):
        question_type = random.choice(self.question_types)
        if question_type == 'function_value':
            self.generate_function_value_question()
        elif question_type == 'find_angle':
            self.generate_find_angle_question()
        elif question_type == 'verify_identity':
            self.generate_verify_identity_question()
        elif question_type == 'solve_equation':
            self.generate_solve_equation_question()
        elif question_type == 'triangle_side':
            self.generate_triangle_side_question()

    def generate_function_value_question(self):
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        angle = random.randint(0, 360)
        func = random.choice(functions)
        self.question = f"Find {func}({angle}°)"
        self.answer = round(self.calculate_trig_function(func, angle), 2)
        self.hint = self.generate_hint(func, angle)
        self.generate_choices()

    def generate_find_angle_question(self):
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        func = random.choice(functions)
        value = round(random.uniform(-1, 1), 2) if func in ['sin', 'cos'] else round(random.uniform(-10, 10), 2)
        self.question = f"Find θ such that {func}(θ) = {value}"
        self.answer = round(math.degrees(math.asin(value)), 2) if func == 'sin' else \
                      round(math.degrees(math.acos(value)), 2) if func == 'cos' else \
                      round(math.degrees(math.atan(value)), 2) if func == 'tan' else \
                      round(math.degrees(math.acos(1/value)), 2) if func == 'sec' else \
                      round(math.degrees(math.asin(1/value)), 2) if func == 'csc' else \
                      round(math.degrees(math.atan(1/value)), 2)
        self.hint = f"Hint: Use inverse {func} to find the angle."
        self.generate_choices()
    
    def generate_verify_identity_question(self):
        identities = [
            ("sin(θ) / cos(θ)", "tan(θ)"),
            ("1 + tan^2(θ)", "sec^2(θ)"),
            ("1 + cot^2(θ)", "csc^2(θ)")
        ]
        identity = random.choice(identities)
        self.question = f"Verify the identity: {identity[0]} = {identity[1]}"
        self.answer = "True"
        self.hint = "Hint: Use trigonometric identities to verify the equation."
        self.generate_choices(identity=True)
    
    def generate_solve_equation_question(self):
        angle = random.randint(1, 359)
        equation = f"2sin({angle}°) + 1 = 0"
        self.question = f"Solve for θ: {equation}"
        self.answer = round(math.degrees(math.asin(-0.5)), 2)
        self.hint = "Hint: Isolate the trigonometric function and solve for the angle."
        self.generate_choices()
    
    def generate_triangle_side_question(self):
        angle = random.randint(1, 89)
        hypotenuse = random.randint(10, 100)
        self.question = f"Find the opposite side in a right triangle where θ = {angle}° and hypotenuse = {hypotenuse}"
        self.answer = round(hypotenuse * math.sin(math.radians(angle)), 2)
        self.hint = "Hint: Use the definition of sine in a right triangle."
        self.generate_choices()

    def calculate_trig_function(self, func, angle):
        radians = math.radians(angle)
        if func == 'sin':
            return math.sin(radians)
        elif func == 'cos':
            return math.cos(radians)
        elif func == 'tan':
            return math.tan(radians)
        elif func == 'sec':
            return 1 / math.cos(radians)
        elif func == 'csc':
            return 1 / math.sin(radians)
        elif func == 'cot':
            return 1 / math.tan(radians)

    def generate_hint(self, func, angle):
        if func == 'sin':
            return f"Hint: sin(θ) = opposite/hypotenuse"
        elif func == 'cos':
            return f"Hint: cos(θ) = adjacent/hypotenuse"
        elif func == 'tan':
            return f"Hint: tan(θ) = opposite/adjacent"
        elif func == 'sec':
            return f"Hint: sec(θ) = 1/cos(θ)"
        elif func == 'csc':
            return f"Hint: csc(θ) = 1/sin(θ)"
        elif func == 'cot':
            return f"Hint: cot(θ) = 1/tan(θ)"

    def generate_choices(self, identity=False):
        if identity:
            choices = ["True", "False", "Cannot Determine", "Not Applicable"]
        else:
            correct_index = random.randint(0, 3)
            choices = [round(self.answer + random.uniform(-2, 2), 2) for _ in range(4)]
            choices[correct_index] = self.answer
        for i, button in enumerate(self.choice_buttons):
            button.config(text=str(choices[i]), command=lambda c=choices[i]: self.check_answer(c))
    
    def next_question(self):
        self.generate_question()
        self.question_label.config(text=self.question)
        self.hint_label.config(text="")
        self.time_left = self.time_limit
        self.update_timer()
        self.progress["value"] = 0
        self.progress["maximum"] = self.time_limit

    def check_answer(self, user_answer):
        if isinstance(user_answer, str):
            correct = user_answer == self.answer
        else:
            correct = abs(user_answer - self.answer) < 0.01  # Allowing a small margin for floating-point comparison
        
        if correct:
            self.score += int(self.multiplier * (self.time_left / self.time_limit) * 10)
            self.level += 1
            winsound.Beep(1000, 200)  # Correct answer sound
            messagebox.showinfo("Result", "Correct!")
        else:
            winsound.Beep(500, 200)  # Incorrect answer sound
            messagebox.showinfo("Result", f"Incorrect! The correct answer is {self.answer}")
        self.update_score()
        self.next_question()

    def show_hint(self):
        self.hint_label.config(text=self.hint)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level}")

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.progress["value"] = self.time_limit - self.time_left
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            winsound.Beep(500, 200)  # Time's up sound
            messagebox.showinfo("Time's up!", f"Time's up! The correct answer was {self.answer}")
            self.update_high_scores()
            self.reset_game()

    def update_high_scores(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only top 5 scores
        self.high_score_list.config(text="\n".join(map(str, self.high_scores)))

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.update_score()
        self.next_question()

if __name__ == "__main__":
    root = tk.Tk()
    game = TrigonometryGame(root)
    root.mainloop()

