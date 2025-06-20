import tkinter as tk
from db.database import get_all_users, create_tables

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My SQLite App")

        create_tables()  # Ensure tables exist

        self.label = tk.Label(self.root, text="Users:")
        self.label.pack()

        users = get_all_users()
        for user in users:
            tk.Label(self.root, text=user[0]).pack()

    def run(self):
        self.root.mainloop()