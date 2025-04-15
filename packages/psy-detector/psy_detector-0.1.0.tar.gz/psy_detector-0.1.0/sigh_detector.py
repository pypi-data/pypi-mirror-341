import os
import click
import librosa
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import soundfile as sf
from scipy.signal import find_peaks
import pyaudio
import time
from datetime import datetime
import threading
import queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better performance

console = Console()

class SighMonitor:
    def __init__(self, min_duration=0.3, max_duration=2.0, threshold=0.5):
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.threshold = threshold
        self.sigh_count = 0
        self.sigh_timestamps = []
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.WINDOW_SIZE = int(self.RATE * 2)  # 2 seconds window
        
        # Initialize plot
        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
        self.fig.suptitle('Real-time Audio Monitoring')
        self.ax1.set_title('Audio Waveform')
        self.ax2.set_title('RMS Energy')
        self.ax1.set_ylim(-1, 1)
        self.ax2.set_ylim(0, 1)
        self.line1, = self.ax1.plot([], [], 'b-')
        self.line2, = self.ax2.plot([], [], 'r-')
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax2.axhline(y=threshold, color='g', linestyle='--', label='Threshold')
        self.ax2.legend()
        plt.tight_layout()
        
        # Initialize data arrays
        self.x = np.linspace(0, 2, self.WINDOW_SIZE)
        self.audio_data = np.zeros(self.WINDOW_SIZE)
        self.rms_data = np.zeros(self.WINDOW_SIZE)

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for audio stream"""
        if self.is_running:
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            self.audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    def update_plot(self):
        """Update the real-time plot"""
        self.line1.set_data(self.x, self.audio_data)
        self.line2.set_data(self.x, self.rms_data)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def process_audio(self, audio_data):
        """Process audio data to detect sighs"""
        # Update audio data for plotting
        self.audio_data = audio_data[-self.WINDOW_SIZE:]
        
        # Compute RMS energy
        frame_length = int(self.RATE * 0.025)  # 25ms frames
        hop_length = int(self.RATE * 0.010)    # 10ms hop
        rms = librosa.feature.rms(y=audio_data, frame_length=frame_length, hop_length=hop_length)[0]
        
        if len(rms) > 0:
            # Normalize RMS
            rms = rms / np.max(rms)
            # Update RMS data for plotting
            self.rms_data = np.interp(self.x, np.linspace(0, 2, len(rms)), rms)
            
            # Find peaks in RMS energy
            peaks, _ = find_peaks(rms, height=self.threshold, 
                                distance=int(self.RATE/hop_length * self.min_duration))
            
            # Filter peaks based on duration
            for peak in peaks:
                start_time = peak * hop_length / self.RATE
                end_idx = np.argmax(rms[peak:] < self.threshold/2)
                if end_idx > 0:
                    duration = end_idx * hop_length / self.RATE
                    if self.min_duration <= duration <= self.max_duration:
                        self.sigh_count += 1
                        self.sigh_timestamps.append((datetime.now(), start_time))
                        return True
        return False

    def start_monitoring(self):
        """Start monitoring microphone input"""
        self.is_running = True
        self.sigh_count = 0
        self.sigh_timestamps = []
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                       channels=self.CHANNELS,
                       rate=self.RATE,
                       input=True,
                       frames_per_buffer=self.CHUNK,
                       stream_callback=self.audio_callback)
        
        try:
            audio_buffer = np.array([])
            while self.is_running:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get()
                    audio_buffer = np.append(audio_buffer, audio_data)
                    
                    if len(audio_buffer) >= self.WINDOW_SIZE:
                        if self.process_audio(audio_buffer):
                            self.display_results()
                        audio_buffer = audio_buffer[-self.WINDOW_SIZE:]
                        self.update_plot()
                
                time.sleep(0.01)  # Reduced sleep time for smoother visualization
                
        except KeyboardInterrupt:
            self.is_running = False
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            plt.close()

    def display_results(self):
        """Display current results"""
        console.clear()
        table = Table(title="Sigh Detection Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Sighs Detected", str(self.sigh_count))
        table.add_row("Last Sigh", self.sigh_timestamps[-1][0].strftime("%H:%M:%S"))
        
        console.print(table)

@click.command()
@click.option('--min-duration', default=0.5, help='Minimum duration of a sigh in seconds')
@click.option('--max-duration', default=2.0, help='Maximum duration of a sigh in seconds')
@click.option('--threshold', default=0.3, help='Energy threshold for sigh detection')
def main(min_duration, max_duration, threshold):
    """Monitor microphone input for sighs in real-time."""
    
    console.print("[bold cyan]Starting sigh detection...[/bold cyan]")
    console.print("[yellow]Press Ctrl+C to stop monitoring[/yellow]")
    
    monitor = SighMonitor(
        min_duration=min_duration,
        max_duration=max_duration,
        threshold=threshold
    )
    
    monitor.start_monitoring()

if __name__ == '__main__':
    main() 