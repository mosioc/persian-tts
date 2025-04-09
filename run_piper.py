import subprocess
import os
import datetime

# Path to the text file
text_file_path = "text.txt"

# Get base name of the text file without extension for dynamic naming
base_name = os.path.splitext(os.path.basename(text_file_path))[0]
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"{base_name}_{timestamp}.wav"

# Paths for Piper and the model
piper_path = "./piper.exe"
model_path = "./models/fa_IR-gyro-medium.onnx"
output_dir = "./outputs"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Output file for the audio with dynamic name
output_file = os.path.join(output_dir, output_filename)

# Check file encoding and process the file
try:
    with open(text_file_path, "r", encoding="utf-8") as file:
        # Read the entire file
        text_content = file.read()
        
        # Main command for Piper
        command = [piper_path, "--model", model_path, "--output_file", output_file]

        try:
            # Send the entire text to Piper
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            stdout, stderr = process.communicate(input=text_content)

            # Check the output
            if process.returncode == 0:
                print(f"Successfully processed text file: {text_file_path}")
                print(f"Output saved to: {output_file}")
            else:
                print(f"Error processing text file: {stderr}")
        except Exception as e:
            print(f"Exception while processing text file: {e}")

except FileNotFoundError:
    print(f"File not found: {text_file_path}")
    exit(1)
except UnicodeDecodeError:
    print("File is not encoded in UTF-8!")
    exit(1)