import subprocess
import os.path
import moviepy.editor as mp


def extract_visual(video):
    # Extracts visual features using OpenFace, requires the OpenFace () repo to be installed
    csv = video.replace('.mp4', '_openface.csv')
    if os.path.isfile(video):
        try:
            command = '{openface_path} -f {input_file} -of {output_file}'.format(openface_path='OpenFace/build/bin/FeatureExtraction', input_file=video, output_file=csv)
            subprocess.call(command, shell=True)
            print('Success! Visual features saved to {csv}'.format(csv=csv))
        except:
            print('ERROR: Unable to run OpenFace.')
    else:
        print("Video file does not exist.")


def video2audio(video):
    # Converts video to audio
    audio_file = video.replace('.mp4', '.mp3')
    clip = mp.VideoFileClip(video).subclip(0, 20)
    clip.audio.write_audiofile(audio_file)
