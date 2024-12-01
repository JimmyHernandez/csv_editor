import tkinter as tk
from tkinter import ttk
from csv_editor_single import CSVEditorSingle
from csv_editor_duo import CSVEditorDuo

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Choose an Application", font=("Helvetica", 14)).pack(pady=20)
        ttk.Button(self.root, text="CSV Editor - Single", command=self.open_csv_editor_single).pack(pady=10)
        ttk.Button(self.root, text="CSV Editor - Duo", command=self.open_csv_editor_duo).pack(pady=10)
        # Add more buttons here for other apps
        # ttk.Button(self.root, text="Another App", command=self.open_another_app).pack(pady=10)

    def open_csv_editor_single(self):
        try:
            self.root.withdraw()  # Hide the main window
            csv_selector_window = tk.Toplevel(self.root)
            CSVEditorSingle(csv_selector_window)
        except Exception as e:
            self.root.deiconify()  # Show the main window again if there's an error
            print(f"Error opening CSV Editor Single: {e}")

    def open_csv_editor_duo(self):
        try:
            self.root.withdraw()  # Hide the main window
            csv_selector_window = tk.Toplevel(self.root)
            CSVEditorDuo(csv_selector_window)
        except Exception as e:
            self.root.deiconify()  # Show the main window again if there's an error
            print(f"Error opening CSV Editor Duo: {e}")

    # Define methods to open other apps here
    # def open_another_app(self):
    #     try:
    #         self.root.withdraw()
    #         another_app_window = tk.Toplevel(self.root)
    #         AnotherApp(another_app_window)
    #     except Exception as e:
    #         self.root.deiconify()
    #         print(f"Error opening Another App: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error initializing the application: {e}")