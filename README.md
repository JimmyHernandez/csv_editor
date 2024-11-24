# CSV Editor

## Overview

CSV Editor is a simple and intuitive tool for editing CSV files. It provides a user-friendly interface for selecting, viewing, and modifying CSV data. The application is built using Python and Tkinter, and it includes features such as file selection, column manipulation, bug reporting, and more.

## Features

- **File Selection**: Select and open multiple CSV files for editing.
- **Column Manipulation**: Add, delete, rename, and reorder columns.
- **About Section**: View information about the application.
- **Console Output**: View application logs and messages in a console display.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/csv-editor.git
    cd csv-editor
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    python csv_editor.py
    ```

## Usage

1. **Open the application**:
    ```sh
    python csv_editor.py
    ```

2. **Select CSV files**:
    - Use the "Select File 1" and "Select File 2" buttons to choose CSV files for editing.

    ```python
    select_button1 = ttk.Button(window, text="Select File 1", command=select_file1)
    select_button1.grid(row=2, column=1, padx=10, pady=10)

    select_button2 = ttk.Button(window, text="Select File 2", command=select_file2)
    select_button2.grid(row=2, column=2, padx=10, pady=10)
    ```

3. **Manipulate columns**:
    - Add, delete, rename, and reorder columns using the buttons provided.

    ```python
    add_button_combined = ttk.Button(button_frame, text="Agregar Columna", command=add_column_to_combined)
    add_button_combined.grid(row=0, column=0, pady=5)

    delete_button_combined = ttk.Button(button_frame, text="Eliminar Columna", command=delete_selected_column)
    delete_button_combined.grid(row=1, column=0, pady=5)
    ```

4. **Submit changes**:
    - Click the "Submit File" button to process and save your changes.

    ```python
    submit_button = ttk.Button(window, text="Submit File", command=lambda: procesar_csv(full_path_file1, [columns1[i] for i in listbox1.curselection()], full_path_file2, [columns2[i] for i in listbox2.curselection()]))
    submit_button.grid(row=5, column=3, pady=5)
    ```

5. **View application information**:
    - Click the "About" button to view details about the application.

    ```python
    about_button = ttk.Button(window, text="About", command=open_about_window)
    about_button.grid(row=9, column=0, columnspan=5, pady=10)
    ```
    
## Acknowledgements

- Tkinter - Python's standard GUI toolkit.
- smtplib - Python's library for sending emails.

## Contact

For any questions or suggestions, please contact jimoem24@gmail.com.

