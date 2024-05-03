from tkinter import filedialog
import tkinter as tk
import json
import os
from asyncio import run


class DataManager:
    def __init__(self, root):
        self.root = root
        self.row = 0
        self.entries = {}
        self.data = {}
        self.load_data_from_json()

    def create_entry(self, label_text, name, isFolder=False, isBrowse=False):
        frame = tk.Frame(self.root)
        frame.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
        self.row += 1

        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=0, padx=(0, 5), pady=5)

        entry = tk.Entry(frame, width=30)
        entry.grid(row=0, column=1, padx=(0, 5), pady=5)
        entry.bind("<FocusOut>", lambda event, name=name: self.save_entry_data(event))

        # Populate entry field with loaded data if available
        if name in self.data:
            entry.insert(0, self.data[name])

        if isBrowse:

            def browse():
                if isFolder:
                    folder = filedialog.askdirectory()
                    if folder:
                        entry.delete(0, tk.END)
                        entry.insert(0, folder)
                else:
                    file = filedialog.askopenfilename()
                    if file:
                        entry.delete(0, tk.END)
                        entry.insert(0, file)
                        self.save_entry_data(None)

            button = tk.Button(frame, text="Browse", command=browse)
            button.grid(row=0, column=2, padx=(0, 5), pady=5)

        self.entries[name] = entry

        return entry

    def create_button(self, text, command, load_data):
        button = tk.Button(
            self.root, text=text, command=lambda: self.run_function(command, load_data)
        )
        button.grid(row=self.row, column=0, padx=10, pady=5)
        self.row += 1
        return button

    def create_label(self, text):
        label = tk.Label(self.root, text=text)
        label.grid(row=self.row, column=0, padx=10, pady=5)
        self.row += 1
        return label

    def save_entry_data(self, event):
        for name, entry in self.entries.items():
            value = entry.get()
            self.data[name] = value
        self.save_data_to_json(self.data)

    def save_data_to_json(self, data):
        with open("data.json", "w") as json_file:
            json.dump(data, json_file)

    def load_data_from_json(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as json_file:
                self.data = json.load(json_file)
                for name, value in self.data.items():
                    if name in self.entries:
                        self.entries[name].insert(0, value)

    def get_data(self, name):
        data = self.data.get(name, None)
        if data is not None and "//" not in data and "/" in data:
            # Assuming a forward slash is only present in URLs, not in file paths
            data = data.replace("/", "\\")
        return data

    def save_data_with_name(self, name, new_value):
        if name in self.data:
            self.data[name] = new_value
            self.save_data_to_json(self.data)

    def run_function(self, function, load_data):
        print("Running")
        self.save_entry_data(None)
        load_data()
        run(function())
        print("Done")

    def clear_entry_data(self, name):
        if name in self.entries:
            self.entries[name].delete(0, tk.END)  # Clear the entry field
            if name in self.data:
                del self.data[name]  # Remove the data associated with the name
                self.save_data_to_json(self.data)
