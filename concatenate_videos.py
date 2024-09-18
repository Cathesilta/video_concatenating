import subprocess
import os    

class configuration():
    bitrate = '3M'
    resolution = '640:480'
    video_path_dir = 'D:/data/nvidia experience/shadow plays/'
    video_path_list = ['D:/data/nvidia experience/shadow plays/6级玉.mp4','D:/data/nvidia experience/shadow plays/7级玉.mp4',
                       'D:/data/nvidia experience/shadow plays/9级玉.mp4','D:/data/nvidia experience/shadow plays/10级玉.mp4',
                       'D:/data/nvidia experience/shadow plays/打黑白子 - Trim.mp4','D:/data/nvidia experience/shadow plays/zbt - Trim.mp4']
    start_time_list = ['00:00:07.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000']
    end_time_list = ['00:00:18.100','00:10:20','00:00:00.000','00:00:00.000','00:00:00.000','00:00:00.000']
    concatenated_video_path = 'D:/data/nvidia experience/shadow plays/Concatenated.mp4'


class trim_and_concat_videos():

    def __init__(self):

        self.concat_videos()

    def process_video(self, video, start_time, end_time):
        # FFmpeg command to trim the video using GPU and output to a pipe
        command = [
            'ffmpeg','-hwaccel','cuda', '-ss', start_time, '-to', end_time, '-i', video,
            '-c:v', 'h264_nvenc', '-b:v',configuration.bitrate, '-vf',f'scale={configuration.resolution}','-f', 'mpegts', 'pipe:1'
        ]
        command = [
            'ffmpeg','-hwaccel','cuda', '-i', video,
            '-c:v', 'h264_nvenc', '-b:v',configuration.bitrate, '-vf',f'scale={configuration.resolution}','-f', 'mpegts', 'pipe:1'
        ]
        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def concat_videos(self):
        # Start FFmpeg processes for each video to trim and output to pipes
        processes = [self.process_video(video, start_time, end_time) for video,start_time,end_time, in zip(configuration.video_path_list,configuration.start_time_list,configuration.end_time_list)]

        # Start another FFmpeg process to concatenate the videos from the pipes
        concat_command = ['ffmpeg', '-f', 'mpegts','-i', 'pipe:0', 
                        '-c:v','copy',
                        configuration.concatenated_video_path]
        with subprocess.Popen(concat_command, stdin=subprocess.PIPE) as ffmpeg_concat:
            for proc in processes:
                while True:
                    data = proc.stdout.read(1024)
                    if not data:
                        break
                    ffmpeg_concat.stdin.write(data)
                proc.stdout.close()
            ffmpeg_concat.stdin.close()
            ffmpeg_concat.wait()

        # Close all the trimming processes
        for proc in processes:
            proc.wait()




t = trim_and_concat_videos()