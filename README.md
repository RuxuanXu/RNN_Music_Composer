# RNN_Music_Composer
Generate music with MIDI files and Tensorflow.

## Instruction
Confirm the following programs are installed on your system: 
* [Python3](https://www.python.org/downloads/)
* [Tensorflow](https://www.tensorflow.org/install/)
* [numpy](http://www.numpy.org/) 
* [python-midi](https://github.com/vishnubob/python-midi/)(install feature/python3 branch)

First, parse MIDI file into text file.
Parse one file at once:
```bash
$ py -c "import midi_parser; midi_parser.parse_file('yourfile.mid')"
```
Or parse multiple files at once:
```bash
$ py -c "import midi_parser; midi_parser.parse('./yourfolder/*.mid')"
```
Then feed the data into RNN:
```bash
$ py -c "import rnn; rnn.train()"
```
When the training is done, convert the result into MIDI file using:
```bash
$ py -c "import midi_parser; midi_parser.create_midi('yourfile.txt')"
```
