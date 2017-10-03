import FeatureExtract
import LingAnalysis


my_dir = sys.argv[1]
lang = sys.argv[2]
config = sys.argv[3]
json_file = open(config, "r").read()
pars = json.loads(json_file)

# Get video files from directory
files = os.listdir(my_dir)

# VIDEO
# First, check that the video is the right .mp4 format
# video_files = [f for f in files if f.endswith('.mp4')]
# openface = pars["OPENFACE"]
# for f in video_files:
#     extract_visual(os.path.join(my_dir, f), openface)
#     video2audio(os.path.join(my_dir, f))
#
# # AUDIO
# # Point to matlab runtime application
# matlab = pars["MATLAB_RUNTIME"]
# extract_audio(my_dir, matlab)
#
# # SPEECH2TEXT
# audio_files = [f for f in os.listdir(my_dir) if f.endswith('.wav')]
# google_key = str(pars['GOOGLE_API_KEY'])
# ibm_pass = str(pars["IBM_PASSWORD"])
# ibm_un = str(pars["IBM_USERNAME"])
# for f in audio_files:
#     if lang == 'english':
#         ibm_speech2text(os.path.join(my_dir, f), 'en-US', ibm_un, ibm_pass)
#     elif lang == 'spanish':
#         ibm_speech2text(os.path.join(my_dir, f), 'es-ES', ibm_un, ibm_pass)
#     # If language in german use Google's API
#     elif lang == 'german':
#         google_speech2text(os.path.join(my_dir, f), 'de-DE', google_key)

# LING
transcript_files = [f for f in os.listdir(my_dir) if f.endswith('_transcript.txt')]
parser_dir = pars["syntaxnet"]
if lang == 'english':
    bag = LingAnalysis.bag_of_words(my_dir, transcript_files)
    for tf in transcript_files:
        LingAnalysis.get_feats(os.path.join(my_dir, tf), bag, lang, parser_dir)

elif lang == 'german':
    bag = LingAnalysis.bag_of_words(transcript_files)
    for tf in transcript_files:
        LingAnalysis.get_feats(os.path.join(my_dir, tf), bag, lang, parser_dir)

elif lang == 'spanish':
    bag = LingAnalysis.bag_of_words(transcript_files)
    for tf in transcript_files:
        LingAnalysis.get_feats(os.path.join(my_dir, tf), bag, lang, parser_dir)

# FUSION
# transcript_files = [f for f in os.listdir(my_dir) if f.endswith('_transcript.txt')]
# for f in transcript_files:
#     early_fusion(os.path.join(my_dir, f))

# Combine all data instances into one csv
# one_csv(my_dir)

# Convert json to txt files
# transcript_files = [f for f in os.listdir(dir) if f.endswith('_transcript.json')]
# for f in transcript_files:
#     json2txt(os.path.join(dir,f))