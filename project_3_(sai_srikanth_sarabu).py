# -*- coding: utf-8 -*-
"""Project- 3 (SAI SRIKANTH SARABU).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ViqqInv-eSm5CZQqPsC7Lb9VaX4e8f55

#SAI SRIKANTH SARABU
#CWID: A20343781
"""

import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install','pyspark'])

from google.colab import drive
drive.mount('/content/drive')

from pyspark import SparkContext, SparkConf
import numpy as np                           #importing numpy for simple calculation
import matplotlib.pyplot as plt              #importing matplotlib for line plot

data= '/content/drive/MyDrive/Sample Data/data.txt'

sc = SparkContext("local","Project-3: k-Means Clustering with PySpark")

allData = sc.textFile(data) #Making complete RDD

#this function converts each number in a line to to float and return List 
def convertToFloat(x):
  floatX = []
  for i in x:
    floatX.append(float(i))
  return floatX 
#the below line splitting the complete data to each line, converting strings to float numbers, assigning index to each line in the data
allDataPoints = allData.map(lambda line: line.split()).map(lambda x:convertToFloat(x)).zipWithIndex().map(lambda x:(x[1],x[0]))

K = 10      #initializing K as number of clusters
I = 20      #initializing I for number of iterations
#below line is taking random K points from the complete data as initial centroids
centroidsDataRDD = sc.broadcast(sc.parallelize(allDataPoints.takeSample(False,K)).collect())

"""**K- Means using Euclidean distance**"""

#Function below will find nearest centroid to point and return the centroid index i.e., the line it is present in the file, its value(all dimenions) and cost of that data point 
def euclDist(x):
  minDist = float('inf')                              #initializing distance to the inifinity
  for i in centroidsDataED.value:                     #looping through all the centroids
    dist = np.sqrt(np.sum(np.square(np.array(x[1]) - np.array(i[1]))))    #subtracting data point value with centroid value, squaring it, adding all those and square rooting it. 
    if dist < minDist:                                #making sure we get minimum distance centroid
      minDist = dist                                  #assigning minimum distance
      clusterNumber = i[0]                            #assigning the cluster number of that minimum distance centroid
  return (clusterNumber,x[1],round(minDist**2,2))     #returning centrioid cluster number, values and cost of the point

costFuncED = []                                       #initializing cost list for I(20) iterations
centroidsDataED = centroidsDataRDD                    #copying initial centroid value 
for i in range(I):                                    #iterating I(20) times
  clusters = allDataPoints.map(lambda x: euclDist(x))       #calling euclDistance() function to get cluster each point it belongs to.
  #below line taking centroid cluster number and value then grouping by the key and making list of all value lists and taking average of that to new centroid
  #and then broadcasting centroids to access in euclDist in next iteration. 
  centroidsDataED = sc.broadcast(clusters.map(lambda x:(x[0],x[1])).groupByKey().mapValues(list).map(lambda x: (x[0],np.average(x[1],axis =0))).collect())
  costFuncED.append(clusters.map(lambda x:x[2]).sum())      #Summing up cost of each point and appending it to the List.

print("\033[1mCost function (Φ) for kmeans using Euclidean distance in 20 iterations\033[0m\n")
for i in range(len(costFuncED)):                #printing cost value for all iterations
  print('Iteration no.'+str(i+1)+':    '+str(costFuncED[i]))

#below lines is copying centroids value after I(20) iterations to a file 
file1 = open("K-Centroids.txt", "w")
file1.write('Centroids of 10 clusters after 20 iterations for Euclidean Distance\n\n')
print('\033[1mCentroids of 10 clusters after 20 iterations for Euclidean Distance \033[0m\n')
for i in range(len(centroidsDataED.value)):
  file1.write('Centroid '+str(i+1)+' ->'+str(list(np.around(centroidsDataED.value[i][1],decimals=2)))+'\n')
  print('Centroid '+str(i+1)+' ->'+str(list(np.around(centroidsDataED.value[i][1],decimals=2))))

"""**K- Means using Manhattan distance**"""

