import numpy as np
# read data

def reader(filename):
    with open('deepbaghchal/game/simul/data/'+filename+'.txt', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

        
def pos_parse(pos):
    my_list = list(pos[:25])

    bagh = np.array([1 if x == 'B' else 0 for x in my_list])
    goat = np.array([1 if x == 'g' else 0 for x in my_list])
    if pos[25]=='0':
        phase=np.zeros(25)
    else:
        phase=np.ones(25)

    if pos[26]=='B':
        turn=np.zeros(25)
    else:
        turn=np.ones(25)
    
    concatenated=np.concatenate([bagh,goat,turn,phase])
    return concatenated


def combine_pos(lst):
    my_arr=pos_parse(lst[0])
    for pos in lst[1:]:
        pos_arr=pos_parse(pos)
        my_arr=np.vstack((my_arr, pos_arr))
    return my_arr

def prepare_data():
    bagh=reader('baghWinList')
    bagh_arr=combine_pos(bagh[:7000])
    print(bagh_arr.shape)
    bagh_arr = np.append(bagh_arr, np.expand_dims(np.zeros(len(bagh_arr)), axis=1), axis=1)
    print(bagh_arr.shape)

    goat=reader('goatWinList')
    goat_arr=combine_pos(goat[:7000])
    goat_arr = np.append(goat_arr, np.expand_dims(np.ones(len(goat_arr)), axis=1), axis=1)

    #draw=reader('drawList')

    #concat and shuffle
    both=np.concatenate((bagh_arr,goat_arr), axis=0)
    np.random.shuffle(both)
    return both

# neural net

import tensorflow as tf

# Set up the model architecture
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(100,)),
    tf.keras.layers.Dense(300, activation='relu'),
    tf.keras.layers.Dense(300, activation='relu'),
    tf.keras.layers.Dense(300, activation='relu'),
    tf.keras.layers.Dense(300, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model with an appropriate optimizer, loss function, and metric(s)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



#train function
data=prepare_data()
input_arr=data[:,:-1]
output_arr=data[:,-1]

history = model.fit(input_arr, output_arr, epochs=10, batch_size=32, verbose=1)
# Save the trained model to a file
model.save('my_model.h5')
