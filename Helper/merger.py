from moviepy.editor import VideoFileClip, AudioFileClip
from Helper import Logger

class MergerMovie():
    def merge(self):
        # Load the video file
        video = VideoFileClip("C:/Users/ASUS/PycharmProjects/mezun/ViewModel/Outputs/temp_video.mov")

        # Load the audio file
        audio = AudioFileClip("C:/Users/ASUS/PycharmProjects/mezun/ViewModel/Outputs/temp_audio.wav")

        # Set the audio of the video clip
        final_video = video.set_audio(audio)

        # Define the output file path
        output_file = "C:/Users/ASUS/PycharmProjects/mezun/ViewModel/Outputs/merged_output_video.mov"

        # Write the final video file with the new audio
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

        # Close the clips to release resources
        video.close()
        audio.close()
        final_video.close()

        # Write the logger
        logger = Logger.Log()
        logger.info("Video and audio were merged!")