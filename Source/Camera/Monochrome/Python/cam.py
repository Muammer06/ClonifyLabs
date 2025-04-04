import cv2
import tkinter as tk
from tkinter import Scale, HORIZONTAL, OptionMenu, StringVar, Frame, Label, Radiobutton
from threading import Thread
import time

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Control")
        
        # Camera variables
        self.camera_index = 4
        self.cap = None
        self.running = True
        
        # Camera formats from v4l2-ctl output
        self.formats = {
            "Y12 (12-bit Greyscale)": "Y12 ",
            "GREY (8-bit Greyscale)": "GREY"
        }
        self.current_format = "GREY"
        
        # Resolution options based on format
        self.all_resolutions = {
            "Y12 ": {
                "2064x1552": (2064, 1552, [51.0, 30.0, 25.0]),
                "1920x1080": (1920, 1080, [72.0, 60.0, 50.0]),
                "640x480": (640, 480, [145.0, 120.0, 100.0])
            },
            "GREY": {
                "2064x1552": (2064, 1552, [72.0, 60.0, 50.0]),
                "1920x1080": (1920, 1080, [100.0, 90.0]),
                "640x480": (640, 480, [198.0, 180.0, 175.0]),
                "1024x768": (1024, 768, [50.0])
            }
        }
        
        # Current settings
        self.current_resolution = "640x480"
        self.current_fps = 100.0
        
        # Create UI
        self.create_ui()
        
        # Initialize camera
        self.init_camera()
        
        # Start video thread
        self.video_thread = Thread(target=self.show_video)
        self.video_thread.daemon = True
        self.video_thread.start()
        
        # Clean up resources when closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        # Create frames for better organization
        format_frame = Frame(self.root)
        format_frame.pack(pady=5, fill=tk.X)
        
        resolution_frame = Frame(self.root)
        resolution_frame.pack(pady=5, fill=tk.X)
        
        self.fps_frame = Frame(self.root)
        self.fps_frame.pack(pady=5, fill=tk.X)
        
        controls_frame = Frame(self.root)
        controls_frame.pack(pady=5, fill=tk.X)
        
        # Format selection
        Label(format_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.format_var = StringVar(self.root)
        self.format_var.set("GREY (8-bit Greyscale)")
        self.format_menu = OptionMenu(format_frame, self.format_var, *self.formats.keys(), command=self.set_format)
        self.format_menu.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Resolution selection
        Label(resolution_frame, text="Resolution:").pack(side=tk.LEFT, padx=5)
        self.resolution_var = StringVar(self.root)
        self.resolution_var.set(self.current_resolution)
        self.resolution_menu = OptionMenu(resolution_frame, self.resolution_var, *self.all_resolutions[self.current_format].keys(), command=self.set_resolution)
        self.resolution_menu.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # FPS selection
        Label(self.fps_frame, text="FPS:").pack(side=tk.LEFT, padx=5)
        self.fps_var = StringVar(self.root)
        self.fps_var.set(str(self.current_fps))
        self.update_fps_menu()
        
        # Gain control (0-24)
        self.gain_scale = Scale(controls_frame, from_=0, to=24, orient=HORIZONTAL, 
                               label='Gain (0-24)', command=self.set_gain)
        self.gain_scale.set(0)
        self.gain_scale.pack(fill=tk.X, padx=10, pady=5)

        # Auto exposure control
        self.auto_exposure_frame = Frame(controls_frame)
        self.auto_exposure_frame.pack(fill=tk.X, padx=10, pady=5)
        
        Label(self.auto_exposure_frame, text="Auto Exposure:").pack(side=tk.LEFT)
        
        self.auto_exposure_var = tk.IntVar(value=0)
        
        # Auto exposure options based on v4l2-ctl output (min=0 max=3)
        self.auto_exposure_options = [
            ("Auto Mode", 0),
            ("Manual Mode", 1),
            ("Shutter Priority Mode", 2),
            ("Aperture Priority Mode", 3)
        ]
        
        for text, value in self.auto_exposure_options:
            Radiobutton(self.auto_exposure_frame, text=text, variable=self.auto_exposure_var, 
                        value=value, command=self.set_auto_exposure).pack(side=tk.LEFT, padx=5)

        # Exposure time control (1-10000)
        self.exposure_scale = Scale(controls_frame, from_=1, to=10000, orient=HORIZONTAL, 
                                   label='Exposure Time (1-10000)', command=self.set_exposure_time)
        self.exposure_scale.set(156)
        self.exposure_scale.pack(fill=tk.X, padx=10, pady=5)

    def update_fps_menu(self):
        # Get available FPS options for current resolution and format
        fps_options = self.all_resolutions[self.current_format][self.current_resolution][2]
        
        # Update FPS dropdown
        if hasattr(self, 'fps_menu'):
            self.fps_menu.destroy()
        
        self.fps_var.set(str(fps_options[0]))  # Set to first available FPS
        self.current_fps = fps_options[0]
        
        self.fps_menu = OptionMenu(self.fps_frame, self.fps_var, 
                                  *[str(fps) for fps in fps_options], 
                                  command=self.set_fps)
        self.fps_menu.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def set_format(self, value):
        format_key = self.formats[value]
        if format_key != self.current_format:
            self.current_format = format_key
            
            # Update resolution options for this format
            self.resolution_menu.destroy()
            self.resolution_var.set(list(self.all_resolutions[self.current_format].keys())[0])
            self.current_resolution = self.resolution_var.get()
            
            resolution_frame = self.resolution_menu.master
            self.resolution_menu = OptionMenu(resolution_frame, self.resolution_var, 
                                             *self.all_resolutions[self.current_format].keys(), 
                                             command=self.set_resolution)
            self.resolution_menu.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Update FPS options
            self.update_fps_menu()
            
            # Reinitialize camera
            self.init_camera()

    def set_resolution(self, value):
        if value != self.current_resolution:
            self.current_resolution = value
            self.update_fps_menu()
            self.init_camera()

    def set_fps(self, value):
        self.current_fps = float(value)
        self.init_camera()

    def init_camera(self):
        # Close camera if already open
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            
        # Open camera
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Could not open camera {self.camera_index}!")
            return False
            
        # Set camera format
        if self.current_format == "GREY":
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('G', 'R', 'E', 'Y'))
        elif self.current_format == "Y12 ":
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', '1', '2', ' '))
        
        # Set resolution
        width, height, _ = self.all_resolutions[self.current_format][self.current_resolution]
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Set FPS
        self.cap.set(cv2.CAP_PROP_FPS, self.current_fps)
        
        # Apply current settings
        self.set_gain(self.gain_scale.get())
        self.set_auto_exposure()
        self.set_exposure_time(self.exposure_scale.get())
        
        return True

    def set_gain(self, value):
        if self.cap and self.cap.isOpened():
            gain_value = int(value)
            self.cap.set(cv2.CAP_PROP_GAIN, gain_value)

    def set_auto_exposure(self):
        if self.cap and self.cap.isOpened():
            auto_exposure = self.auto_exposure_var.get()
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
            
            # Enable/disable exposure time control based on auto exposure setting
            if auto_exposure == 0:  # Auto Mode
                self.exposure_scale.config(state=tk.DISABLED)
            else:
                self.exposure_scale.config(state=tk.NORMAL)

    def set_exposure_time(self, value):
        if self.cap and self.cap.isOpened():
            exposure_time = int(value)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure_time)

    def show_video(self):
        while self.running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # Display current settings on frame
                    settings_text = f"Format: {self.current_format.strip()} | Resolution: {self.current_resolution} | FPS: {self.current_fps}"
                    cv2.putText(frame, settings_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Show camera properties
                    gain = self.gain_scale.get()
                    exposure_mode = self.auto_exposure_options[self.auto_exposure_var.get()][0]
                    exposure_time = self.exposure_scale.get()
                    
                    props_text = f"Gain: {gain} | Exposure: {exposure_mode} | Exp. Time: {exposure_time}"
                    cv2.putText(frame, props_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    cv2.imshow('Camera', frame)
                else:
                    # Try to reconnect if connection lost
                    print("Camera connection lost, trying to reconnect...")
                    self.init_camera()
                    time.sleep(1)
            else:
                # Try to open camera if not open
                print("Camera not open, trying to open...")
                self.init_camera()
                time.sleep(1)
                
            if cv2.waitKey(1) == ord('q'):
                self.running = False
                break

    def on_closing(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
