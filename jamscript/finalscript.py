

import numpy
from numpy.random import seed
numpy.random.seed(1)
from tensorflow import set_random_seed
set_random_seed(1)
seed = 1
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.models import load_model
import json


df = pd.read_csv('sensor_readings_2.data', header = None)

nooflayers = 2 #noofhiddenlayers defined
noofneurons = 3 #noofneurons in each hidden layer

dataset = df.values

noofcol = len(df.columns)
Xorig = dataset[0:100,0:noofcol-1]
Yorig = dataset[0:100,noofcol-1]
X,Xtest,Y,Ytest = train_test_split(Xorig, Yorig, test_size = 0.2, random_state =seed)
noofoutput = len(numpy.unique(Y))


encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
for i in range(0,nooflayers):
    model.add(Dense(noofneurons, input_dim=noofcol-1, activation='sigmoid', use_bias = True))
model.add(Dense(noofoutput, activation='sigmoid', use_bias = True))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
model.fit(X, dummy_y, epochs=500, verbose = False)



model.save('model.h5')
model1 = load_model('model.h5')

predict = model1.predict(X[:,0:noofcol-1])
predicttest = model1.predict(Xtest)
encoder.fit(Ytest)
encoded_ytest = encoder.transform(Ytest)
dummytest = np_utils.to_categorical(encoded_ytest)

temp = numpy.floor(predicttest/predicttest.max(axis=1)[:,None])

value = numpy.sum(temp == dummytest, axis = 1)

print(numpy.float32(sum(value == 4))*100/len(value))

noofinputs = (model1.layers[0].get_weights()[0].shape[0])
noofneurons = model1.layers[0].get_weights()[0].shape[1]
noofoutputs = model1.layers[1].get_weights()[0].shape[1]

out1 = {'network':{'noofinputs': noofinputs, 'noofneuronsineachlayer':noofneurons, 'noofoutputs':noofoutputs, 'noofhiddenlayers': nooflayers}}

listoflayers = range(nooflayers)
data2 = {}
for layer in listoflayers:
    listofneurons = range(noofneurons)
    bias = map(str,model1.layers[layer].get_weights()[1])
    arrayofneurons= []
    for counter in listofneurons:
        current = ({'id':counter+1, 'bias' :bias[counter], 'weights':map(str, model1.layers[layer].get_weights()[0][:,counter])})
        arrayofneurons.append(current)
    data2.update({'hiddenlayer%s' %(layer+1): [{'neurons': arrayofneurons}]})



outputbias = map(str, model1.layers[nooflayers].get_weights()[1])
outputweights = model1.layers[nooflayers].get_weights()[0]

arrayofoutputneurons = []
listofneurons = range(noofoutputs)
for counter in listofneurons:
    current = ({'id':counter+1, 'bias': outputbias[counter], 'weights':map(str, outputweights[:,counter])})
    arrayofoutputneurons.append(current)
data3 = {'outputlayer':[{'neurons': arrayofoutputneurons}]}

with open('network.json','w') as outfile:
   json.dump(out1, outfile, indent =4)

with open('hiddenlayer.json','w') as outfile:
   json.dump(data2, outfile, indent = 4)

with open('outputlayer.json','w') as outfile:
    json.dump(data3, outfile, indent =4)

print('Values saved to files')
