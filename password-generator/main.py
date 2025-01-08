import mysql.connector
import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_password():
    service = service_entry.get()
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Password length must be an integer!")
        return
    
    # Generate password
    global generated_password  # To allow copying later
    generated_password = generate_password(length)
    result_label.config(text=f"Generated Password: {generated_password}", foreground="green")
    
    # Store in MySQL Database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            # port = 3306,
            user="root",
            password="db password here",
            database="passwordgenerator"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (service_name, password) VALUES (%s, %s)", (service, generated_password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"MySQL Error: {err}")

def copy_to_clipboard():
    if generated_password:
        root.clipboard_clear()
        root.clipboard_append(generated_password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")

# Initialize Tkinter root
root = tk.Tk()
root.title("Modern Password Generator")
root.geometry("400x350")
root.configure(bg="#2C3E50")

# Apply theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#3498DB", foreground="white", font=('Helvetica', 12, 'bold'), padding=10)
style.configure("TLabel", background="#2C3E50", foreground="white", font=('Helvetica', 12))
style.configure("TEntry", padding=5, font=('Helvetica', 12))
style.configure("TFrame", background="#2C3E50")

# Create frame for layout management
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# Service Name Input
ttk.Label(main_frame, text="Service Name:").pack(pady=5)
service_entry = ttk.Entry(main_frame, width=30)
service_entry.pack(pady=5)

# Password Length Input
ttk.Label(main_frame, text="Password Length:").pack(pady=5)
length_entry = ttk.Entry(main_frame, width=30)
length_entry.pack(pady=5)

# Generate and Save Button
generate_button = ttk.Button(main_frame, text="Generate & Save Password", command=save_password)
generate_button.pack(pady=10)

# Copy to Clipboard Button
copy_button = ttk.Button(main_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=10)

# Result Label
result_label = ttk.Label(main_frame, text="", font=('Helvetica', 12, 'bold'))
result_label.pack()

# Run the Tkinter event loop
root.mainloop()