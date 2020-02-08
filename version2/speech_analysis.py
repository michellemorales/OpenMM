import speech_recognition as sr


def speech_recognizer(audio):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        read_audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        transcript = r.recognize_sphinx(read_audio)
        print("Sphinx thinks you said " + transcript)
        transcript_file = audio.replace('.wav', '_transcript.txt')
        with open(transcript_file, 'w') as out_file:
            out_file.write(transcript)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
