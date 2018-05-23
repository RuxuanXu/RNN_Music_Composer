
import numpy as np
import midi

def midi_to_onehot(fp):
    
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
<<<<<<< HEAD
            
=======
            #print event
>>>>>>> 36df76b4b4f1bd6374253984e7af75061ba3ccf3
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
<<<<<<< HEAD
=======

    print ('\nNote List (time, pitch, duration): \n')
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(note_list)))
    
    pitch_list = sorted(list(set(pitch_list)))
    duration_list = sorted(list(set(duration_list)))
    p_len = len(pitch_list)
    d_len = len(duration_list)

    note_onehot = [0] * (len(pitch_list)+1) * (len(duration_list)+1)
>>>>>>> 36df76b4b4f1bd6374253984e7af75061ba3ccf3
    notes = []
    
    for i in range(len(note_list)):

<<<<<<< HEAD
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
        
    output_name = 'onehot_' + fp +'.txt'
    with open(output_name, 'w') as f:
        for i in notes:
            f.write("%s\n" % i)
    print("The result of parsing has been saved into %s." % output_name)
=======
        p_idx = pitch_list.index(note_list[i][1])
        d_idx = duration_list.index(note_list[i][2])

        if i == 0:
            if note_list[i][0] == note_list[i+1][0]:
                notes.append(note_to_onehot(-1, -1, p_len, d_len))
            notes.append(note_to_onehot(p_idx, d_idx, p_len, d_len))
        elif i == len(note_list)-1:
            notes.append(note_to_onehot(p_idx, d_idx, p_len, d_len))
            if(note_list[i][0] == note_list[i-1][0]):
                notes.append(note_to_onehot(-1, -1, p_len, d_len))
        else:
            if note_list[i][0] == note_list[i+1][0] and note_list[i][0] != note_list[i-1][0]:
                notes.append(note_to_onehot(-1, -1, p_len, d_len))
            notes.append(note_to_onehot(p_idx, d_idx, p_len, d_len))
            if note_list[i][0] == note_list[i-1][0] and note_list[i][0] != note_list[i+1][0]:
                notes.append(note_to_onehot(-1, -1, p_len, d_len))

    #print('\n'.join('{}: {}'.format(*k) for k in enumerate(notes)))
    
    output_name = 'onehot_' + fp +'.txt'
    with open(output_name, 'w') as f:
       for item in notes:
           f.write("%s\n" % item)
        
def note_to_onehot(pitch, duration, p_len, d_len):
    note_onehot = [0] * (p_len + 1) * (d_len + 1)
    note_onehot [(pitch + 1) * (d_len + 1) + (duration + 1)] = 1
    return note_onehot

>>>>>>> 36df76b4b4f1bd6374253984e7af75061ba3ccf3

