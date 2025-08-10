import tkinter as tk
import time
from tkinter import ttk
from itertools import cycle

class TrafficLightSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pre-Timed Traffic Light Control System")
        
        # Fixed time intervals for each light (in seconds)
        self.timings = {
            'NS_red_EW_green': 20,    # North-South red, East-West green
            'NS_red_EW_yellow': 5,    # North-South red, East-West yellow
            'NS_green_EW_red': 20,    # North-South green, East-West red
            'NS_yellow_EW_red': 5     # North-South yellow, East-West red
        }
        
        # Current phase and remaining time
        self.current_phase = None
        self.remaining_time = 0
        self.running = False
        
        # Create the dashboard
        self.create_dashboard()
        
        # Create the traffic light display
        self.create_traffic_lights()
        
        # Create control buttons
        self.create_controls()
        
        # Phase sequence
        self.phases = cycle([
            'NS_red_EW_green',
            'NS_red_EW_yellow',
            'NS_green_EW_red',
            'NS_yellow_EW_red'
        ])
        
    def create_dashboard(self):
        """Create the information dashboard"""
        self.dashboard_frame = ttk.LabelFrame(self.root, text="Dashboard", padding=10)
        self.dashboard_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Current phase display
        ttk.Label(self.dashboard_frame, text="Current Phase:").grid(row=0, column=0, sticky="w")
        self.phase_label = ttk.Label(self.dashboard_frame, text="System Off", font=('Arial', 12, 'bold'))
        self.phase_label.grid(row=0, column=1, sticky="w")
        
        # Time remaining display
        ttk.Label(self.dashboard_frame, text="Time Remaining:").grid(row=1, column=0, sticky="w")
        self.time_label = ttk.Label(self.dashboard_frame, text="0 s", font=('Arial', 12))
        self.time_label.grid(row=1, column=1, sticky="w")
        
        # Timing configuration display
        ttk.Label(self.dashboard_frame, text="Timing Configuration:", font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")
        
        for i, (phase, duration) in enumerate(self.timings.items()):
            phase_name = phase.replace('_', ' ').title()
            ttk.Label(self.dashboard_frame, text=f"{phase_name}:").grid(row=3+i, column=0, sticky="w")
            ttk.Label(self.dashboard_frame, text=f"{duration} s").grid(row=3+i, column=1, sticky="w")
    
    def create_traffic_lights(self):
        """Create the visual representation of traffic lights"""
        self.lights_frame = ttk.LabelFrame(self.root, text="Traffic Lights", padding=10)
        self.lights_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # North-South lights
        ttk.Label(self.lights_frame, text="North-South", font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5)
        
        self.ns_red = self.create_light_circle(self.lights_frame, 1, 0, 'gray')
        self.ns_yellow = self.create_light_circle(self.lights_frame, 2, 0, 'gray')
        self.ns_green = self.create_light_circle(self.lights_frame, 3, 0, 'gray')
        
        # East-West lights
        ttk.Label(self.lights_frame, text="East-West", font=('Arial', 10, 'bold')).grid(row=0, column=1, pady=5)
        
        self.ew_red = self.create_light_circle(self.lights_frame, 1, 1, 'gray')
        self.ew_yellow = self.create_light_circle(self.lights_frame, 2, 1, 'gray')
        self.ew_green = self.create_light_circle(self.lights_frame, 3, 1, 'gray')
    
    def create_light_circle(self, parent, row, column, color):
        """Helper function to create a light circle"""
        canvas = tk.Canvas(parent, width=50, height=50, bg='white', highlightthickness=0)
        canvas.grid(row=row, column=column, padx=10, pady=5)
        circle = canvas.create_oval(5, 5, 45, 45, fill=color, outline='black')
        return canvas
    
    def create_controls(self):
        """Create control buttons"""
        self.control_frame = ttk.Frame(self.root, padding=10)
        self.control_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_system)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_system)
        self.stop_button.pack(side="left", padx=5)
        
        self.reset_button = ttk.Button(self.control_frame, text="Reset", command=self.reset_system)
        self.reset_button.pack(side="left", padx=5)
    
    def start_system(self):
        """Start the traffic light system"""
        if not self.running:
            self.running = True
            self.next_phase()
    
    def stop_system(self):
        """Stop the traffic light system"""
        self.running = False
        self.phase_label.config(text="System Off")
        self.time_label.config(text="0 s")
        self.reset_lights()
    
    def reset_system(self):
        """Reset the traffic light system"""
        self.stop_system()
        self.phases = cycle([
            'NS_red_EW_green',
            'NS_red_EW_yellow',
            'NS_green_EW_red',
            'NS_yellow_EW_red'
        ])
    
    def next_phase(self):
        """Move to the next phase in the sequence"""
        if not self.running:
            return
            
        self.current_phase = next(self.phases)
        self.remaining_time = self.timings[self.current_phase]
        
        # Update the dashboard
        phase_name = self.current_phase.replace('_', ' ').title()
        self.phase_label.config(text=phase_name)
        self.time_label.config(text=f"{self.remaining_time} s")
        
        # Update the lights
        self.update_lights()
        
        # Start the countdown
        self.countdown()
    
    def update_lights(self):
        """Update the traffic light display based on current phase"""
        # Reset all lights to gray
        self.reset_lights()
        
        # Set the active lights based on current phase
        if self.current_phase == 'NS_red_EW_green':
            self.ns_red.itemconfig(1, fill='red')
            self.ew_green.itemconfig(1, fill='green')
        elif self.current_phase == 'NS_red_EW_yellow':
            self.ns_red.itemconfig(1, fill='red')
            self.ew_yellow.itemconfig(1, fill='yellow')
        elif self.current_phase == 'NS_green_EW_red':
            self.ns_green.itemconfig(1, fill='green')
            self.ew_red.itemconfig(1, fill='red')
        elif self.current_phase == 'NS_yellow_EW_red':
            self.ns_yellow.itemconfig(1, fill='yellow')
            self.ew_red.itemconfig(1, fill='red')
    
    def reset_lights(self):
        """Reset all lights to inactive (gray)"""
        for light in [self.ns_red, self.ns_yellow, self.ns_green, 
                     self.ew_red, self.ew_yellow, self.ew_green]:
            light.itemconfig(1, fill='gray')
    
    def countdown(self):
        """Handle the countdown for the current phase"""
        if not self.running:
            return
            
        self.remaining_time -= 1
        self.time_label.config(text=f"{self.remaining_time} s")
        
        if self.remaining_time <= 0:
            self.next_phase()
        else:
            self.root.after(1000, self.countdown)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLightSystem(root)
    root.mainloop()