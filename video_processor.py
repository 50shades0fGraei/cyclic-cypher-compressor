
import os
import subprocess
import sys
import struct
import tempfile
import shutil

# Add the 'core' directory to the Python path for the hybrid engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from cyclic_hybrid import compress_realtime, decompress_realtime

def compress_video(video_path, output_path):
    """
    Compresses a video file into a .cvp (Compressed Video Package).

    The process:
    1. Create a temporary directory.
    2. Use ffmpeg to extract video frames as PNG images into the temp directory.
    3. For each frame, use the cyclic_hybrid engine to compress it.
    4. Write each compressed frame into a single .cvp file, with a header
       indicating the length of each frame's data.
    5. Clean up the temporary directory.
    """
    print(f"--- Starting Video Compression for {video_path} ---")
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    # Create a temporary directory to store frames
    temp_dir = tempfile.mkdtemp(prefix="video_frames_")
    print(f"1. Created temporary directory: {temp_dir}")

    # 2. Extract frames using ffmpeg
    print("2. Extracting frames from video...")
    frame_pattern = os.path.join(temp_dir, 'frame-%06d.png')
    try:
        # We also get the framerate to use it during decompression
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
        framerate_proc = subprocess.run(ffprobe_cmd, check=True, capture_output=True, text=True)
        framerate = framerate_proc.stdout.strip()

        ffmpeg_cmd = ['ffmpeg', '-i', video_path, frame_pattern]
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print("Frame extraction complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frames: {e.stderr}")
        shutil.rmtree(temp_dir)
        return
    except FileNotFoundError:
        print("Error: 'ffmpeg' or 'ffprobe' not found. Please ensure they are installed and in your PATH.")
        shutil.rmtree(temp_dir)
        return

    # 3. Compress each frame and write to the output file
    print("3. Compressing frames and building package...")
    frame_files = sorted([f for f in os.listdir(temp_dir) if f.endswith('.png')])

    with open(output_path, 'wb') as f_out:
        # Write a simple header: Magic bytes, version, and framerate
        f_out.write(b'CVP1')
        f_out.write(framerate.encode('utf-8').ljust(16))

        for frame_file in frame_files:
            frame_path = os.path.join(temp_dir, frame_file)
            compressed_frame_path = frame_path + '.compressed'
            
            # Compress the frame using the hybrid engine
            compress_realtime(frame_path, compressed_frame_path)
            
            # Read the compressed data
            with open(compressed_frame_path, 'rb') as f_in:
                compressed_data = f_in.read()
            
            # Write the length of the upcoming data chunk, then the data itself
            f_out.write(struct.pack('>Q', len(compressed_data)))
            f_out.write(compressed_data)

    print(f"4. Successfully created compressed package: {output_path}")

    # 5. Clean up
    shutil.rmtree(temp_dir)
    print("5. Cleaned up temporary files.")
    print("--- Compression Complete ---")


def decompress_video(video_path, output_path):
    """
    Decompresses a .cvp file back into a playable video.

    The process:
    1. Create a temporary directory.
    2. Read the .cvp file frame by frame.
    3. For each compressed frame data, save it to a temporary file.
    4. Use the cyclic_hybrid engine to decompress the temporary file into a PNG.
    5. Use ffmpeg to assemble the decompressed PNG frames into a video.
    6. Clean up the temporary directory.
    """
    print(f"--- Starting Video Decompression for {video_path} ---")
    if not os.path.exists(video_path):
        print(f"Error: Compressed video package not found at {video_path}")
        return

    temp_dir = tempfile.mkdtemp(prefix="video_frames_")
    print(f"1. Created temporary directory: {temp_dir}")
    
    # 2. Read the package and decompress frames
    print("2. Reading package and decompressing frames...")
    frame_count = 0
    with open(video_path, 'rb') as f_in:
        # Read header
        magic = f_in.read(4)
        if magic != b'CVP1':
            print("Error: Not a valid .cvp file (magic bytes mismatch).")
            shutil.rmtree(temp_dir)
            return
        
        framerate = f_in.read(16).strip(b'\x00').decode('utf-8')
        print(f"Original framerate: {framerate}")

        while True:
            # Read the length of the next chunk
            length_bytes = f_in.read(8)
            if not length_bytes:
                break # End of file
            
            chunk_length = struct.unpack('>Q', length_bytes)[0]
            compressed_data = f_in.read(chunk_length)
            
            frame_count += 1
            temp_compressed_path = os.path.join(temp_dir, f"frame_{frame_count}.compressed")
            temp_decompressed_path = os.path.join(temp_dir, f"frame-%06d.png" % frame_count)

            with open(temp_compressed_path, 'wb') as f_temp:
                f_temp.write(compressed_data)
            
            # Decompress the frame using the hybrid engine
            decompress_realtime(temp_compressed_path, temp_decompressed_path)

    print(f"Decompressed {frame_count} frames.")

    # 5. Re-assemble video using ffmpeg
    print("3. Assembling frames into video...")
    frame_pattern_in = os.path.join(temp_dir, 'frame-%06d.png')
    try:
        ffmpeg_cmd = [
            'ffmpeg',
            '-framerate', framerate,
            '-i', frame_pattern_in,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"4. Successfully created decompressed video: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error assembling video: {e.stderr}")
        shutil.rmtree(temp_dir)
        return
    except FileNotFoundError:
        print("Error: 'ffmpeg' not found. Please ensure it is installed and in your PATH.")
        shutil.rmtree(temp_dir)
        return

    # 6. Clean up
    shutil.rmtree(temp_dir)
    print("5. Cleaned up temporary files.")
    print("--- Decompression Complete ---")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python video_processor.py <compress|decompress> <input_file> <output_file>")
        sys.exit(1)

    command = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if command.lower() == 'compress':
        compress_video(input_file, output_file)
    elif command.lower() == 'decompress':
        decompress_video(input_file, output_file)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
