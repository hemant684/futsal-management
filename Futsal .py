import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class FutsalManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Futsal Management System")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Apply a modern theme and styling using ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("Header.TLabel", font=("Helvetica", 18, "bold"))
        
        self.current_user = None
        self.users = []
        self.futsals = []
        self.bookings = []
        
        # Main container for frames
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainMenu, RegisterFrame, LoginFrame, UserMenu, OwnerMenu, AdminMenu):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("MainMenu")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="30 30 30 30")
        self.controller = controller
        header = ttk.Label(self, text="Futsal Management System", style="Header.TLabel")
        header.pack(pady=20)
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Register", command=lambda: controller.show_frame("RegisterFrame")).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Login", command=lambda: controller.show_frame("LoginFrame")).pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Exit", command=controller.quit).pack(fill="x", pady=5)
        
class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="30 30 30 30")
        self.controller = controller
        
        header = ttk.Label(self, text="User Registration", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self, text="Role:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.role_combobox = ttk.Combobox(self, values=["user", "owner", "admin"], state="readonly")
        self.role_combobox.set("user")
        self.role_combobox.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Register", command=self.register).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame("MainMenu")).grid(row=0, column=1, padx=5)
        
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get().lower()
        
        if any(user.username == username for user in self.controller.users):
            messagebox.showerror("Error", "Username already exists!")
            return
        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        self.controller.users.append(User(username, password, role))
        messagebox.showinfo("Success", "Registration successful!")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_combobox.set("user")
        self.controller.show_frame("MainMenu")

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="30 30 30 30")
        self.controller = controller
        
        header = ttk.Label(self, text="User Login", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Login", command=self.login).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame("MainMenu")).grid(row=0, column=1, padx=5)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = next((u for u in self.controller.users if u.username == username and u.password == password), None)
        if user:
            self.controller.current_user = user
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.controller.show_frame(f"{user.role.capitalize()}Menu")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class UserMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="20 20 20 20")
        self.controller = controller
        
        header = ttk.Label(self, text="User Dashboard", style="Header.TLabel")
        header.pack(pady=10)
        
        self.tree = ttk.Treeview(self, columns=("Name", "Location", "Price"), show="headings", height=10)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Price", text="Price")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Location", width=200, anchor="center")
        self.tree.column("Price", width=150, anchor="center")
        self.tree.pack(pady=10, fill="x")
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="View Futsals", command=self.view_futsals).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Book Futsal", command=self.book_futsal).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="View Bookings", command=self.view_bookings).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Logout", command=self.logout).grid(row=0, column=3, padx=5)
        
    def on_show(self):
        self.view_futsals()
        
    def view_futsals(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for futsal in self.controller.futsals:
            self.tree.insert("", "end", values=(futsal.name, futsal.location, f"Rs.{futsal.price}/hour"))
            
    def book_futsal(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a futsal first!")
            return
        futsal_index = self.tree.index(selected)
        futsal = self.controller.futsals[futsal_index]
        time_slot = simpledialog.askstring("Booking", "Enter preferred time (HH:MM format):")
        date = simpledialog.askstring("Booking", "Enter date (YYYY-MM-DD):")
        if not time_slot or not date:
            messagebox.showerror("Error", "Time slot and date are required!")
            return
        if futsal.slots.get(time_slot, False):
            self.controller.bookings.append(Booking(self.controller.current_user, futsal, date, time_slot))
            futsal.slots[time_slot] = False
            messagebox.showinfo("Success", "Booking successful!")
        else:
            messagebox.showerror("Error", "Slot not available!")
            
    def view_bookings(self):
        bookings = [b for b in self.controller.bookings if b.user == self.controller.current_user]
        if not bookings:
            messagebox.showinfo("Info", "No bookings found!")
            return
        booking_list = "\n".join([f"{b.futsal.name} on {b.date} at {b.time_slot}" for b in bookings])
        messagebox.showinfo("Your Bookings", booking_list)
        
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("MainMenu")

class OwnerMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="30 30 30 30")
        self.controller = controller
        
        header = ttk.Label(self, text="Owner Dashboard", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self, text="Futsal Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self, text="Location:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.location_entry = ttk.Entry(self)
        self.location_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self, text="Price per hour:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Add Futsal", command=self.add_futsal).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="View My Futsals", command=self.view_futsals).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Logout", command=self.logout).grid(row=0, column=2, padx=5)
        
    def add_futsal(self):
        name = self.name_entry.get()
        location = self.location_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number!")
            return
        if not name or not location or not price:
            messagebox.showerror("Error", "All fields are required!")
            return
        self.controller.futsals.append(Futsal(name, location, price, self.controller.current_user))
        messagebox.showinfo("Success", "Futsal added successfully!")
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        
    def view_futsals(self):
        owner_futsals = [f for f in self.controller.futsals if f.owner == self.controller.current_user]
        if not owner_futsals:
            messagebox.showinfo("Info", "No futsals registered!")
            return
        futsal_list = "\n".join([f"{f.name} - {f.location} (Rs.{f.price}/hour)" for f in owner_futsals])
        messagebox.showinfo("Your Futsals", futsal_list)
        
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("MainMenu")

class AdminMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="30 30 30 30")
        self.controller = controller
        header = ttk.Label(self, text="Admin Dashboard", style="Header.TLabel")
        header.pack(pady=20)
        ttk.Label(self, text="(Under Development)", font=("Helvetica", 14)).pack(pady=10)
        ttk.Button(self, text="Logout", command=self.logout).pack(pady=10)
        
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("MainMenu")

# Domain classes
class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role

class Futsal:
    def __init__(self, name, location, price_per_hour, owner):
        self.name = name
        self.location = location
        self.price = price_per_hour
        self.owner = owner
        self.slots = {f"{hour:02}:00": True for hour in range(9, 23)}

class Booking:
    def __init__(self, user, futsal, date, time_slot):
        self.user = user
        self.futsal = futsal
        self.date = date
        self.time_slot = time_slot

if __name__ == "__main__":
    app = FutsalManagementApp()
    app.mainloop()