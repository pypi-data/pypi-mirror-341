import os
import subprocess

class VideoConverter:
    def __init__(self, ffmpeg_path="ffmpeg"):
        """
        Initialize with FFmpeg path
        Parameters:
            ffmpeg_path (str): Path to FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path

    def mov_to_mp4(self, input_mov, output_mp4):
        """
        Convert MOV to MP4
        Parameters:
            input_mov (str): Input MOV file path
            output_mp4 (str): Output MP4 file path
        """
        if not os.path.exists(input_mov):
            raise FileNotFoundError(f"Input file '{input_mov}' not found")

        command = [
            self.ffmpeg_path,
            "-i", input_mov,
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_mp4
        ]

        try:
            subprocess.run(command, check=True, capture_output=True)
            print(f"MOV to MP4 conversion successful: {output_mp4}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"MOV conversion failed: {e.stderr.decode()}")

    def mp4_to_scr(self, input_mp4, output_scr):
        """
        Convert MP4 to SCR (placeholder implementation)
        Parameters:
            input_mp4 (str): Input MP4 file path
            output_scr (str): Output SCR file path
        """
        if not os.path.exists(input_mp4):
            raise FileNotFoundError(f"Input file '{input_mp4}' not found")

        temp_noaudio = "temp_noaudio.mp4"
        
        # Remove audio
        try:
            subprocess.run([
                self.ffmpeg_path,
                "-i", input_mp4,
                "-an",
                "-vcodec", "copy",
                temp_noaudio
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Audio removal failed: {e.stderr.decode()}")

        # Create SCR placeholder (actual implementation would require proper compilation)
        try:
            with open(output_scr, "wb") as scr_file:
                scr_file.write(b"SCR_PLACEHOLDER_HEADER\n")
                with open(temp_noaudio, "rb") as video_file:
                    scr_file.write(video_file.read())
        finally:
            if os.path.exists(temp_noaudio):
                os.remove(temp_noaudio)

        print(f"MP4 to SCR conversion complete: {output_scr}")

    def convert_mov_to_scr(self, input_mov, output_scr):
        """Handle full conversion pipeline"""
        # Generate intermediate MP4 path
        base = os.path.splitext(input_mov)[0]
        intermediate_mp4 = f"{base}_temp.mp4"
        
        try:
            self.mov_to_mp4(input_mov, intermediate_mp4)
            self.mp4_to_scr(intermediate_mp4, output_scr)
        finally:
            if os.path.exists(intermediate_mp4):
                os.remove(intermediate_mp4)

# Usage Example
if __name__ == "__main__":
    converter = VideoConverter()
    
    try:
        converter.convert_mov_to_scr(
            input_mov="input.mov",
            output_scr="output.scr"
        )
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        exit(1)
