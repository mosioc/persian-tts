# Piper TTS - Script for Persian/English Text-to-Speech Converter

This project provides a Python-based interface for the Piper text-to-speech engine, allowing you to convert text files into high-quality speech audio files. It supports both regular text files and large text files that need to be processed line by line.

## Features

- Convert text files to WAV audio files
- Support for UTF-8 encoded text files
- Handles both small and large text files
- Automatic output file naming with timestamps
- Combines multiple audio segments for large files
- Persian (Farsi) language support with the fa_IR-gyro-medium model

## Prerequisites

- Python 3.x
- FFmpeg (for combining audio files)
- Piper TTS engine and its dependencies:
  - piper.exe
  - piper_phonemize.dll
  - espeak-ng.dll
  - onnxruntime.dll
  - onnxruntime_providers_shared.dll
  - espeak-ng-data directory
  - models directory with the TTS model
 
## Downloading Models

The model files are not included in this repository due to their large size (approximately 60MB each). To use the TTS system:

1. Create a `models` directory in the project root
2. Download the desired model(s) from the Piper TTS model repository:
   - Persian models: https://huggingface.co/rhasspy/piper-voices/tree/main/fa_IR
   - English models: https://huggingface.co/rhasspy/piper-voices/tree/main/en_US
3. Place the downloaded `.onnx` files in the `models` directory

## Project Structure

```
.
├── models/                  # TTS model files
├── outputs/                 # Generated audio files
├── espeak-ng-data/         # eSpeak-ng data files
├── run_piper.py            # Script for regular text files
├── run_piper_very_large_file.py  # Script for large text files
├── text.txt                # Input text file
└── [other dependencies]    # Various DLL files and configurations
```

## Usage

### For Regular Text Files

1. Place your text in `text.txt` (UTF-8 encoded)
2. Run the script:
   ```bash
   python run_piper.py
   ```
3. The output will be saved in the `outputs` directory with a timestamp

### For Large Text Files

1. Place your text in `text.txt` (UTF-8 encoded)
2. Run the script:
   ```bash
   python run_piper_very_large_file.py
   ```
3. The script will:
   - Process the text line by line
   - Generate individual WAV files for each line
   - Combine all audio files into a single output file
   - Clean up temporary files

## Configuration

The scripts use the following default settings:
- Input file: `text.txt`
- Model: `models/fa_IR-gyro-medium.onnx`
- Output directory: `outputs/`

You can modify these paths in the scripts if needed.

## Model Configuration and Language Support

### Available Models

The project supports multiple language models. You can find the following models in the `models` directory:

- Persian (Farsi):
  - `fa_IR-gyro-medium.onnx` (default)
  - `fa_IR-gyro-high.onnx`
  - `fa_IR-gyro-low.onnx`

- English:
  - `en_US-amy-medium.onnx`
  - `en_US-amy-high.onnx`
  - `en_US-amy-low.onnx`

### Changing the Model

To change the model, follow these steps:

1. Download the desired model from the Piper TTS model repository
2. Place the model file in the `models` directory
3. Modify the model path in your script:

For regular text files (`run_piper.py`):
```python
model_path = "models/en_US-amy-medium.onnx"  # Change to your desired model
```

For large text files (`run_piper_very_large_file.py`):
```python
model_path = "models/en_US-amy-medium.onnx"  # Change to your desired model
```

### Model Quality Levels

Each language model comes in three quality levels:
- `low`: Faster processing, lower quality
- `medium`: Balanced quality and speed (recommended)
- `high`: Best quality, slower processing

Choose the quality level based on your needs for audio quality and processing speed.

### Troubleshooting

#### Persian Text Encoding Issues

If you encounter empty output when generating Persian text, it might be due to PowerShell encoding settings. Run this command in your terminal before executing the scripts:

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

This command ensures proper UTF-8 encoding support for Persian characters in PowerShell.

## Notes

- Ensure all text files are UTF-8 encoded
- The Persian model (fa_IR-gyro-medium) is used by default
- Large files are processed line by line to manage memory usage
- FFmpeg is required for combining audio files in the large file processor

## Error Handling

The scripts include error handling for:
- File not found errors
- Encoding issues
- Processing errors
- FFmpeg combination errors

