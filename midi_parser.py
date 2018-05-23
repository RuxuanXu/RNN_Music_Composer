
import numpy as np
import midi

def parse(fp):
    
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
                        duration_list.append(duration)
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
                notes.append([0, 0])
            notes.append([p, d])
        elif i == len(note_list)-1:
            notes.append([p, d])
            if(note_list[i][0] == note_list[i-1][0]):
                notes.append([0, 0])
        else:
            if note_list[i][0] == note_list[i+1][0] and note_list[i][0] != note_list[i-1][0]:
                notes.append([0, 0])
            notes.append([p, d])
            if note_list[i][0] == note_list[i-1][0] and note_list[i][0] != note_list[i+1][0]:
                notes.append([0, 0])
        
    output_name = fp +'.txt'
    with open(output_name, 'w') as f:
        for i in notes:
            f.write("%s\n" % i)
    print("The result of parsing has been saved into %s." % output_name)

