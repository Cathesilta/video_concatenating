from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

video = VideoFileClip("D:/data/nvidia experience/shadow plays/Concatenated.mp4")


# Create the first text clip with specific position and duration
text_clip1 = TextClip("Hello, World!", fontsize=50, color='white')
text_clip1 = text_clip1.set_position((100, 400))  # (x, y) position in pixels
text_clip1 = text_clip1.set_start(2).set_duration(4)  # Start at 2 seconds, last for 4 seconds

# Create the second text clip with specific position and duration
text_clip2 = TextClip("Welcome to the Video!", fontsize=50, color='white')
text_clip2 = text_clip2.set_position((100, 400))  # (x, y) position in pixels
text_clip2 = text_clip2.set_start(6).set_duration(3)  # Start at 6 seconds, last for 3 seconds

# Create a composite video with the text overlays
video_with_text = CompositeVideoClip([video, text_clip1, text_clip2])

# Save the final video
video_with_text.write_videofile("output_video.mp4", codec="libx264")