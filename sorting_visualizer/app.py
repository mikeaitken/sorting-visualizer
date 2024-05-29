import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from .algorithms import (
    selection_sort, bubble_sort, insertion_sort, merge_sort, quick_sort, heap_sort,
    counting_sort, radix_sort, bucket_sort, shell_sort, tim_sort,
    comb_sort, pigeonhole_sort, cycle_sort, cocktail_sort, strand_sort,
    pancake_sort, bogo_sort, gnome_sort, stooge_sort, tag_sort,
    odd_even_sort, merge_sort_3way
)
from .visualize import visualize_sorting

class SortingVisualizerApp:
    """Application for visualizing sorting algorithms."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        
        self.algorithms = {
            "Selection Sort": selection_sort,
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": lambda arr: quick_sort(arr, 0, len(arr) - 1),
            "Heap Sort": heap_sort,
            "Counting Sort": counting_sort,
            "Radix Sort": radix_sort,
            "Bucket Sort": bucket_sort,
            "Shell Sort": shell_sort,
            "Tim Sort": tim_sort,
            "Comb Sort": comb_sort,
            "Pigeonhole Sort": pigeonhole_sort,
            "Cycle Sort": cycle_sort,
            "Cocktail Sort": cocktail_sort,
            "Strand Sort": strand_sort,
            "Pancake Sort": pancake_sort,
            "Bogo Sort": bogo_sort,
            "Gnome Sort": gnome_sort,
            "Stooge Sort": stooge_sort,
            "Tag Sort": tag_sort,
            "Odd-Even Sort": odd_even_sort,
            "3-way Merge Sort": merge_sort_3way,
        }
        
        self.arr = [random.randint(1, 100) for _ in range(50)]
        
        self.selected_algorithm = tk.StringVar(value="Selection Sort")
        self.speed = tk.IntVar(value=50)
        
        self.anim = None
        self.canvas = None
        self.after_ids = []
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Setup the user interface."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(control_frame, text="Algorithm:").pack(side=tk.LEFT)
        self.algo_menu = ttk.OptionMenu(control_frame, self.selected_algorithm, self.selected_algorithm.get(), *self.algorithms.keys())
        self.algo_menu.pack(side=tk.LEFT)
        
        ttk.Label(control_frame, text="Speed (ms):").pack(side=tk.LEFT)
        speed_scale = ttk.Scale(control_frame, from_=1, to_=100, variable=self.speed, orient=tk.HORIZONTAL)
        speed_scale.pack(side=tk.LEFT)
        
        generate_button = ttk.Button(control_frame, text="Generate New Data", command=self.generate_data)
        generate_button.pack(side=tk.LEFT)
        
        start_button = ttk.Button(control_frame, text="Start/Resume", command=self.start_or_resume_sorting)
        start_button.pack(side=tk.LEFT)
        
        stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_sorting)
        stop_button.pack(side=tk.LEFT)
        
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.root.geometry("800x600")
        
    def generate_data(self):
        """Generate new random data for sorting."""
        self.arr = [random.randint(1, 100) for _ in range(50)]
        self.stop_sorting()
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            self.canvas = None
        self.anim = None
    
    def start_or_resume_sorting(self):
        """Start or resume the sorting visualization."""
        if self.anim and self.anim.event_source:
            self.anim.event_source.start()
        else:
            selected_algo = self.algorithms[self.selected_algorithm.get()]
            speed = self.speed.get()
            
            if self.canvas:
                self.canvas.get_tk_widget().pack_forget()
            
            fig, anim = visualize_sorting(self.arr, selected_algo, self.selected_algorithm.get() + " Visualization", speed)
            self.anim = anim
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def stop_sorting(self):
        """Stop the sorting visualization."""
        if self.anim and self.anim.event_source:
            self.anim.event_source.stop()

    def on_closing(self):
        """Handle the closing of the application."""
        self.stop_sorting()
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            self.canvas = None
        self.root.quit()
        self.root.destroy()

    def after(self, ms, func):
        """Schedule a function to be called after a given time."""
        after_id = self.root.after(ms, func)
        self.after_ids.append(after_id)
        return after_id
