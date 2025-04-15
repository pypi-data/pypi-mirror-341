import customtkinter as ctk
from tkinter import filedialog
import warnings
import traceback
from itertools import chain

from numbers_and_brightness.analysis import numbers_and_brightness_analysis, numbers_and_brightness_batch
from numbers_and_brightness import __version__
from numbers_and_brightness.defaults import (
    DEFAULT_BACKGROUND,
    DEFAULT_SEGMENT,
    DEFAULT_DIAMETER,
    DEFAULT_FLOW_THRESHOLD,
    DEFAULT_CELLPROB_THRESHOLD,
    DEFAULT_ANALYSIS,
    DEFAULT_ERODE
)

def wrap(name: str, max_num: int):
    if len(name)>max_num:
        return f"...{name[-max_num:]}"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Numbers and brightness Analysis - Version {__version__}")
        self.resizable(False, False)

        self.file = ""
        self.folder = ""
        self.segment = ctk.BooleanVar(value=DEFAULT_SEGMENT)
        self.analysis = ctk.BooleanVar(value=DEFAULT_ANALYSIS)

        self.file_select_button = ctk.CTkButton(master=self, text="Select file", command=self.get_file)
        self.file_select_button.grid(row=0, column=0, pady=(10, 5), padx=10, sticky='nesw', columnspan=2)

        self.folder_select_button = ctk.CTkButton(master=self, text="Select folder", command=self.get_folder)
        self.folder_select_button.grid(row=1, column=0, pady=(5, 5), padx=10, sticky='nesw', columnspan=2)

        self.background_label = ctk.CTkLabel(master=self, text="Background:")
        self.background_label.grid(row=2, column=0, pady=(5,5), padx=10, sticky='w')
        self.background_input = ctk.CTkEntry(master=self)
        self.background_input.grid(row=2, column=1, pady=(5,5), padx=10, sticky='nesw')
        self.background_input.insert(0, DEFAULT_BACKGROUND)

        self.segment_label = ctk.CTkLabel(master=self, text="Segment:")
        self.segment_label.grid(row=3, column=0, pady=(5,5), padx=10, sticky='w')
        self.segment_input = ctk.CTkCheckBox(master=self, variable=self.segment, text="")
        self.segment_input.grid(row=3, column=1, pady=(5,5), padx=10, sticky='nesw')
        
        self.cellpose_frame = ctk.CTkFrame(master=self)
        self.cellpose_frame.grid(row=4, column=0, pady=(5,5), padx=10, sticky='nesw', columnspan=2)

        self.cellpose_label = ctk.CTkLabel(master=self.cellpose_frame, text="Cellpose settings:")
        self.cellpose_label.grid(row=3, column=0, pady=(10,5), padx=10, sticky='nesw')

        self.diameter_label = ctk.CTkLabel(master=self.cellpose_frame, text="Diameter:")
        self.diameter_label.grid(row=4, column=0, pady=(5,5), padx=10, sticky='w')
        self.diameter_input = ctk.CTkEntry(master=self.cellpose_frame)
        self.diameter_input.grid(row=4, column=1, pady=(5,5), padx=10, sticky='nesw')
        self.diameter_input.insert(0, DEFAULT_DIAMETER)

        self.flow_label = ctk.CTkLabel(master=self.cellpose_frame, text="Flow threshold:")
        self.flow_label.grid(row=5, column=0, pady=(5,5), padx=10, sticky='w')
        self.flow_input = ctk.CTkEntry(master=self.cellpose_frame)
        self.flow_input.grid(row=5, column=1, pady=(5,5), padx=10, sticky='nesw')
        self.flow_input.insert(0, DEFAULT_FLOW_THRESHOLD)

        self.cellprob_label = ctk.CTkLabel(master=self.cellpose_frame, text="Cellprob threshold:")
        self.cellprob_label.grid(row=6, column=0, pady=(5,10), padx=10, sticky='w')
        self.cellprob_input = ctk.CTkEntry(master=self.cellpose_frame)
        self.cellprob_input.grid(row=6, column=1, pady=(5,10), padx=10, sticky='nesw')
        self.cellprob_input.insert(0, DEFAULT_CELLPROB_THRESHOLD)

        self.analysis_label = ctk.CTkLabel(master=self, text="Analysis:")
        self.analysis_label.grid(row=7, column=0, pady=(5,5), padx=10, sticky='w')
        self.analysis_input = ctk.CTkCheckBox(master=self, variable=self.analysis, text="")
        self.analysis_input.grid(row=7, column=1, pady=(5,5), padx=10, sticky='nesw')

        self.erode_label = ctk.CTkLabel(master=self, text="Erode:")
        self.erode_label.grid(row=8, column=0, pady=(5,5), padx=10, sticky='w')
        self.erode_input = ctk.CTkEntry(master=self)
        self.erode_input.grid(row=8, column=1, pady=(5,5), padx=10, sticky='nesw')
        self.erode_input.insert(0, DEFAULT_ERODE)

        self.process_file_button = ctk.CTkButton(master=self, text="Process file", command=self.process_file)
        self.process_file_button.grid(row=9, column=0, pady=(5, 5), padx=10, sticky='nesw', columnspan=2)

        self.process_folder_button = ctk.CTkButton(master=self, text="Process folder", command=self.process_folder)
        self.process_folder_button.grid(row=10, column=0, pady=(5, 10), padx=10, sticky='nesw', columnspan=2)

        self.select_buttons = [self.file_select_button, self.folder_select_button]
        self.process_buttons = [self.process_file_button, self.process_folder_button]

    def get_file(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.file = filename
            self.file_select_button.configure(text=wrap(filename, 50))

    def get_folder(self):
        foldername = filedialog.askdirectory()
        if foldername != "":
            self.folder = foldername
            self.folder_select_button.configure(text=wrap(foldername, 50))

    def process_file(self):
        if self.file == "":
            print("Select a file")
            return
        try:
            # Disable all buttons
            for button in chain(self.select_buttons, self.process_buttons):
                button.configure(state="disabled")
            numbers_and_brightness_analysis(
                file=self.file,
                background=float(self.background_input.get()),
                segment=self.segment.get(),
                diameter=int(self.diameter_input.get()),
                flow_threshold=float(self.flow_input.get()),
                cellprob_threshold=float(self.cellprob_input.get()),
                analysis=self.analysis.get(),
                erode=int(self.erode_input.get())
            )
            print(f"Processed: {self.file}")
        except:
            traceback.print_exc()

        for button in chain(self.select_buttons, self.process_buttons):
            button.configure(state="normal")


    def process_folder(self):
        if self.folder == "":
            print("Select a folder")
            return
        try:
            # Disable all buttons
            for button in chain(self.select_buttons, self.process_buttons):
                button.configure(state="disabled")
            numbers_and_brightness_batch(
                folder=self.folder,
                background=float(self.background_input.get()),
                segment=self.segment.get(),
                diameter=int(self.diameter_input.get()),
                flow_threshold=float(self.flow_input.get()),
                cellprob_threshold=float(self.cellprob_input.get()),
                analysis=self.analysis.get(),
                erode=int(self.erode_input.get())
            )
        except:
            traceback.print_exc()
    
        for button in chain(self.select_buttons, self.process_buttons):
            button.configure(state="normal")
def nb_gui():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        app = App()
        app.mainloop()

if __name__ == "__main__":
    nb_gui()