
import numpy as np
import collect_states as cs
from sklearn.model_selection import train_test_split

# Stratify example
#https://stackoverflow.com/questions/29438265/stratified-train-test-split-in-scikit-learn

# Sklearn train_test_split
#https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html


if __name__ == "__main__":
    nn = cs.Collection()
    data = cs.read_data()       # Get the data
    labels = cs.read_data("state_data/label.csv")     # Get the labels

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, stratify=labels)
    print("\n\nData was split\n\n")
    print(X_train.shape)


    # Train Model
    nn.model.fit(X_train, y_train, epochs=20, verbose=1)

    # Verify Model
    loss, acc = nn.model.evaluate(X_test, y_test, verbose=2)

    print("Loss: {}\tAcc: {}".format(loss, acc))

    nn.model.save_weights('model_files/nn_01.hdf5')
    print ("Weights saved!")


    jump_ex = [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0]
    npjump = np.asarray(jump_ex)
    re = np.reshape(npjump, (-1,16))
    prediction = nn.model.predict( re )
    one_hot = [0,0,0,0]
    one_hot[np.argmax(prediction[0])] = 1
    print(prediction, "\t", one_hot)
