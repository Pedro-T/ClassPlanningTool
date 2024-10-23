import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Toplevel
import threading
import time
from controller.class_plan_controller import ClassPlanController
from error_handling.type_checker import check_file_type
import os

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Class Planning Tool")

        self.controller = ClassPlanController() 

        self.root.geometry("1000x600")

        self.setup_title(root)

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill='both', expand=True)
        self.setup_file_upload_buttons(main_frame)

        status_frame = ttk.Frame(root, padding="10")
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.setup_status_frame(status_frame)

        submit_frame = ttk.Frame(root)
        submit_frame.pack(fill='x', pady=10)
        self.setup_submit_button(submit_frame)

        self.degree_file_path = None
        self.study_plan_file_path = None
        self.schedule_file_path = None

        self.update_status()

    def setup_title(self, parent):
        self.title_label = ttk.Label(parent, text="Smart Class Planning Tool", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY)
        self.title_label.pack(pady=20)

    def setup_file_upload_buttons(self, parent):
        self.create_file_upload_row(parent, "Degree Requirements File:", self.upload_degree_file, 0)
        self.create_file_upload_row(parent, "Graduate Study Plan File:", self.upload_study_plan_file, 1)
        self.create_file_upload_row(parent, "4-Year Schedule File:", self.upload_schedule_file, 2)
        ttk.Label(parent, text="URL:", bootstyle="info").grid(row=3, column=0, sticky='w', padx=10, pady=10)
        self.url_entry = ttk.Entry(parent, width=40)
        self.url_entry.grid(row=3, column=1, padx=10, pady=10)

    def create_file_upload_row(self, parent, label_text, command, row):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky='w', padx=10, pady=10)
        button = ttk.Button(parent, text="Upload", command=lambda: command(button), bootstyle=PRIMARY)
        button.grid(row=row, column=1, padx=10, pady=10)
        filename_label = ttk.Label(parent, text="", bootstyle=INFO)
        filename_label.grid(row=row, column=2, sticky='w', padx=10)
        button.filename_label = filename_label

    def setup_status_frame(self, parent):
        self.status_label = ttk.Label(parent, text="Document Status:", font=("Helvetica", 14, "bold"))
        self.status_label.pack(anchor='w')
        self.status_box = ttk.Text(parent, height=6, width=80, state='disabled')
        self.status_box.pack(pady=10)

    def setup_submit_button(self, parent):
        self.submit_button = ttk.Button(parent, text="Submit & Process", command=self.submit_files, bootstyle=SUCCESS)
        self.submit_button.pack(pady=10)

    def upload_degree_file(self, button):
        file_path = filedialog.askopenfilename(title="Select Degree Requirements File")
        if not file_path:
            return
        
        if file_path and check_file_type(file_path, [".pdf"]):
            self.degree_file_path = file_path
            button.config(text="File Uploaded", bootstyle=SUCCESS)
            button.filename_label.config(text=file_path.split('/')[-1])
            messagebox.showinfo("File Selected", "Degree Requirements File uploaded successfully!",  parent=self.root)
        else:
            messagebox.showerror("Invalid File", "Please select a valid PDF file.",  parent=self.root)
            self.degree_file_path = None
            button.config(text="Upload", bootstyle=PRIMARY)
            button.filename_label.config(text="")
        self.update_status()
        
    def upload_study_plan_file(self, button):
        file_path = filedialog.askopenfilename(title="Select Graduate Study Plan File")
        if not file_path:
            return
        if file_path and check_file_type(file_path, [".xlsx", ".xls"]):
            self.study_plan_file_path = file_path
            button.config(text="File Uploaded", bootstyle=SUCCESS)
            button.filename_label.config(text=file_path.split('/')[-1])
            messagebox.showinfo("File Selected", "Graduate Study Plan File uploaded successfully!",  parent=self.root)
        else:
            messagebox.showerror("Invalid File", "Please select a valid Excel file.",  parent=self.root)
            self.study_plan_file_path = None
            button.config(text="Upload", bootstyle=PRIMARY)
            button.filename_label.config(text="")
        self.update_status()
        
    def upload_schedule_file(self, button):
        file_path = filedialog.askopenfilename(title="Select 4-Year Schedule File")
        if not file_path:
            return
        if file_path and check_file_type(file_path, [".xlsx", ".xls"]):
            self.schedule_file_path = file_path
            button.config(text="File Uploaded", bootstyle=SUCCESS)
            button.filename_label.config(text=file_path.split('/')[-1])
            messagebox.showinfo("File Selected", "4-Year Schedule File uploaded successfully!",  parent=self.root)
        else:
            messagebox.showerror("Invalid File", "Please select a valid Excel file.",  parent=self.root)
            self.schedule_file_path = None
            button.config(text="Upload", bootstyle=PRIMARY)
            button.filename_label.config(text="")
        self.update_status()
        
    def submit_files(self):
        if not (self.degree_file_path and self.study_plan_file_path and self.schedule_file_path and self.url_entry.get()):
            messagebox.showwarning("Missing Files", "Please upload all required files.",  parent=self.root)
        else:
            loading_window = Toplevel(self.root)
            loading_window.title("Processing")
            loading_window.geometry("300x100")
            loading_window.attributes('-topmost', 'true')
            ttk.Label(loading_window, text="Processing files, please wait...", font=("Helvetica", 12)).pack(pady=20)
            spinner_frame = ttk.Frame(loading_window)
            spinner_frame.pack()
            spinner = ttk.Progressbar(spinner_frame, mode='indeterminate', bootstyle=INFO)
            spinner.pack(pady=10)
            spinner.start()
            ttk.Label(loading_window, text="Processing files, please wait...", font=("Helvetica", 12)).pack(pady=20)
            threading.Thread(target=self.process_files, args=(loading_window,), daemon=True).start()
            
    def process_files(self, loading_window):
        #todo add logic of processing data
        degree_data = self.controller.process_degreeworks_file(self.degree_file_path)

        schedule_data = self.controller.process_schedule_file(self.schedule_file_path)

        url = self.url_entry.get()
        prereq_data = self.controller.process_prerequisites(url)

        loading_window.destroy()
        
      
        if isinstance(degree_data, dict): 

            for widget in self.root.winfo_children():
                widget.destroy()

            self.root.title("Processing Result")
            self.root.geometry("1000x600")

            result_text = ttk.Text(self.root, height=30, width=100)
            result_text.pack(pady=20)

            result_text.tag_configure("green_title", foreground="green", font=("Helvetica", 12, "bold"))

            #Display the parsed DegreeWorks result
            degree_file_name = os.path.basename(self.degree_file_path) 
            result_text.insert('end', f"Parsed result from your {degree_file_name}:\n", "green_title")

            for course, details in degree_data.items():
                result_text.insert(
                    'end', 
                    f"Course: {course}, Status: {details['status']}, Term: {details['term']}\n"
                )

            schedule_file_name = os.path.basename(self.schedule_file_path)
            result_text.insert('end', f"\n\nResult from your {schedule_file_name}:\n", "green_title")

            for course, terms in schedule_data.items():
                result_text.insert(
                    'end', 
                    f"Course: {course}, Available in: {', '.join(terms)}\n"
                )

            result_text.insert('end', f"\n\nPrerequisites from scraping:\n\n", "green_title")
            for course, prereqs in prereq_data.items():
                if prereqs:
                    prereq_text = " AND ".join([" OR ".join(group) for group in prereqs])
                    result_text.insert('end', f"Course: {course}, Prerequisites: {prereq_text}\n")
                else:
                    result_text.insert('end', f"Course: {course}, Prerequisites: None\n")

            result_text.insert('end', "\n\nParsed result from your Graduate_Plan.xlsx:\n\n")

            result_text.config(state='disabled')

            download_button = ttk.Button(self.root, text="Download Result in Excel File", command=self.download_result, bootstyle=SUCCESS)
            download_button.pack(pady=10)
        else:
            messagebox.showerror("Processing Error", f"An error occurred: {degree_data}", parent=self.root)  
    def download_result(self):
        messagebox.showinfo("Download", "Your result Excel file has been downloaded successfully!", parent=self.root)

    def update_status(self):
        status_text = """
            Degree Requirements File: {} {}
            Graduate Study Plan File: {} {}
            4-Year Schedule File: {} {}""".format(
            "Uploaded" if self.degree_file_path else " Not Uploaded",
            "\u2705" if self.degree_file_path else "\u274C",
            "Uploaded" if self.study_plan_file_path else " Not Uploaded",
            "\u2705" if self.study_plan_file_path else "\u274C",
            "Uploaded" if self.schedule_file_path else " Not Uploaded",
            "\u2705" if self.schedule_file_path else "\u274C"
            )
        self.status_box.config(state='normal')
        self.status_box.delete('1.0', 'end')
        self.status_box.insert('1.0', status_text)

        self.apply_text_color_to_status_box("\u2705", "green")
        self.apply_text_color_to_status_box("\u274C", "red")
        
        self.status_box.config(state='disabled')

    def apply_text_color_to_status_box(self, symbol, color):
        start_idx = '1.0'
        while True:
            start_idx = self.status_box.search(symbol, start_idx, stopindex='end')
            if not start_idx:
                break
            end_idx = f"{start_idx}+1c"
            self.status_box.tag_add(color, start_idx, end_idx)
            start_idx = end_idx
        self.status_box.tag_configure(color, foreground=color)
