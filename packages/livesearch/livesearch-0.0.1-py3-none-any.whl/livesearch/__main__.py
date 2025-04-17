import tkinter as tk
from tkinter import simpledialog
from . import search

class SearchApp:
    def __init__(self, root, data):
        self.data = data
        self.root = root
        self.root.title("Search App")

        self.label = tk.Label(root, text="Enter search term:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.perform_search)  # Bind key release event to perform_search

        self.results_label = tk.Label(root, text="Results:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(root, width=50, height=10)
        self.results_listbox.pack()

    def perform_search(self, event=None):
        search_term = self.entry.get()
        results = search(search_term, self.data)

        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, f"{result.item} (Confidence: {result.confidence})")

if __name__ == "__main__":
    sample_data = ["apple", "banana", "grape", "orange", "pineapple", "blueberry"]
    root = tk.Tk()
    app = SearchApp(root, sample_data)
    root.mainloop()
