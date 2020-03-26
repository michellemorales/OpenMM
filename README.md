OpenMM: An Open-source Multimodal Feature Extraction Tool
=============

OpenMM is an open-source tool that can perform multimodal feature extraction. In other words, this tool will allow you to easily extract video, audio, and linguistic features all at once. This tool builds upon existing GitHub repos for visual feature extraction [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace) and audio feature extraction [Covarep](https://github.com/covarep/covarep). I integrate these existing repos with my code for linguistic feature extraction (LingAnalysis). OpenMM provides a simple way for researchers to extract multimodal features. The tool only requires a video as input and outputs a csv of multimodal features, audio conversion and speech-to-text are handled internally. My hope is that this will help promote more interest and research in building multimodal systems. 

![alt tag](https://github.com/michellemorales/OpenMM/blob/master/images/PipelineVersion3.jpeg)

## Installation
Please see the Wiki for installation instructions.

## Citing

If you use any of this code in your work, please cite:

OpenMM: An Open-Source Multimodal Feature Extraction Tool (Michelle Renee Morales, Stefan Scherer, Rivka Levitan), In Proceedings of Interspeech 2017, ISCA, 2017. 

```
@inproceedings{morales_openmm:_2017,
	address = {Stockholm, Sweden},
	title = {{OpenMM}: {An} {Open}-{Source} {Multimodal} {Feature} {Extraction} {Tool}},
	url = {https://www.researchgate.net/publication/319185055_OpenMM_An_Open-Source_Multimodal_Feature_Extraction_Tool},
	doi = {10.21437/Interspeech.2017-1382}}
```

## Note
This repo represents code from my dissertation work. I did my best to ensure that the code runs out of the box, but there are always issues. So please understand that this is research code and not a commercial level product. However, if you encounter any problems/bugs/issues please contact me on github or email me at ms.morales3@gmail.com for any bug reports/questions/suggestions.

## Installation

These instructions were tested on a Mac running macOS Sierra Version 10.12.4. 

In order to get OpenMM to work you need to have the following things installed

### Python Modules
In order to run OpenMM, you'll need to install [Python 2.7](https://www.python.org/downloads/) (Python 3 support is not available yet) and the following Python modules:

* [numpy and scipy](https://www.scipy.org/install.html): packages for scientific computing
* [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html): package for data structures and data analysis
* [speech_recognition](https://github.com/Uberi/speech_recognition): package for interacting with speech recognition APIs 

You can install them all at once using pip:
`pip install numpy scipy pandas SpeechRecognition`

### Matlab Runtime Version
In order to use Covarep to extract acoustic features, you also need the 2017 Matlab Runtime version for your machine, which is free and available to download on their [site](https://www.mathworks.com/products/compiler/mcr.html). 

### ffmpeg
In order to convert video to audio, you need to [ffmpeg](https://ffmpeg.org/download.html) installed:

`brew install ffmpeg`

### OpenFace
To perform visual feature extraction OpenMM requires [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace).

### Parsers
To extract syntactic features, which are part of the linguistic analysis, [SyntaxNet](https://github.com/tensorflow/models/tree/master/syntaxnet) parser is required. We suggest following these [instructions](http://www.whycouch.com/2016/07/how-to-install-and-use-syntaxnet-and.html) to download. If you plan on working with German or Spanish data, make sure to also add those models to your Docker container. Here are the [instructions](https://github.com/tensorflow/models/blob/master/syntaxnet/g3doc/universal.md) for downloading the other language models. 

### OpenMM Install
After all the prerequisities and dependencies are installed successfully. You can install OpenMM by cloning this repo:

`git clone https://github.com/michellemorales/OpenMM.git`


