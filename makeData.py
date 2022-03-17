import matplotlib.pyplot as plt
import random



def makeDataSet(k):


    # make k random centroids
    centroids = []

    for i in range(k):

        lowerBound = i * 100 + 200
        upperBound = i * 100 + 400

        x = random.randint(lowerBound, upperBound)
        y = random.randint(lowerBound, upperBound)
        c = [x,y]
        centroids.append(c)



    maxMinLimit = 50
    dataList = []
    for c in centroids: # make points for every cluster

        # dataList.append(c) # add cluster centroid to data set

        # interval from where data point can be chosen
        minLimx = c[0] - maxMinLimit
        maxLimx = c[0] + maxMinLimit

        minLimy = c[1] - maxMinLimit
        maxLimy = c[1] + maxMinLimit


        for j in range(100):     # make 100 data points for every cluster

            x = random.randint(minLimx, maxLimx)
            y = random.randint(minLimy, maxLimy)

            dataPoint = [x, y]
            dataList.append(dataPoint)  # add data point to data set

    return dataList


##################################################################################################################

#
#
#
def saveDocument(fileName, dataList):

    with open(fileName, 'w') as f:
        
        for dataPoint in dataList:

            dataPoint = [str(x) for x in dataPoint]

            f.write(dataPoint[0] + '   ' + dataPoint[1] + '\n')
            
##################################################################################################################

# 
# 
#             
def plot(dataList, k):

    
    fig = plt.figure()

    # plot data points
    n = len(dataList)  # nr of data points
    for j in range(n):

        x = dataList[j][0]                 # x-coordinate
        y = dataList[j][1]                 # y-coordinate

        plt.scatter(x, y, s = 10)
        
    plt.title('k-means clustering: ' + str(k) + ' clusters, ' + str(n) + ' data points')
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.show()
    

##################################################################################################################


def main():

    
    k = 6       # nr of clusters
    
    data = makeDataSet(k)

    print('nr of data points: ' + str(len(data)))

    plot(data, k)

    # saveDocument('testfile.txt', dataList)



main()