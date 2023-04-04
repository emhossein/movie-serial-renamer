import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rename Files")
        self.geometry("400x250")

        # Create a label to display the current folder path
        self.path_label = tk.Label(self, text="No folder selected")
        self.path_label.pack(pady=10)

        # Create a button to choose the folder path
        self.choose_button = tk.Button(self, text="Choose Folder", command=self.choose_folder)
        self.choose_button.pack(pady=10)

        # Create a label and entry field for the file types
        self.file_types_label = tk.Label(self, text="File Types (e.g. mp4,avi):")
        self.file_types_label.pack(pady=5)
        self.file_types_entry = tk.Entry(self)
        self.file_types_entry.pack()

        # Create a label and entry field for the prefix
        self.prefix_label = tk.Label(self, text="Prefix (optional):")
        self.prefix_label.pack(pady=5)
        self.prefix_entry = tk.Entry(self)
        self.prefix_entry.pack()

        # Create a button to rename the files
        self.rename_button = tk.Button(self, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(pady=10)

    def choose_folder(self):
        # Allow the user to choose a folder
        folder_path = filedialog.askdirectory()

        # Update the label with the chosen folder path
        self.path_label.config(text=folder_path)

    def rename_files(self):
        # Get the chosen folder path
        folder_path = self.path_label.cget("text")

        # Get the file types from the entry field
        file_types = self.file_types_entry.get().split(",")

        # Get a list of all the files in the directory with the specified types
        files = [file for file in os.listdir(folder_path) if os.path.splitext(file)[1].lstrip('.') in file_types]

        # Sort the files by name
        files.sort()

        # Loop through the files and rename them
        for file in files:
            # Extract the season and episode numbers from the file name
            match = re.search(r"S(\d+)E(\d+)", file, re.IGNORECASE)
            if match:
                season = match.group(1)
                episode = match.group(2)

                # Generate the new file name
                new_name = f"{self.prefix_entry.get()} S{season.zfill(2)}E{episode.zfill(2)}.{os.path.splitext(file)[1].lstrip('.')}"

                # Get the full path of the file
                old_path = os.path.join(folder_path, file)

                # Get the full path of the new file
                new_path = os.path.join(folder_path, new_name)

                # Rename the file
                shutil.move(old_path, new_path)

        # Show a message box to indicate that the files have been renamed
        messagebox.showinfo("Rename Files", "Files have been renamed.")

        # Show a warning message box if no files with the specified types are found
        if len(files) == 0:
            messagebox.showwarning("Rename Files", "No files found in folder.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
