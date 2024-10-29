import subprocess

def file_manager():
    filename= "Default_user"
    print("Muxing")
    cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.mov -pix_fmt yuv420p " + filename + ".avi"
    subprocess.call(cmd, shell=True)

file_manager()