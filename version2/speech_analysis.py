import speech_recognition as sr
import librosa
import pandas as pd
import numpy as np
from librosa import feature


def get_feature_vector(y, sr):
    """Extract acoustic features mean values."""
    fn_list_i = [
        feature.chroma_stft,
        feature.spectral_centroid,
        feature.spectral_bandwidth,
        feature.spectral_rolloff]

    fn_list_ii = [
        feature.rms,
        feature.zero_crossing_rate]

    feat_vect_i = [np.mean(funct(y, sr)) for funct in fn_list_i]
    feat_vect_ii = [np.mean(funct(y)) for funct in fn_list_ii]

    # Add MFCCs
    S = feature.melspectrogram(y, sr=sr)
    log_S = librosa.power_to_db(S, ref=np.max)
    mfcc = feature.mfcc(S=log_S, n_mfcc=13)
    mfcc_mean = [np.mean(x) for x in mfcc]

    # Add Tempo
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.tempo(onset_env, sr=sr)
    feature_vector = feat_vect_i + feat_vect_ii + mfcc_mean + tempo
    return feature_vector


def get_feature_header():
    """Create acoustic feature names."""
    audio_feature_names = [
        'chroma_stft',
        'spectral_centroid',
        'spectral_bandwidth',
        'spectral_rolloff',
        'rmse',
        'zero_crossing_rate']
    mfccs = ['mfcc_{}'.format(x) for x in range(1, 14)]
    audio_feature_names += mfccs
    audio_feature_names += ['tempo']
    return audio_feature_names


def extract_audio(audio):
    """Generate acoustic features."""
    y, sr = librosa.load(audio) # time-series-array (y) and a sampling rate(sr), ie. digital representation of the audio
    acoustic_feats = get_feature_vector(y=y, sr=sr)
    acoustic_feats_names = get_feature_header()
    print(acoustic_feats_names)
    acoustic_df = pd.DataFrame(acoustic_feats, columns=acoustic_feats_names)

    # Save acoustic features to csv file
    csv = audio.replace('.wav', '_acoustic.csv')
    acoustic_df.to_csv(csv, index=False)
    return acoustic_df


def speech_recognizer(audio):
    """Convert speech file to text transcript."""
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        read_audio = r.record(source)  # read the entire audio file

    # Recognize speech using Sphinx
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
