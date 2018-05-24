import numpy as np
import tensorflow as tf
import random
from file_manager import createDir, readDir

def train():

    #Training setting
    hidden_size   = 100
    seq_len = 20
    gen_len = 1600
    iteration_times = 20001
    output_freq = 500
    initial_learning_rate = 0.1
    decay_steps = 1000
    decay_rate = 0.9

    #Read training data
    data = []
    path = './data/*.txt'
    training_data = readDir(path)
    if training_data==0:
        return 0

    for fi in training_data:
        fi = open(fi, 'r')
        for li in fi:
            li = li.replace("[","")
            li = li.replace("]","")
            note = li.split(',')
            data.append((int(note[0]),int(note[1])))

    note_list = sorted(list(set(data)), key = lambda data: (data[0], data[1]))

    #Convert table
    id_by_note= {(pitch, duration): i for i, (pitch, duration) in enumerate(note_list)}
    note_by_id = {i: (pitch, duration) for i, (pitch, duration) in enumerate(note_list)}

    #Shape Setting 
    inputs     = tf.placeholder(shape=[None, len(note_list)], dtype=tf.float32, name="inputs")
    targets    = tf.placeholder(shape=[None, len(note_list)], dtype=tf.float32, name="targets")
    init_state = tf.placeholder(shape=[1, hidden_size], dtype=tf.float32, name="state")
    initializer = tf.random_normal_initializer(stddev=0.1)

    with tf.variable_scope("RNN") as scope:
        hs_t = init_state
        ys = []
        for t, xs_t in enumerate(tf.split(inputs, seq_len, axis=0)):
            if t > 0: scope.reuse_variables()
            whh = tf.get_variable("whh", [hidden_size, hidden_size], initializer=initializer)
            wxh = tf.get_variable("wxh", [len(note_list), hidden_size], initializer=initializer)
            why = tf.get_variable("why", [hidden_size, len(note_list)], initializer=initializer)
            bh  = tf.get_variable("bh", [hidden_size], initializer=initializer)
            by  = tf.get_variable("by", [len(note_list)], initializer=initializer)

            hs_t = tf.tanh(tf.matmul(xs_t, wxh) + tf.matmul(hs_t, whh) + bh)
            ys_t = tf.matmul(hs_t, why) + by
            ys.append(ys_t)

    hprev = hs_t
    output_softmax = tf.nn.softmax(ys[-1])

    outputs = tf.concat(ys, axis=0)
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=targets, logits=outputs))

    # Optimizer
    global_step = tf.Variable(0, trainable=False)
    learning_rate = tf.train.exponential_decay(initial_learning_rate,
                                           global_step = global_step,
                                           decay_steps = decay_steps, decay_rate = decay_rate)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    learning_step = (optimizer.minimize(loss, global_step=global_step))

    # Initialize
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    hprev_val = np.zeros([1, hidden_size])
    iteration = 0
    para = 0
    createDir('./output/')

    ############ TRAINING LOOP ############
    while iteration<iteration_times:

        # Reset paragraph
        if para + seq_len + 1 >= len(data) or iteration == 0:
            hprev_val = np.zeros([1, hidden_size])
            para = 0  # reset

        # Inputs Setting
        input_vals  = [id_by_note[i] for i in data[para : para + seq_len]]
        target_vals = [id_by_note[i] for i in data[para + 1 : para + seq_len + 1]]
        input_vals  = np.eye(len(note_list))[input_vals]
        target_vals = np.eye(len(note_list))[target_vals]
        
        #Feed RNN
        hprev_val, loss_val, _ = sess.run([hprev, loss, learning_step],
                                          feed_dict={inputs: input_vals, targets: target_vals, init_state: hprev_val})

        if iteration % output_freq == 0:

            #Generate notes
            start_note      = random.randint(0, len(data) - seq_len)
            seq_note = [id_by_note[i] for i in data[start_note:start_note + seq_len]]
            notes          = []
            prev_state = np.copy(hprev_val)

            for i in range(gen_len):
                sample_input_vals = np.eye(len(note_list))[seq_note]
                sample_output_softmax_val, prev_state = \
                    sess.run([output_softmax, hprev],
                             feed_dict={inputs: sample_input_vals, init_state: prev_state })

                note = np.random.choice(range(len(note_list)), p=sample_output_softmax_val.ravel())
                notes.append(note)
                seq_note = seq_note[1:] + [note]
            
            #Output results
            print(('iteration: %d, loss: %f' % (iteration, loss_val)))

            temp = '\n'.join(str(note_by_id[note]) for note in notes)
            output_name = str(iteration) +'.txt'
            with open('./output/' + output_name, 'w') as f:
                f.write('iteration: %d, loss: %f\n' % (iteration, loss_val))
                f.write("----\n%s" % temp)
    
        iteration += 1
        para += seq_len