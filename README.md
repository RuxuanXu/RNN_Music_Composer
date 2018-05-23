# RNN_Music_Composer
Generate music with MIDI files and Tensorflow.

## Instruction
Confirm the following programs are installed on your system: 
* [Python3](https://www.python.org/downloads/)
* [Tensorflow](https://www.tensorflow.org/install/)
* [numpy](http://www.numpy.org/) 
* [python-midi](https://github.com/vishnubob/python-midi/)

First, parse MIDI file into text file:
```
python3 -c "import midi_parser; midi_parser.parse('yourfile.mid')"
```
Then feed it into RNN:
```
python3 -c "import rnn; rnn.train('yourfile.txt')"
```
When the training is done, turn the result into MIDI file using:
```
python3 -c "import midi_parser; midi_parser.create_midi('yourfile.txt')"
```
