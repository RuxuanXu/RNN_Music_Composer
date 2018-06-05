import numpy as np
import midi
from file_manager import createDir, readDir, getName

def parse(dir):

    parsing_data = readDir(dir)
    if parsing_data==0:
        return 0
    
    for fp in parsing_data:
        parse_file(fp)

def parse_file(fp):

    pitch_list = []
    duration_list = []
    note_list = []
    #noteon_list[pitch] = tick, the midi pitch range is 128 
    noteon_list = [-1]*128  
    time = 0

    pattern = midi.read_midifile(fp)
    
    for i in range(len(pattern)):
        track = pattern[i]
        for j in range(len(track)):
            event = track[j]
            
            if isinstance(event, midi.NoteEvent):
                time += event.tick

                if isinstance(event, midi.NoteOffEvent) or event.velocity == 0:
                    if noteon_list[event.pitch] != -1:
                        duration = time - noteon_list[event.pitch]
                        if duration: duration_list.append(duration)
                        #append [time, pitch, duration]
                        note_list.append([noteon_list[event.pitch], event.pitch, duration])

                    noteon_list[event.pitch] = -1
                else:
                    pitch_list.append(event.pitch)
                    noteon_list[event.pitch] = time

    #sort note_list by time
    note_list = sorted(note_list, key=lambda x : x[0]) 
    notes = []
    
    for i in range(len(note_list)):

        p = note_list[i][1] 
        d = note_list[i][2] 

        if i == 0:
            if note_list[i][0] == note_list[i+1][0]:
                notes.append([0, -1])
            notes.append([p, d])
        elif i == len(note_list)-1:
            notes.append([p, d])
            if(note_list[i][0] == note_list[i-1][0]):
                notes.append([0, -2])
        else:
            if note_list[i][0] == note_list[i+1][0] and note_list[i][0] != note_list[i-1][0]:
                notes.append([0, -1])
            notes.append([p, d])
            if note_list[i][0] == note_list[i-1][0] and note_list[i][0] != note_list[i+1][0]:
                notes.append([0, -2])

    #set most common duration to 100
    #standard = np.bincount(duration_list).argmax()
    #for i in range(len(notes)):
    #    notes[i][1] = int(notes[i][1]/standard * 100)

    createDir('./data/')
        
    output_name = getName(fp) +'.txt'
    with open('./data/' + output_name, 'w') as f:
        for i in notes:
            f.write("%s\n" % i)
    print("The result of parsing has been saved into %s." % 'data/' + output_name)

def create_midi(fp):

    volumn = 50

    data = []
    fp = open(fp, 'r')
    lines = fp.readlines()[2:]
    for li in lines:
        li = li.replace("(","")
        li = li.replace(")"," ")
        note = li.split(',')
        data.append([int(note[0]),int(note[1])])

    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)
    
    tick = 0
    data_iter=data.__iter__()

    while True:
        try:
            i = data_iter.__next__()
        except StopIteration:
            break
        if i[1]==-1:
            chords = []
            try:
                i = data_iter.__next__()
            except StopIteration:
                break
            temp = i

            while i[1]!=-2:
                while i[1]==-1:
                    try:
                        i = data_iter.__next__()
                    except StopIteration:
                        break
                if i[1]!=-2: chords.append(i)
                try:
                    i = data_iter.__next__()
                except StopIteration:
                    break

            chords = sorted(chords, key=lambda x : x[1]) 

            for n in chords:
                on = midi.NoteOnEvent(tick = 0, velocity=volumn, pitch=n[0])
                track.append(on)
            
            prev = 0
            for n in chords:
                off = midi.NoteOffEvent(tick = n[1]-prev, pitch=n[0])
                track.append(off)
                prev = n[1]

        else:
            if i[0]!=0:
                on = midi.NoteOnEvent(tick = 0,velocity=volumn, pitch=i[0])
                track.append(on)
                off = midi.NoteOffEvent(tick = i[1], pitch=i[0])
                track.append(off)

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    print("The result has been saved as %s.mid." % fp.name)
    midi.write_midifile("{}.mid".format(fp.name), pattern)