import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil

# Folder prefixes to check
PREFIXES = (
    "RESTACKED_DWARF_RAW_TELE_",
    "RESTACKED_DWARF_RAW_WIDE_",
    "DWARF_RAW_TELE_",
    "DWARF_RAW_WIDE_"
)

def list_matching_dirs(root):
    """Return dict {folder_name: full_path} for matching dirs under root."""
    matches = {}
    for dirpath, dirnames, _ in os.walk(root):
        for d in list(dirnames):  # iterate over a copy
            if d.startswith(PREFIXES):
                matches[d] = os.path.join(dirpath, d)
                # prevent walking inside this dir (avoid nested duplicates)
                dirnames.remove(d)
    return matches

def get_all_files(root):
    """Return set of relative file paths under root."""
    files = set()
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            files.add(rel)
    return files

def compare_dirs(dir1, dir2):
    """Return comparison result: (files_count1, files_count2, subset, warning)."""
    files1 = get_all_files(dir1)
    files2 = get_all_files(dir2)
    n1, n2 = len(files1), len(files2)

    warning = False
    subset = None
    if files1 <= files2:
        subset = 1  # dir1 is subset of dir2
    elif files2 <= files1:
        subset = 2  # dir2 is subset of dir1
    else:
        warning = True

    return n1, n2, subset, warning

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astro Duplicate Finder")

        self.parent1 = tk.StringVar()
        self.parent2 = tk.StringVar()

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Parent Dir 1:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.parent1, width=60).grid(row=0, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_dir(self.parent1)).grid(row=0, column=2)

        ttk.Label(frame, text="Parent Dir 2:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.parent2, width=60).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=lambda: self.browse_dir(self.parent2)).grid(row=1, column=2)

        ttk.Button(frame, text="Find Duplicates", command=self.find_duplicates).grid(row=2, column=0, columnspan=3, pady=5)

        # Tree with checkbox column
        self.tree = ttk.Treeview(frame, columns=("Select", "Parent1", "Parent2", "Status"), show="headings")
        self.tree.heading("Select", text="✔")
        self.tree.heading("Parent1", text="Parent 1")
        self.tree.heading("Parent2", text="Parent 2")
        self.tree.heading("Status", text="Status")

        self.tree.column("Select", width=40, anchor="center")
        self.tree.column("Parent1", width=350)
        self.tree.column("Parent2", width=350)
        self.tree.column("Status", width=150)

        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)

        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(1, weight=1)

        # Bind click event for checkbox toggle
        self.tree.bind("<Button-1>", self.on_click)

        ttk.Button(frame, text="Delete Selected", command=self.delete_selected).grid(row=4, column=0, columnspan=3)

        # Keep row data
        self.row_data = {}  # item_id -> (dir1, dir2)

    def browse_dir(self, var):
        d = filedialog.askdirectory()
        if d:
            var.set(d)

    def find_duplicates(self):
        self.tree.delete(*self.tree.get_children())
        self.row_data.clear()

        dirs1 = list_matching_dirs(self.parent1.get())
        dirs2 = list_matching_dirs(self.parent2.get())

        duplicates = set(dirs1.keys()) & set(dirs2.keys())

        for d in sorted(duplicates):
            n1, n2, subset, warning = compare_dirs(dirs1[d], dirs2[d])
            status = "⚠️ Different files" if warning else ""

            # Decide which directory to keep
            if n1 > n2:
                keep = 1
            elif n2 > n1:
                keep = 2
            else:
                keep = subset  # could be None if identical

            # Prepare display text
            p1_text = f"{dirs1[d]} ({n1})"
            p2_text = f"{dirs2[d]} ({n2})"

            if keep == 1:
                p1_text = f"✔ {p1_text}"
            elif keep == 2:
                p2_text = f"✔ {p2_text}"

            # Insert row (all default color)
            item_id = self.tree.insert("", "end", values=("☐", p1_text, p2_text, status))
            self.row_data[item_id] = (dirs1[d], dirs2[d])

    def on_click(self, event):
        """Toggle checkbox when clicking in Select column"""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        if col != "#1":  # Only "Select" column
            return
        row = self.tree.identify_row(event.y)
        if not row:
            return

        current = self.tree.set(row, "Select")
        new_val = "☑" if current == "☐" else "☐"
        self.tree.set(row, "Select", new_val)

    def delete_selected(self):
        to_delete = []
        for item in self.tree.get_children():
            if self.tree.set(item, "Select") == "☑":
                dir1, dir2 = self.row_data[item]
                # find which one to delete
                p1_text, p2_text, status = self.tree.item(item, "values")[1:4]

                if "✔" in p1_text and "✔" not in p2_text:
                    to_delete.append(dir2)
                elif "✔" in p2_text and "✔" not in p1_text:
                    to_delete.append(dir1)
                else:
                    # identical: decide policy (e.g. delete Parent2 copy)
                    to_delete.append(dir2)

        if not to_delete:
            messagebox.showinfo("Info", "No directories selected for deletion.")
            return

        if not messagebox.askyesno("Confirm", f"Delete {len(to_delete)} directories?"):
            return

        for d in to_delete:
            if os.path.exists(d):
                shutil.rmtree(d)

        messagebox.showinfo("Done", "Selected directories deleted.")
        self.find_duplicates()

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()
