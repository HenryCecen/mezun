import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.withdraw()  # Hide the main window

def message_ok():
    messagebox.showinfo("Information", "The interface is working now!")

def message_close():
    messagebox.showwarning("Warning", "Cam and microphone are stopped!")

def message_user_role_error():
    messagebox.showwarning("Warning", "Please select role of user!")

def user_not_found():
    messagebox.showwarning("Error", "User not found!")
"""
# Show an information message box
messagebox.showinfo("Information", "This is an information message box")

# Show a warning message box
messagebox.showwarning("Warning", "This is a warning message box")

# Show an error message box
messagebox.showerror("Error", "This is an error message box")

# Show a question message box
response = messagebox.askquestion("Question", "Do you want to proceed?")
if response == 'yes':
    print("User chose to proceed")
else:
    print("User chose not to proceed")

# Show an OK/Cancel message box
response = messagebox.askokcancel("OK/Cancel", "Do you want to proceed?")
if response:
    print("User chose OK")
else:
    print("User chose Cancel")

# Show a Yes/No message box
response = messagebox.askyesno("Yes/No", "Do you want to proceed?")
if response:
    print("User chose Yes")
else:
    print("User chose No")

# Show a Retry/Cancel message box
response = messagebox.askretrycancel("Retry/Cancel", "Do you want to retry?")
if response:
    print("User chose Retry")
else:
    print("User chose Cancel")

# Close the main application window
root.quit()
"""
