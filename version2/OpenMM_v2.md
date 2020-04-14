# Things To Do
- Set up machine: github, pycharm, terminal, python install
- Research on State of the art in NLP: 
    - https://github.com/sebastianruder/NLP-progress
    - https://www.analyticsvidhya.com/blog/2019/03/pretrained-models-get-started-nlp/
    - State of the art POS tagging results - https://github.com/zalandoresearch/flair (paper https://www.aclweb.org/anthology/N19-4010/)
- Create requirements file - https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository
- Parsey mcparseface - 2016
- Universal Dependencies: https://universaldependencies.org/


## Features & Models
### Syntax:
Leverages the Stanford NLP tool for tagging and parsing which uses  Universal Dependencies: (UD) is a framework for consistent annotation of grammar (parts of speech, morphological features, and syntactic dependencies) across different human languages. 
Learn more here: https://universaldependencies.org/
### Speech recognition
Originally used watson/google in speech to text which is online - updated the tool to use Pocketsphinx which is offline - however tool supports 
any of hte following: google, microsoft, watson, pocketsphinx via the `SpeechRecognition` python library. To change from the default
go to the `speech_analysis.py` file and make any updates
### Acoustic analysis
Original tool used was Covarep (https://github.com/covarep/covarep), a library written in Matlab
which was difficult to get set-up due to the need to download and install the runtime version of matlab.
The library has also not been updated in many years. So in v2 OpenMM uses Opensmile. For 
its robust set of features. The latest stable release of openSMILE can be found at http://opensmile.audeering.com/.
The version used in this release of OpenMM is Opensmile 2.3.0 

Opensmile is a bit complicated to install on my Mac. I ran into a few errors and
needed to make some changes to the build scripts, I followed the advice of these two threads: 

https://stackoverflow.com/questions/42736091/macos-configure-error-c-compiler-cannot-create-executables
https://github.com/naxingyu/opensmile/issues/10

Librosa (https://librosa.github.io/)
features extracted = https://medium.com/tencent-thailand/music-information-retrieval-part-1-using-librosa-to-extract-audio-features-6e8569537185
https://medium.com/@alexandro.ramr777/audio-files-to-dataset-by-feature-extraction-with-librosa-d87adafe5b64

For those new to acoustic analysis this site provides a good intro to
understanding sound waveforms: https://pudding.cool/2018/02/waveforms/


Comprehensive list of available packages - https://github.com/faroit/awesome-python-scientific-audio
### Facial analysis
OpenFace(https://github.com/TadasBaltrusaitis/OpenFace/wiki/) is still used in this latest version release. Although not built or run in Python. It is relatively easy to install
, has great documentation, and does work well out of the box. You **must install** this prior to running OpenMM 2.0. 
The latest version of OpenFace includes state-of-the-art algoirthms for facial landmark detection, head pose estimation, facial action unit recognition, 
and eye-gaze estimation, further making a great chioce for inclusions in our tool. Moreover, OpenFace is still being maintained. 

Although installation is a bit complicated requiring many prerequisites, installation does work without error (at least for Mac). 
The following prerequisites are needed (see more detailed list on the wiki page- https://github.com/TadasBaltrusaitis/OpenFace/wiki/Mac-installation :
- Download XQuartz
- dl landmark files via bash script did not work for me had to do it manually

```brew update
  brew install gcc --HEAD
  brew install boost
  brew install tbb
  brew install openblas
  brew install --build-from-source dlib
  brew install wget
  brew install opencv
```
 
Alternatives:
https://github.com/opencv/opencv 
OpenCV (https://opencv.org)
FAQ (https://answers.opencv.org/questions/)
Installing OpenCV (on Mac) -
https://www.learnopencv.com/install-opencv3-on-macos/

If you'd like to use one of the alternatives you can make the updates to the `video_analysis.py` script