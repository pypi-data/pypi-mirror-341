import subprocess
import os
import pyautogui
import cv2
import numpy as np
import time

def record_screen_saver(scr_path, output_mp4, fps=5, duration=10, ffmpeg_path="ffmpeg"):
    """
    Records the screen saver as a video and saves it as MP4.

    Parameters:
    - scr_path: Path to the .scr file.
    - output_mp4: Desired path for the MP4 output.
    - fps: Frames per second for the recording.
    - duration: Duration of the screen recording in seconds.
    - ffmpeg_path: Path to the FFmpeg executable.
    """
    try:
        # Run the screen saver
        subprocess.run(f"start {scr_path}", shell=True)
        
        # Wait for the screen saver to start
        time.sleep(2)
        
        # Record the screen
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        temp_file = "temp.avi"
        out = cv2.VideoWriter(temp_file, fourcc, fps, (screen_size.width, screen_size.height))
        
        for _ in range(int(duration * fps)):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        
        out.release()
        
        # Convert the recorded video to MP4 using FFmpeg
        command = [
            ffmpeg_path,
            "-i", temp_file,
            "-c:v", "libx264",
            "-crf", "23",
            output_mp4
        ]
        subprocess.run(command, check=True)
        
    finally:
        # Remove the temporary AVI file if it exists
        if os.path.exists("temp.avi"):
            os.remove("temp.avi")

def convert_scr_to_mp4(scr_path, output_mp4, ffmpeg_path="ffmpeg", fps=5, duration=10):
    """
    Attempts to convert an SCR file to MP4 using FFmpeg.

    Parameters:
    - scr_path: Path to the SCR file.
    - output_mp4: Desired path for the MP4 output.
    - ffmpeg_path: Path to the FFmpeg executable.
    - fps: Frames per second for the recording.
    - duration: Duration of the screen recording in seconds.
    """
    try:
        # Attempt direct conversion with FFmpeg
        command = [
            ffmpeg_path,
            "-i", scr_path,
            "-c:v", "libx264",
            "-crf", "23",
            output_mp4
        ]
        subprocess.run(command, check=True)
        print(f"Conversion successful: '{scr_path}' -> '{output_mp4}'")
    except subprocess.CalledProcessError:
        print(f"Error: Could not convert '{scr_path}' directly. Attempting screen recording.")
        
        # If direct conversion fails, attempt screen recording
        record_screen_saver(scr_path, output_mp4, fps=fps, duration=duration, ffmpeg_path=ffmpeg_path)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
'''if __name__ == "__main__":
    scr_path = input("Enter the path to the .scr file: ")
    output_mp4 = input("Enter the desired path for the .mp4 file: ")
    ffmpeg_path = input("Enter the path to FFmpeg (default is 'ffmpeg'): ") or "ffmpeg"
    fps = int(input("Enter the desired frames per second (FPS): "))
    duration = int(input("Enter the recording duration in seconds: "))
    
    # Basic input validation
    if not os.path.isfile(scr_path):
        print("Invalid SCR file path.")
    elif not ffmpeg_path:
        print("FFmpeg path is required.")
    else:
        convert_scr_to_mp4(scr_path, output_mp4, ffmpeg_path=ffmpeg_path, fps=fps, duration=duration)'''
