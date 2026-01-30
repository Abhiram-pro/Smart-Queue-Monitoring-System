#!/usr/bin/env python3
"""
Resize video to smaller dimensions using OpenCV
No ffmpeg required - uses cv2 VideoWriter
"""

import cv2
import sys
import os

def resize_video(input_path, output_path, scale=0.5):
    """
    Resize video by scale factor
    
    Args:
        input_path: Input video path
        output_path: Output video path
        scale: Scale factor (0.5 = half size, 0.25 = quarter size)
    """
    print(f"\n{'='*70}")
    print("VIDEO RESIZER")
    print(f"{'='*70}\n")
    
    # Open input video
    print(f"Opening: {input_path}")
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video: {input_path}")
        return False
    
    # Get video properties
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    print(f"\n📊 Original: {original_width}x{original_height} @ {fps:.2f} FPS")
    print(f"📊 New:      {new_width}x{new_height} @ {fps:.2f} FPS")
    print(f"📊 Scale:    {scale*100:.0f}%")
    print(f"📊 Frames:   {total_frames}")
    
    # Setup video writer
    print(f"\n⚙️  Setting up writer...")
    fourcc_options = ['mp4v', 'XVID', 'avc1', 'MJPG']
    writer = None
    
    for fourcc_code in fourcc_options:
        fourcc = cv2.VideoWriter_fourcc(*fourcc_code)
        temp_writer = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
        if temp_writer.isOpened():
            writer = temp_writer
            print(f"✓ Using codec: {fourcc_code}")
            break
        temp_writer.release()
    
    if writer is None:
        print("❌ Error: Could not initialize video writer")
        cap.release()
        return False
    
    # Process frames
    print(f"\n🎬 Processing...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        writer.write(resized_frame)
        
        frame_count += 1
        if frame_count % 30 == 0 or frame_count == total_frames:
            progress = (frame_count / total_frames) * 100
            print(f"  Progress: {frame_count}/{total_frames} frames ({progress:.1f}%)", end='\r')
    
    print(f"\n\n✓ Resized {frame_count} frames")
    
    # Cleanup
    cap.release()
    writer.release()
    
    # Check file sizes
    original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
    new_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    
    print(f"\n📁 File sizes:")
    print(f"   Original: {original_size:.2f} MB")
    print(f"   Resized:  {new_size:.2f} MB")
    print(f"   Saved:    {original_size - new_size:.2f} MB ({(1-new_size/original_size)*100:.1f}% reduction)")
    
    print(f"\n✓ Done! Saved to: {output_path}")
    print(f"{'='*70}\n")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Usage: python3 resize_video.py <input_video> [output_video] [scale]")
        print("\nExamples:")
        print("  python3 resize_video.py test/queue_3.mp4")
        print("  python3 resize_video.py test/queue_3.mp4 test/queue_3_small.mp4")
        print("  python3 resize_video.py test/queue_3.mp4 test/queue_3_small.mp4 0.5")
        print("\nScale options:")
        print("  0.5 = Half size (default)")
        print("  0.25 = Quarter size")
        print("  0.75 = Three-quarter size")
        sys.exit(1)
    
    input_video = sys.argv[1]
    
    # Generate output filename if not provided
    if len(sys.argv) >= 3:
        output_video = sys.argv[2]
    else:
        base, ext = os.path.splitext(input_video)
        output_video = f"{base}_resized{ext}"
    
    # Get scale factor
    scale = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.5
    
    if not os.path.exists(input_video):
        print(f"\n❌ Error: Input video not found: {input_video}")
        sys.exit(1)
    
    success = resize_video(input_video, output_video, scale)
    
    if success:
        print("💡 Now you can analyze the resized video:")
        print(f"   python3 queue_analyzer.py {output_video}")
    else:
        sys.exit(1)
