# Michelle Morales
# OpenMM

import os
import zipfile
import StringIO
import csv
import re

def zip_copy_covarep(dir):
    # Get zip directories
    zip_files = [f for f in os.listdir(dir) if f.endswith('.zip')]
    header = [s.strip() for s in "F0	VUV	NAQ	QOQ	H1H2	PSP	MDQ	peakSlope	Rd	Rd_conf	" \
                                 "creak	MCEP_0	MCEP_1	MCEP_2	MCEP_3	MCEP_4	MCEP_5	MCEP_6	MCEP_7	MCEP_8	MCEP_9	MCEP_10	MCEP_11	MCEP_12	MCEP_13	MCEP_14	MCEP_15	" \
                                 "MCEP_16	MCEP_17	MCEP_18	MCEP_19	MCEP_20	MCEP_21	MCEP_22	MCEP_23	MCEP_24	HMPDM_0	" \
                                 "HMPDM_1	HMPDM_2	HMPDM_3	HMPDM_4	HMPDM_5	HMPDM_6	HMPDM_7	HMPDM_8	HMPDM_9	HMPDM_10	HMPDM_11	HMPDM_12	HMPDM_13	HMPDM_14	HMPDM_15	HMPDM_16	" \
                                 "HMPDM_17	HMPDM_18	HMPDM_19	HMPDM_20	HMPDM_21	" \
                                 "HMPDM_22	HMPDM_23	HMPDM_24	HMPDD_0	HMPDD_1	HMPDD_2	HMPDD_3	HMPDD_4	HMPDD_5	HMPDD_6	HMPDD_7	HMPDD_8	HMPDD_9	HMPDD_10	HMPDD_11	HMPDD_12".split()]
    feature_header = ','.join(header)
    for z in zip_files:
        filename = dir+'/'+z
        pid = z.split('_')[0]
        archive = zipfile.ZipFile(filename, 'r')
        archive_files = archive.namelist()
        for f in archive_files:
            if 'COVAREP' in f:
                new_csv = open('/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Audio_Features/%s_covarep.csv'%pid,'w')
                new_csv.write(feature_header+'\n')
                data = StringIO.StringIO(archive.read(f))  # don't forget this line!
                reader = csv.reader(data)
                for row in reader:
                    new_csv.write(','.join(row)+'\n')


def zip_copy_openface(dir):
    # Get zip directories
    zip_files = [f for f in os.listdir(dir) if f.endswith('.zip')]
    for z in zip_files:
        filename = dir+'/'+z
        pid = z.split('_')[0]
        archive = zipfile.ZipFile(filename, 'r')
        archive_files = archive.namelist()
        for f in archive_files:
            if 'FACET' in f:
                new_csv = open('/Users/michellemorales/Desktop/MoralesDocs/DAIC_WOZ/Video_Features/%s_openface.csv' % pid, 'w')
                data = StringIO.StringIO(archive.read(f))  # don't forget this line!
                reader = csv.reader(data)
                for row in reader:
                    new_csv.write(','.join(row) + '\n')

print('Copying files...')
zip_copy_openface('/Volumes/MORALES/Data/DAIC_WOZ/')
print('DONE copying video files!')