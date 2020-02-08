import speech_recognition as sr

AUDIO_FILE = "../Examples/FerrisBuellerClip.wav"


def speech_recognizer():
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        transcript = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + transcript)
        with open("transcript.txt", 'w') as out_file:
            out_file.write(transcript)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


# speech_recognizer()
