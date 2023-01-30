# Python Smart Chess
Chess game built on pure python programming. Added google speech API just for fun.

## Requirements
- python == 3.6

## How to run on Windows
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
$ python main.py

# Enjoy the game !!
```

## How to run on Linux
```bash
$ python -m venv venv
$ source venv/bin/activate
$ sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
$ pip install pyaudio
$ pip install pygame
$ pip install SpeechRecognition
$ pip install phonetics # Optional
$ python main.py

# Enjoy the game on your favorite machine!!
```

## Solving speech-to-text challenges
Because it is not common to speak 'A2', 'Nf3', etc in real life. The pre-trained recognizer was not performing well, therefore to solve the challenge without using ML,  I used phonetics library to create similar sounding words and then replace those words to chess cell when recognized.

This is my first project after completing python course, and coding chess in 3500+ lines of code without any library was amazing..
