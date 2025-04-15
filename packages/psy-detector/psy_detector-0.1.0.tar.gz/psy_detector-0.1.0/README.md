# Psy Detector

Writing a thesis, working on a manuscript, track your anxitety.
A Python application that detects and counts sighs in real-time using your microphone. The application continuously monitors audio input to identify sigh patterns based on their acoustic characteristics.

## Installation

### From PyPI (Recommended)

```bash
pip install psy-detector
```

### From Source

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application to start monitoring your microphone:

```bash
psy-detector
```

### Options

- `--min-duration`: Minimum duration of a sigh in seconds (default: 0.5)
- `--max-duration`: Maximum duration of a sigh in seconds (default: 2.0)
- `--threshold`: Energy threshold for sigh detection (default: 0.3)

Example with custom parameters:
```bash
psy-detector --min-duration 0.3 --max-duration 1.5 --threshold 0.25
```

## How it Works

The application:
1. Continuously captures audio from your microphone
2. Processes the audio in real-time using a sliding window approach
3. Computes RMS energy and identifies potential sigh patterns
4. Filters and validates sighs based on duration and energy characteristics
5. Displays the total count and timestamp of detected sighs

## Features

- Real-time monitoring of microphone input
- Configurable detection parameters
- Live display of sigh count and timestamps
- Graceful shutdown with Ctrl+C

## Notes

- Make sure your microphone is properly connected and configured
- The application uses a 2-second sliding window for processing
- Press Ctrl+C to stop the monitoring

## Supported Audio Formats

The application supports common audio formats including WAV, MP3, and FLAC. 