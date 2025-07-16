#!/usr/bin/env python3
"""
Script for creating timelapse from saved frames
Can be used independently from the main proxy
Uses OpenCV instead of moviepy
"""

import os
import sys
import glob
import argparse
from datetime import datetime
import cv2

def create_timelapse_video(frames_dir, output_file=None, fps=24, resize_width=None):
    """
    Creates timelapse video from frames in folder using OpenCV
    
    Args:
        frames_dir: Folder with frames
        output_file: Output filename (optional)
        fps: Frames per second
        resize_width: Width to resize to (optional)
    """
    try:
        # Find all JPG files in folder
        image_files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))
        
        if len(image_files) < 2:
            print(f"❌ Not enough frames in folder {frames_dir} (found: {len(image_files)})")
            return False
        
        print(f"🎬 Creating timelapse from {len(image_files)} frames...")
        print(f"📁 Folder: {frames_dir}")
        print(f"🎯 FPS: {fps}")
        
        # Create output filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"timelapse_{timestamp}.mp4"
        
        # Read first frame to check size
        first_frame = cv2.imread(image_files[0])
        if first_frame is None:
            print("❌ Cannot read first frame")
            return False
        
        height, width, _ = first_frame.shape
        print(f"📏 Original size: {width}x{height}")
        
        # Resize if needed
        if resize_width and resize_width != width:
            new_height = int(height * (resize_width / width))
            width, height = resize_width, new_height
            print(f"🔄 Resizing to: {width}x{height}")
        
        # Video information
        duration = len(image_files) / fps
        print(f"📊 Estimated duration: {duration:.1f} seconds")
        print(f"💾 Saving to: {output_file}")
        
        # Configure VideoWriter
        fourcc_options = [
            cv2.VideoWriter_fourcc(*'mp4v'),  # MP4
            cv2.VideoWriter_fourcc(*'XVID'),  # AVI
            cv2.VideoWriter_fourcc(*'MJPG'),  # Motion JPEG
        ]
        
        video_writer = None
        for fourcc in fourcc_options:
            try:
                video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
                if video_writer.isOpened():
                    print(f"✅ Codec configured successfully")
                    break
                else:
                    video_writer.release()
                    video_writer = None
            except:
                continue
        
        if video_writer is None:
            print("❌ Cannot configure VideoWriter")
            return False
        
        # Write frames to video
        print("🎥 Writing frames to video...")
        for i, image_file in enumerate(image_files):
            frame = cv2.imread(image_file)
            if frame is not None:
                # Resize frame if needed
                if resize_width and frame.shape[1] != width:
                    frame = cv2.resize(frame, (width, height))
                
                video_writer.write(frame)
                
                # Show progress every 10 frames
                if i % 10 == 0:
                    print(f"   📝 Processed {i+1}/{len(image_files)} frames...")
        
        # Release VideoWriter
        video_writer.release()
        
        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / 1024 / 1024  # MB
            print(f"✅ Timelapse created: {output_file}")
            print(f"📊 File size: {file_size:.1f} MB")
            return True
        else:
            print("❌ Video file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error creating timelapse: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Creates timelapse from JPG frames using OpenCV")
    parser.add_argument("frames_dir", help="Folder with JPG frames")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-f", "--fps", type=int, default=24, help="Frames per second (default: 24)")
    parser.add_argument("-w", "--width", type=int, help="Width to resize to")
    parser.add_argument("--preview", action="store_true", help="Show information without creating video")
    
    args = parser.parse_args()
    
    # Check if folder exists
    if not os.path.exists(args.frames_dir):
        print(f"❌ Folder {args.frames_dir} does not exist")
        sys.exit(1)
    
    # Check frames
    image_files = sorted(glob.glob(os.path.join(args.frames_dir, "*.jpg")))
    print(f"📁 Folder: {args.frames_dir}")
    print(f"📸 Found frames: {len(image_files)}")
    
    if len(image_files) == 0:
        print("❌ No JPG frames found in folder")
        sys.exit(1)
    
    # Information about first and last frame
    if image_files:
        first_file = os.path.basename(image_files[0])
        last_file = os.path.basename(image_files[-1])
        print(f"🎬 First frame: {first_file}")
        print(f"🎬 Last frame: {last_file}")
        
        # Check sample size
        sample_img = cv2.imread(image_files[0])
        if sample_img is not None:
            height, width, _ = sample_img.shape
            print(f"📏 Frame size: {width}x{height}")
    
    if args.preview:
        duration = len(image_files) / args.fps
        print(f"📊 Estimated duration at {args.fps} FPS: {duration:.1f} seconds")
        return
    
    # Create timelapse
    success = create_timelapse_video(
        args.frames_dir,
        args.output,
        args.fps,
        args.width
    )
    
    if success:
        print("🎉 Success!")
    else:
        print("❌ Error creating timelapse")
        sys.exit(1)

if __name__ == "__main__":
    main() 