#Function below will find nearest centroid to point and return the centroid index i.e., the line it is present in the file, its value(all dimenions) and cost of that data point 
def manDist(x):
  minDist = float('inf')                                      #initializing distance to the inifinity
  for i in centroidsDataMD.value:                             #looping through all the centroids
    dist = np.sum(np.abs(np.array(x[1]) - np.array(i[1])))    #subtracting data point value with centroid value, taking absolute value, adding all values.
    if dist < minDist:                                        #making sure we get minimum distance centroid
      minDist = dist                                          #assigning minimum distance
      clusterNumber = i[0]                                    #assigning the cluster number of that minimum distance centroid
  return (clusterNumber,x[1],round(minDist,2))                #returning centrioid cluster number, values and cost of the point

costFuncMD = []                                                 #initializing cost list for I(20) iterations
centroidsDataMD = centroidsDataRDD                              #copying initial centroid value
for i in range(I):                                              #iterating I(20) times
  clusters = allDataPoints.map(lambda x: manDist(x))            #calling euclDistance() function to get cluster each point it belongs to.
  #below line taking centroid cluster number and value then grouping by the key and making list of all value lists and taking average of that to new centroid
  #and then broadcasting centroids to access in euclDist in next iteration. 
  centroidsDataMD = sc.broadcast(clusters.map(lambda x:(x[0],x[1])).groupByKey().mapValues(list).map(lambda x: (x[0],np.average(x[1],axis =0))).collect())
  costFuncMD.append(clusters.map(lambda x:x[2]).sum())          #Summing up cost of each point and appending it to the List.

print("\033[1mCost function (Ψ) for kmeans using Manhattan distance in 20 iterations\033[0m\n")
for i in range(len(costFuncMD)):                            #printing cost value for all iterations
  print('Iteration no.'+str(i+1)+':    '+str(costFuncMD[i]))

#below lines is copying centroids value after I(20) iterations to a file
file1.write('\n\nCentroids of 10 clusters after 20 iterations for Manhattan Distance \n\n')
print('\033[1mCentroids of 10 clusters after 20 iterations for Manhattan distance \033[0m \n')
for i in range(len(centroidsDataMD.value)):
  file1.write('Centroid '+str(i+1)+' ->'+str(list(np.around(centroidsDataMD.value[i][1],decimals=2)))+'\n')
  print('Centroid '+str(i+1)+' ->'+str(list(np.around(centroidsDataMD.value[i][1],decimals=2))))
file1.close()

#graph for cost function vs Iterations for Euclean distance
x = [i+1 for i in range(I)]
plt.plot(x, costFuncED, label="Cost function for Euclean distance ");
plt.grid(True,color='k',linestyle=':')

plt.title("Cost vs Iterations K- Means Graph(Euclean distance)");
plt.xlabel("Iterations");
plt.xlim(0,I+1)
plt.xticks(x) 
plt.ylabel("Cost Function (Φ)");
plt.legend(loc=0);

#graph for cost function vs Iterations for Manhattan distance
plt.plot(x, costFuncMD, label="Cost function for manhattan distance ");
plt.grid(True,color='k',linestyle=':')
plt.title("Cost vs Iterations K- Means Graph(Manhattan distance)");
plt.xlabel("Iterations");
plt.xlim(0,I+1)
plt.xticks(x) 
plt.ylabel("Cost Function (Ψ)");
plt.legend(loc=0);

#percentage change in cost function after 10 iterations for Euclidean distance
perChED = ((costFuncED[0] - costFuncED[9])*100)/costFuncED[0]

print('Percentage change in Cost Function(Φ) after 10 iterations for Euclidean Distance is '+'\033[1m'+str(round(perChED,2))+'\033[0m')

#percentage change in cost function after 10 iterations for Manhattan distance
perChMD = ((costFuncMD[0] - costFuncMD[9])*100)/costFuncMD[0]
print('Percentage change in Cost Function(Φ) after 10 iterations for Manhattan distance is '+'\033[1m'+str(round(perChMD,2))+'\033[0m')

"""**Cost function comparision for Euclidean distance and Manhattan distance**

The Cost function for Euclidean distance decreases gradually in each and every iteration after updating the centroid through out 20 iteration, where as cost function for Manhattan distance also decreases but with some slight adjustments in between 20 iterations, after 10 iteration the decrease in cost function for Euclidean distance more than decrease in Manhattan distance. Therefore we can say that Euclidean distance works with better performance than Manhattan distance for the given data.
"""