import wikipedia
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous search term. Please be more specific.\nOptions: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "No matching page found on Wikipedia."

def on_search():
    query = entry.get()
    result_text.delete(1.0, tk.END)  # Clear previous results
    result = search_wikipedia(query)
    result_text.insert(tk.END, result)

def on_voice_search():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, query)
        on_search()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Create the main window
app = tk.Tk()
app.title("Wikipedia Search App")
app.geometry("600x400")

# Style configuration
style = ttk.Style()
style.theme_use('clam')  # You can try different themes: 'clam', 'alt', 'default', 'classic'
style.configure("TButton", padding=(10, 5, 10, 5), font=('Arial', 10), background='#4CAF50', foreground='white')
style.configure("TLabel", padding=(0, 5, 0, 5), font=('Arial', 12), background='#333', foreground='white')
style.configure("TEntry", padding=(5, 5, 5, 5), font=('Arial', 10), background='white', foreground='#333')

# Create and place widgets
label = ttk.Label(app, text="Enter search term:")
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry = ttk.Entry(app, width=40)
entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

search_button = ttk.Button(app, text="Search", command=on_search)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

voice_search_button = ttk.Button(app, text="Voice Search", command=on_voice_search)
voice_search_button.grid(row=2, column=0, columnspan=2, pady=10)

result_text = tk.Text(app, height=10, width=50, wrap="word", background='#EEE', foreground='#333', font=('Arial', 10))
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
app.grid_rowconfigure(3, weight=1)
app.grid_columnconfigure(1, weight=1)

app.mainloop()
