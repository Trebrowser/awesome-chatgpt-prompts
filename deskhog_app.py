#!/usr/bin/env python3
"""
Deskhog App - A desktop application to disconnect from active Zoom calls
using a center button interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import psutil
import threading
import time
import sys
import os
from datetime import datetime

class DeskhogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deskhog - Zoom Disconnect Tool")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set app icon if available
        try:
            # Try to set a custom icon (you can add an icon file later)
            self.root.iconname("Deskhog")
        except:
            pass
        
        # Application state
        self.zoom_status = "Not Detected"
        self.monitoring = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start monitoring thread
        self.start_monitoring()
        
        # Setup window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🖥️ Deskhog", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Zoom Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Status indicator
        self.status_label = ttk.Label(status_frame, text="🔍 Scanning for Zoom...", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar for status
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.progress.start()
        
        # Center button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Main disconnect button (center button)
        self.disconnect_button = tk.Button(
            button_frame,
            text="📞\nDISCONNECT\nZOOM CALL",
            font=("Arial", 16, "bold"),
            bg="#FF4444",
            fg="white",
            activebackground="#CC3333",
            activeforeground="white",
            relief="raised",
            bd=3,
            width=15,
            height=4,
            command=self.disconnect_zoom_call
        )
        self.disconnect_button.pack(pady=10)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Last action label
        self.last_action_label = ttk.Label(info_frame, text="Ready to disconnect Zoom calls", font=("Arial", 10))
        self.last_action_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
    
    def find_zoom_processes(self):
        """Find running Zoom processes"""
        zoom_processes = []
        zoom_process_names = [
            'zoom', 'Zoom', 'zoom.exe', 'Zoom.exe',
            'ZoomLauncher', 'ZoomLauncher.exe'
        ]
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_name = proc.info['name'].lower() if proc.info['name'] else ''
                    if any(zoom_name.lower() in proc_name for zoom_name in zoom_process_names):
                        zoom_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"Error finding Zoom processes: {e}")
        
        return zoom_processes
    
    def disconnect_zoom_call(self):
        """Disconnect from active Zoom call"""
        try:
            zoom_processes = self.find_zoom_processes()
            
            if not zoom_processes:
                self.update_status("❌ No Zoom process found")
                self.update_last_action("No active Zoom session detected")
                messagebox.showwarning("No Zoom Detected", "No active Zoom session found to disconnect from.")
                return
            
            # Method 1: Try to send Alt+Q (Zoom's quit shortcut) if on Linux/Mac
            if sys.platform.startswith('linux') or sys.platform == 'darwin':
                try:
                    # Use xdotool on Linux to send quit command to Zoom
                    if sys.platform.startswith('linux'):
                        subprocess.run(['xdotool', 'search', '--name', 'zoom', 'key', 'alt+q'], 
                                     capture_output=True, check=True)
                    # Use AppleScript on macOS
                    elif sys.platform == 'darwin':
                        applescript = '''
                        tell application "zoom.us"
                            quit
                        end tell
                        '''
                        subprocess.run(['osascript', '-e', applescript], 
                                     capture_output=True, check=True)
                    
                    self.update_status("✅ Zoom disconnected via hotkey")
                    self.update_last_action(f"Disconnected Zoom using system hotkey at {datetime.now().strftime('%H:%M:%S')}")
                    messagebox.showinfo("Success", "Zoom call disconnected successfully!")
                    return
                
                except subprocess.CalledProcessError:
                    # Fall back to process termination
                    pass
                except FileNotFoundError:
                    # xdotool not installed, fall back to process termination
                    pass
            
            # Method 2: Terminate Zoom processes
            terminated_count = 0
            for proc in zoom_processes:
                try:
                    proc.terminate()
                    terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if terminated_count > 0:
                # Wait a moment for graceful termination
                time.sleep(2)
                
                # Force kill if still running
                for proc in self.find_zoom_processes():
                    try:
                        proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                self.update_status("✅ Zoom disconnected via process termination")
                self.update_last_action(f"Terminated {terminated_count} Zoom process(es) at {datetime.now().strftime('%H:%M:%S')}")
                messagebox.showinfo("Success", f"Zoom disconnected! Terminated {terminated_count} process(es).")
            else:
                self.update_status("❌ Failed to disconnect Zoom")
                self.update_last_action("Failed to terminate Zoom processes")
                messagebox.showerror("Error", "Failed to disconnect from Zoom. Please try manually.")
        
        except Exception as e:
            error_msg = f"Error disconnecting Zoom: {str(e)}"
            self.update_status("❌ Error occurred")
            self.update_last_action(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def monitor_zoom_status(self):
        """Monitor Zoom status in background thread"""
        while self.monitoring:
            try:
                zoom_processes = self.find_zoom_processes()
                
                if zoom_processes:
                    self.zoom_status = "Active"
                    self.root.after(0, lambda: self.update_status("🟢 Zoom Active - Ready to disconnect"))
                    self.root.after(0, lambda: self.disconnect_button.config(state='normal', bg='#FF4444'))
                else:
                    self.zoom_status = "Not Detected"
                    self.root.after(0, lambda: self.update_status("🔍 Scanning for Zoom..."))
                    self.root.after(0, lambda: self.disconnect_button.config(state='normal', bg='#888888'))
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(5)  # Wait longer on error
    
    def update_status(self, status_text):
        """Update status label"""
        self.status_label.config(text=status_text)
        
        if "Active" in status_text:
            self.progress.stop()
            self.progress.config(mode='determinate', value=100)
        elif "Scanning" in status_text:
            self.progress.config(mode='indeterminate')
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.config(mode='determinate', value=0)
    
    def update_last_action(self, action_text):
        """Update last action label"""
        self.last_action_label.config(text=action_text)
    
    def start_monitoring(self):
        """Start the background monitoring thread"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_zoom_status, daemon=True)
        self.monitor_thread.start()
    
    def on_closing(self):
        """Handle application closing"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread') and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
        self.root.destroy()

def main():
    """Main function to run the Deskhog app"""
    # Check for required dependencies
    missing_deps = []
    
    try:
        import psutil
    except ImportError:
        missing_deps.append('psutil')
    
    if missing_deps:
        print(f"Missing required dependencies: {', '.join(missing_deps)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_deps)}")
        sys.exit(1)
    
    # Create and run the application
    root = tk.Tk()
    app = DeskhogApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        app.on_closing()

if __name__ == "__main__":
    main()