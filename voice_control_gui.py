import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3

# Text-to-speech
engine = pyttsx3.init()
def speak(text):
    print(f"System: {text}")
    engine.say(text)
    engine.runAndWait()

# Recognize voice
def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            command_label.config(text=f"Command: {command}")
            process_command(command)
        except sr.WaitTimeoutError:
            speak("No speech detected. Try again.")
        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that.")
        except Exception as e:
            speak(f"Error: {str(e)}")

# Device states
device_states = {
    "light": False,
    "fan": False,
    "motor": False
}

# Update GUI labels
def update_gui():
    light_status.config(text="ON" if device_states["light"] else "OFF", fg="green" if device_states["light"] else "red")
    fan_status.config(text="ON" if device_states["fan"] else "OFF", fg="green" if device_states["fan"] else "red")
    motor_status.config(text="ON" if device_states["motor"] else "OFF", fg="green" if device_states["motor"] else "red")

# Command processor
def process_command(command):
    recognized = False
    for device in device_states:
        if f"turn on {device}" in command:
            device_states[device] = True
            speak(f"{device} turned on")
            recognized = True
        elif f"turn off {device}" in command:
            device_states[device] = False
            speak(f"{device} turned off")
            recognized = True

    if "status" in command:
        show_status()
        recognized = True

    if not recognized:
        speak("Command not recognized.")
    
    update_gui()

# Show status popup
def show_status():
    status = "\n".join([f"{d.capitalize()}: {'ON' if s else 'OFF'}" for d, s in device_states.items()])
    messagebox.showinfo("Device Status", status)

# GUI Setup
root = tk.Tk()
root.title("Voice-Controlled Device Simulation")
root.geometry("400x300")
root.config(bg="white")

tk.Label(root, text="Voice-Controlled Device Automation", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
command_label = tk.Label(root, text="Command: ", font=("Arial", 12), bg="white")
command_label.pack()

device_frame = tk.Frame(root, bg="white")
device_frame.pack(pady=10)

tk.Label(device_frame, text="Light:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w")
light_status = tk.Label(device_frame, text="OFF", font=("Arial", 12), fg="red", bg="white")
light_status.grid(row=0, column=1)

tk.Label(device_frame, text="Fan:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w")
fan_status = tk.Label(device_frame, text="OFF", font=("Arial", 12), fg="red", bg="white")
fan_status.grid(row=1, column=1)

tk.Label(device_frame, text="Motor:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w")
motor_status = tk.Label(device_frame, text="OFF", font=("Arial", 12), fg="red", bg="white")
motor_status.grid(row=2, column=1)

tk.Button(root, text="🎙️ Speak Command", font=("Arial", 12), command=recognize_command, bg="#4285F4", fg="white").pack(pady=15)
tk.Button(root, text="📋 Show Status", font=("Arial", 11), command=show_status).pack()
tk.Button(root, text="❌ Exit", font=("Arial", 11), command=root.quit).pack(pady=5)

root.mainloop()
