import tkinter as tk
from tkinter import messagebox
import time
import threading

# Define flashcards categorized by difficulty
questions = {
    'easy': [
        {
            'question': "What is 2 + 2?",
            'options': ["3", "4", "5", "6"],
            'correctAnswer': "4"
        },
        {
            'question': "What is 5 + 3?",
            'options': ["6", "7", "8", "9"],
            'correctAnswer': "8"
        },
        {
            'question': "What is 10 - 4?",
            'options': ["5", "6", "7", "8"],
            'correctAnswer': "6"
        },
        {
            'question': "who is father of india?",
            'options': ["B.R.Ambedkar", "Mohandas karamchand gandhi", "Indira gandhi", "jawaharlal Nehru"],
            'correctAnswer': "Mohandas karamchand gandhi"
        },
        {
            'question': "longest river in kerala?",
            'options': ["periyar", "ganga", "bharathapuzha", "yamuna"],
            'correctAnswer': "periyar"
        }
    ],
    'medium': [
        {
            'question': "What is the capital of France?",
            'options': ["Berlin", "Madrid", "Paris", "Rome"],
            'correctAnswer': "Paris"
        },
        {
            'question': "Which planet is known as the Red Planet?",
            'options': ["Earth", "Mars", "Jupiter", "Saturn"],
            'correctAnswer': "Mars"
        },
        {
            'question': "What is 26 + 12?",
            'options': ["58", "48", "38", "46"],
            'correctAnswer': "38"
        },
        {
            'question': "what is the name of keralas first film studio?",
            'options': ["malayil", "udaya", "chithranjali", "navodhaya"],
            'correctAnswer': "udaya"
        },
        {
            'question': "Who wrote play Hamlet?",
            'options': ["charles dickens", "susanna hall", "Shakespere", "Arundhathi"],
            'correctAnswer': "Shakespere"
        }
    ],
    'hard': [
        {
            'question': "What is the chemical symbol for gold?",
            'options': ["Au", "Ag", "Pb", "Fe"],
            'correctAnswer': "Au"
        },
        {
            'question': "What is the square root of 144?",
            'options': ["10", "11", "12", "13"],
            'correctAnswer': "12"
        },
        {
            'question': "Who developed the theory of relativity?",
            'options': ["Newton", "Einstein", "Darwin", "Galileo"],
            'correctAnswer': "Einstein"
        }, 
        {
            'question': "which element has the atomic number 100 and is named after a famous physist?",
            'options': ["bohrium", "nobelium", "fermium", "mentelevium"],
            'correctAnswer': "fermium"
        },
        {
            'question': "which country is home to the worlds largest rainforest ?",
            'options': ["argentina", "china", "russia", "brazil"],
            'correctAnswer': "brazil"
        }


    ]
}

current_question_index = 0
score = 0
time_left = 60  # Set time limit to 60 seconds
selected_difficulty = 'easy'  # Default difficulty
timer_thread = None

# Function to update the timer every second
def update_timer():
    global time_left
    while time_left > 0:
        time.sleep(1)  # Wait for 1 second
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.update()  # Update the Tkinter window
    game_over()  # Call game over function when time is up

def load_question():
    global current_question_index
    question_data = questions[selected_difficulty][current_question_index]
    
    question_label.config(text=question_data['question'])
    
    for i, option in enumerate(question_data['options']):
        option_buttons[i].config(text=option)

def check_answer(selected_option):
    global current_question_index, score
    
    correct_answer = questions[selected_difficulty][current_question_index]['correctAnswer']
    
    if selected_option == correct_answer:
        score += 1
    
    score_label.config(text=f"Score: {score}")
    
    # Show message box to inform the user if their answer was correct or not
    if selected_option == correct_answer:
        messagebox.showinfo("Correct!", "Correct Answer!")
    else:
        messagebox.showerror("Incorrect!", f"Wrong Answer! The correct answer is {correct_answer}")
    
    # Move to the next question
    current_question_index += 1
    if current_question_index < len(questions[selected_difficulty]):
        load_question()
    else:
        game_over()

def game_over():
    """End the game and show final score."""
    messagebox.showinfo("Time's Up!", f"Game over! Your final score is {score}.")
    root.quit()  # Close the application

def start_game(difficulty):
    """Start the quiz game based on selected difficulty."""
    global selected_difficulty, current_question_index, score, time_left, timer_thread
    selected_difficulty = difficulty
    current_question_index = 0
    score = 0
    time_left = 60  # Reset time to 60 seconds for each game
    score_label.config(text=f"Score: {score}")
    timer_label.config(text=f"Time Left: {time_left}s")
    
    # Remove the difficulty selection screen and start the quiz
    difficulty_frame.pack_forget()  # Hide difficulty selection
    game_frame.pack(fill="both", expand=True)  # Show game screen
    
    # Start the timer in a separate thread
    if timer_thread and timer_thread.is_alive():
        timer_thread.join()  # Stop any previous timer thread
    timer_thread = threading.Thread(target=update_timer)
    timer_thread.daemon = True  # Ensure the thread terminates when the program exits
    timer_thread.start()

    load_question()

# Setup the main window
root = tk.Tk()
root.title("Flashcard Quiz App with Time Limit and Difficulty Levels")
root.geometry("400x300")

# Frame for difficulty selection
difficulty_frame = tk.Frame(root)
difficulty_label = tk.Label(difficulty_frame, text="Choose Difficulty Level:", font=('Arial', 14))
difficulty_label.pack(pady=10)

easy_button = tk.Button(difficulty_frame, text="Easy", width=20, font=('Arial', 12), command=lambda: start_game('easy'))
easy_button.pack(pady=5)

medium_button = tk.Button(difficulty_frame, text="Medium", width=20, font=('Arial', 12), command=lambda: start_game('medium'))
medium_button.pack(pady=5)

hard_button = tk.Button(difficulty_frame, text="Hard", width=20, font=('Arial', 12), command=lambda: start_game('hard'))
hard_button.pack(pady=5)

difficulty_frame.pack(fill="both", expand=True)  # Show difficulty selection screen

# Frame for game screen
game_frame = tk.Frame(root)

question_label = tk.Label(game_frame, text="", font=('Arial', 16), wraplength=300)
question_label.pack(pady=20)

option_buttons = []
for i in range(4):
    button = tk.Button(game_frame, text="", font=('Arial', 12), width=20, command=lambda i=i: check_answer(option_buttons[i].cget('text')))
    button.pack(pady=5)
    option_buttons.append(button)

score_label = tk.Label(game_frame, text="Score: 0", font=('Arial', 12))
score_label.pack(pady=20)

timer_label = tk.Label(game_frame, text=f"Time Left: {time_left}s", font=('Arial', 12))
timer_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
