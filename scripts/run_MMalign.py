import MMalign
import os
import zipfile
import StringIO

dir = '/Volumes/MORALES/Data/DAIC_WOZ/'
zip_files = [f for f in os.listdir(dir) if f.endswith('.zip')]
for z in zip_files[10:]:
    filename = dir + z
    # print filename
    pid = z.split('_')[0]
    archive = zipfile.ZipFile(filename, 'r')
    archive_files = archive.namelist()
    for f in archive_files:
        if 'TRANSCRIPT' in f:
            transcript = StringIO.StringIO(archive.read(f))
        elif 'AUDIO' in f:
            wav_file = StringIO.StringIO(archive.read(f))
    MMalign.get_features(wav_file, transcript, '/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Informed_Features/%s_informed.csv'%pid)