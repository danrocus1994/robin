Robin
-----
A sound recognition system intended to provide emotional health  analisys, and suggest treatment options.

Motivation
----------
To bring better support to health care workers, helping them to be more effective with their practice, and to keep in the research of emotional analisys through the spoken communication.


Rosan
-----
Stands by RObin Spectrum ANalizer, is the integrated tool for spectrum analisis, it performs graphical signal drawing for Time and Frequency domains

Screenshots
-----------

Rosan

![](/images/sample.png)


Dependencies
------------

1. Python ^3.6
	* librosa
	* tk
	* sounddevice
	* soundfile
	* wave

2. Ubuntu 18.04 (OS)
	* ffmpeg
	* libportaudio2
	* libasound-dev

Installation
------------

Run the script

```
$ ./install_modules.sh
```

Usage
-----

To run Rosan, be sure of having installed all dependencies

```
$ ./rosan
```
click to 'open file'

and type one of the files in the list without the .wav extension, all audio files are stored in [/recs](/recs) directory,
you can add your own files to analyze.

Architecture
------------

Rosan is the entry point, it joins two cores [docs](GRAPHICS.md):

- [spectrum_analyser.py](spectrum_analyser.py):

Encapsulates the render functions for the Window, Track and Sample elements [docs](AUDIO.md):

- [sound_reader.py](sound_reader.py)

Reads the .wav sound files, and store the raw bytes as an attribute for Audio object


Extras (Test Features)
----------------------

This feature is at creation state, an updated documentation about this feature will be release with the working version.
You can also try to run ```$ ./kivy.sh```

#### Requirement

Install buildozer check the docs at [kivy](https://kivy.org/doc/stable/guide/packaging-android.html)

```
#!/usr/bin/env bash

# Install buildozer
git clone https://github.com/kivy/buildozer.git
cd buildozer
sudo python setup.py install
```

To record the needed data, a kivy test AndroidApp has been builded, using the [buildozer.spec](buildozer.spec) file.

Plug your Android device and run:

```
$ buildozer android debug deploy run
```

Contribute
----------

To add new features just fork this repo and ask for a PR, also please send me an email 
commenting about your experience with emotional health, we can build a community and bring great solutions for this.

Authors
-------
<a href="https://sourcerer.io/danucas"><img src="https://avatars0.githubusercontent.com/u/45695858?v=4" height="50px" width="50px" alt=""/></a>
<a href="https://sourcerer.io/danucas"><img src="https://img.shields.io/badge/Python-783%20commits-orange.svg" alt=""></a>
* Daniel Rodriguez 
	- Gmail [dnart.tech@gmail.com](dnart.tech@gmail.com)
	- Twitter [@Danucas1](https://twitter.com/Danucas1)
	- Linkedin [daniel-rodriguez-castillo](https://www.linkedin.com/in/daniel-rodriguez-castillo/)

	Software engineer from Holberton School interested in visual programming, signal processing, data analisys,
	graphics, sound and a lot of other fields.

Portfolio Project
-----------------
[Data in motion](https://github.com/alejolo311/DataInMotion)


