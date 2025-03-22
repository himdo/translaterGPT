import sys
import wave
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import pyaudio

class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Initialize audio recording variables
        self.recording = False
        self.frames = []
        self.audio_format = pyaudio.paInt16  # 16-bit resolution
        self.channels = 1  # Mono
        self.rate = 44100  # Sampling rate
        self.chunk = 1024  # Data chunk size
        self.filename = "output.wav"
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
    
    def initUI(self):
        # Create a button and set its text
        self.button = QPushButton('Start Recording', self)
        self.button.clicked.connect(self.toggle_recording)
        
        # Create a label to display status
        self.status_label = QLabel('Press Start Recording to begin.', self)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.status_label)
        
        # Set the window properties
        self.setLayout(layout)
        self.setWindowTitle('Audio Recorder')
        self.setGeometry(100, 100, 300, 200)
    
    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        self.status_label.setText('Recording...')
        self.button.setText('Stop Recording')
        
        # Open a stream for recording
        self.stream = self.audio.open(format=self.audio_format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        
        self.recording = True
        self.frames = []
        
        # Start the recording in a separate thread to keep the GUI responsive
        import threading
        threading.Thread(target=self.record_audio).start()
    
    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
    
    def stop_recording(self):
        self.status_label.setText('Recording stopped.')
        self.button.setText('Start Recording')
        
        # Stop and close the stream
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        
        # Save the recorded data as a WAV file
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        self.status_label.setText(f'Recording saved to {self.filename}.')
    
    def closeEvent(self, event):
        # Ensure the audio stream is closed properly on exit
        if hasattr(self, 'stream') and self.stream.is_active():
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        event.accept()

def main():
    app = QApplication(sys.argv)
    ex = AudioRecorder()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()