#!/usr/bin/python3.5

"""
Prototype V2
Main Program
By: Xiaochi (George) Li. Adjusted by Jia Chen.
Nov.2018
"""


import MLP_helper_C
import MLP_model
import datetime


# --------------------------------------------------------------------------------------
# Set num_epoch. Here we set it to 5 to run faster. Set to 60 can get the best performance.
num_epoch = 5 
batch_size = 32

# --------------------------------------------------------------------------------------
# Choose the model you want to use. m_3 is the best model we got right now.
model = MLP_model.m_3()

# --------------------------------------------------------------------------------------
# todo: Add Command Line support for epoch and model selection for faster development.
log_name = input("What's the name of this run?:")

# create image label pair as a dictionary
label_file = "../RAFDB/list_patition_label.txt"
folder = "../RAFDB/aligned/"
train_img_label_pair, test_img_label_pair = MLP_helper_C.label_loader(label_file)

# Use pickle to speed up reading data
import pickle
print("Loading Data")
try:
    train_img, train_label, test_img, test_label = pickle.load(open("processed_data_C.pickle", 'rb'))
except:
    train_img, train_label = MLP_helper_C.load_to_numpy(train_img_label_pair, folder)
    test_img, test_label = MLP_helper_C.load_to_numpy(test_img_label_pair, folder)
    print("First time reading data, saving to pickle to speed up next time")
    pickle.dump((train_img, train_label, test_img, test_label), open("processed_data_C.pickle", 'wb'))
    
# --------------------------------------------------------------------------------------
# save model to trained_model_C
import os
if not os.path.exists("./trained_model_C"):
    print("First run, make model dir")
    os.makedirs("./trained_model_C")
    
# --------------------------------------------------------------------------------------
# Keras model and Tensor Board
from tensorflow.keras.callbacks import TensorBoard
import time
tb = TensorBoard(log_dir="logs_MLP/" + log_name +" "+ time.ctime())
# ---------------------------------------------
# Count running time
start_time = datetime.datetime.now()

history = model.fit(train_img, train_label, epochs=num_epoch, batch_size=batch_size,
                    validation_data=(test_img, test_label), callbacks=[tb])

end_time = datetime.datetime.now()
total_time = (end_time - start_time).seconds
print("-------------------------------------")
print("Total running time is:", total_time)
print("-------------------------------------")

# ----------------------------------------------------------------------------------------------------
# Plot validation loss and accuracy
MLP_helper_C.plot(history, log_name, num_epoch)

# ----------------------------------------------------------------------------------------------------
# save model to trained_model_C    
model.save("./trained_model_C/"+log_name+".h5")
loss, accuracy = model.evaluate(test_img, test_label, batch_size=batch_size)
print("test loss:", loss)
print("test accuracy:", accuracy)

