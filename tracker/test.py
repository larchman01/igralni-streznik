import pickle
import os

from Resources.TrackerResources import *


if os.path.isfile(ResFileNames.mapConfigFilePath):
    configMap = pickle.load(open(ResFileNames.mapConfigFilePath, "rb"))

print("hello world")