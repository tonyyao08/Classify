Instructions to replicate training and recreate models

Running imageai needs to be done on linux machine
Do following installs:
pip install tensorflow==2.4.0
pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 
	    opencv-python keras-resnet==0.2.0
pip install imageai --upgrade

train_coins python file was used to create the models in this folder
To add train and test file for running tests, must follow a specific folder format
Have a dataset folder in current directory, put train and test folders inside dataset folder
Put images inside a folder that labels what the images are

Ex. For classifying quarters, add train data as follows
    coin_dataset//train//quarter//quarter-images
    coin_dataset//test//quarter//quarter-images

Output: 2 models inside of model folder with end of file names specifying training accuracy
        json file to label each object for testing model on images

TODO: Test models with images of coins from test data
      Train new models with updated data
