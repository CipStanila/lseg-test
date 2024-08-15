import os

#Cleanup the outputs folder

if (os.path.exists('outputs')):
    files = os.listdir('outputs')
    for file in files:
        os.remove('outputs\\' + file)
    os.rmdir('outputs')
