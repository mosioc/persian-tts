import subprocess
import os

# Path to the text file
text_file_path = "text.txt"

# Paths for Piper and the model
piper_path = "./piper.exe"
model_path = "./models/fa_IR-gyro-medium.onnx"
output_dir = "./outputs"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List to store individual audio files
audio_files = []

# Check file encoding and process line by line
try:
    with open(text_file_path, "r", encoding="utf-8") as file:
        # Read the file line by line
        for line_number, line in enumerate(file, start=1):
            line = line.strip()  # Remove extra whitespace
            if not line:  # Skip empty lines
                continue

            # Output file for this line
            output_file = os.path.join(output_dir, f"output_line_{line_number}.wav")
            audio_files.append(output_file)  # Add to list for combining later

            # Main command for Piper
            command = [piper_path, "--model", model_path, "--output_file", output_file]

            try:
                # Send the line to Piper
                process = subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                )
                stdout, stderr = process.communicate(input=line)

                # Check the output
                if process.returncode == 0:
                    print(f"Successfully processed line {line_number}: {line}")
                    print(f"Output saved to: {output_file}")
                else:
                    print(f"Error processing line {line_number}: {line}\n{stderr}")
            except Exception as e:
                print(f"Exception while processing line {line_number}: {line}\n{e}")

    # Combine all audio files into one using ffmpeg
    if audio_files:
        # Create a text file listing all audio files for ffmpeg (with proper path formatting)
        list_file = os.path.join(output_dir, "audio_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for audio_file in audio_files:
                # Use absolute paths with forward slashes for FFmpeg
                abs_path = os.path.abspath(audio_file)
                formatted_path = abs_path.replace("\\", "/")
                f.write(f"file '{formatted_path}'\n")

        # Output file for the combined audio
        combined_output = os.path.join(output_dir, "combined_output.wav")
        abs_combined_output = os.path.abspath(combined_output)
        
        # ffmpeg command to concatenate audio files (using absolute paths)
        ffmpeg_command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", os.path.abspath(list_file),
            "-c", "copy",
            abs_combined_output,
        ]

        try:
            # Run ffmpeg to combine audio files (without changing directory)
            subprocess.run(ffmpeg_command, check=True)
            print(f"All audio files combined into: {combined_output}")
        except subprocess.CalledProcessError as e:
            print(f"Error combining audio files: {e}")
        except Exception as e:
            print(f"Unexpected error during file combination: {e}")
        finally:
            # Clean up the list file
            if os.path.exists(list_file):
                try:
                    os.remove(list_file)
                except:
                    print(f"Could not remove temporary file: {list_file}")

except FileNotFoundError:
    print(f"File not found: {text_file_path}")
    exit(1)
except UnicodeDecodeError:
    print("File is not encoded in UTF-8!")
    exit(1)