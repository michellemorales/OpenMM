import subprocess

def extract_visual(video, openface):
    # Extracts visual features using OpenFace, requires the OpenFace () repo to be installed
    csv = video.replace('.mp4','_openface.csv')
    print('Launching OpenFace to extract visual features... \n\n\n\n\n')
    command = '%s -f %s -of %s'%(openface, video, csv)
    subprocess.call(command, shell=True)
    print 'DONE! Visual features saved to %s' % csv