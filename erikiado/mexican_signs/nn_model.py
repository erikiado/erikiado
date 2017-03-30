import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import ModelCheckpoint
from keras.layers import Activation, Dropout
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Current paths for the files
data_path = '/home/erikiado/Code/benja/dset/dset_t/20x20/'
data_flats = '/home/erikiado/Code/benja/dset/pickles_flat/'
saved = True


def serialize(path_experiment, obj, name_pickle):
    """ Function to serialize the data into a pickle

    """
    try:
        name = name_pickle + '.pickle'
        fp = os.path.join(path_experiment, name)
        with open(fp, 'wb') as handle:
            pickle.dump(obj, handle)
    except Exception as e:
        print(repr(e))


def save_results(path_experiment, history, model):
    """ Function to save the resulting architecture to a json

    """
    print(history.history)
    serialize(path_experiment, history.history, "hist")
    json_string = model.to_json()
    fp = os.path.join(path_experiment, 'my_model_architecture.json')
    open(fp, 'w').write(json_string)


def save_confusion_matrix(y_test, y_pred, encoder):
    """ Function to generate and save a confusion matrix to see in which cases the algorithms
        is performing well
    """
    response = np.unique(y_test)
    labels = []
    for l in response:
        labels.append(encoder.inverse_transform(l))
    conf_arr = confusion_matrix(y_test, y_pred)
    norm_conf = []
    for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j) / float(a))
        norm_conf.append(tmp_arr)
    fig = plt.figure(figsize=(15, 15))
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    width, height = conf_arr.shape
    for x in range(width):
        for y in range(height):
            ax.annotate(str(conf_arr[x][y]), xy=(y, x), horizontalalignment='center',
                        verticalalignment='center')
    ax.set_xticks(list(range(len(labels))))
    ax.set_yticks(list(range(len(labels))))
    ax.set_xticklabels(labels + [''], rotation=90)
    ax.set_yticklabels(labels + [''])
    plt.savefig('confusion_matrix.png', format='png')


def get_folders(path):
    """ Function to get the folders path for the dataset

    """
    folders = {}
    letter_folder = os.listdir(path)
    for l_folder in letter_folder:
        folder_path = path+l_folder+"/"
        folders[l_folder] = folder_path
    return folders


def get_files(directory):
    """ Function to get the images contained in the folder

    """
    imgs = os.listdir(directory)
    return imgs


def main():
    """ Main function in which the architecture is initalized and taken through the process of
        training and testing. This was iterated multiple times in order to achieve better accuracy
        each time based on the parameters

    """
    data = []
    labels = []
    print("Reading...")
    # Read the pickles which contain the images serialized
    for pick in get_files(data_flats):
        with open(data_flats + pick, "rb") as p_file:
            x = pickle.load(p_file)
            for h in x:
                data.append(h)
                labels.append(pick.split(".")[0])
        print("Reading {}...".format(pick.split(".")[0]))

    # Initialize the label encoder which helps identify which label is which output
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    print("Fitted labels {}...".format(len(labels)))
    # Normalize the data
    data = np.array(data) / 255.0
    # Change the order of the dataset since we read it in order it may cause the model to train
    # in an strange form
    idx = np.random.permutation(data.shape[0])
    data, labels = data[idx], labels[idx]
    labels = np_utils.to_categorical(labels, 25)
    print("[INFO] constructing training/testing split...")
    # Actual training process for the model
    (trainData, testData, trainLabels, testLabels) = train_test_split(
        data, labels, test_size=0.25, random_state=42)

    # Define the architecture of the network
    model = Sequential()
    model.add(Dense(400, input_dim=400, init="uniform", activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(300, init="uniform", activation="relu"))
    model.add(Dropout(0.35))
    model.add(Dense(25))
    model.add(Activation("softmax"))

    # Train the model using adam
    print("[INFO] compiling model...")
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    path_model = '/home/erikiado/Code/benja/dset/'

    json_string = model.to_json()
    fp = os.path.join(path_model, 'my_model_architecture.json')
    open(fp, 'w').write(json_string)

    if saved:
        model.load_weights(path_model + '/weights.hdf5')
    print("Done compiling")
    fp = os.path.join(path_model, 'weights.hdf5')
    checkpointer = ModelCheckpoint(filepath=fp, verbose=1, save_best_only=True)
    hist = model.fit(trainData, trainLabels, nb_epoch=40, batch_size=32,
                     validation_data=(testData, testLabels), callbacks=[checkpointer], verbose=1)

    # Show the accuracy on the testing set
    print("[INFO] evaluating on testing set...")
    (loss, accuracy) = model.evaluate(testData, testLabels, batch_size=32, verbose=1)
    print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))

    y_pred = model.predict_classes(testData)
    print('pred shape: %d' % (y_pred.shape))
    # Save the model and results after training
    save_confusion_matrix(testLabels.argmax(axis=-1), y_pred, le)
    save_results(path_model, hist, model)


main()
