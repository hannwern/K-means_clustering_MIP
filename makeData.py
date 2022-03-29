import matplotlib.pyplot as plt
import random
import math
import os


filePath = '/Users/Hanna/Documents/KEX/data_sets/'
figPath = '/Users/Hanna/Documents/KEX/plottar/data set plots/'

###########################################################################################################

def makeDataSet(k):


    # make k random centroids
    centroids = []
    ceilSqrtk = math.ceil(math.sqrt(k))

    for A in range(1,ceilSqrtk+1):

        for B in range (1,A+1):
            x = 1000*A
            y = 1000*B
            c = [x,y]
            centroids.append(c)
        
        for C in range (1,A):
            x = 1000*C
            y = 1000*A
            c = [x,y]
            centroids.append(c)
    
    centroids = centroids[0:k]

    
    
    # Annat sätt att få fram clusterpunkter som jag inte tror var lika bra som det övre
    # for xKoordinat in range(1,ceilSqrtk+1):
    #     for yKoordinat in range(1,ceilSqrtk+1):
    #             x = 1000*xKoordinat
    #             y = 1000*yKoordinat
    #             c = [x,y]
    #             centroids.append(c)

    # centroids = centroids[0:k]


    #     a = random.randint(1,1000)

    #     lowerBound = i * a + 100
    #     upperBound = i * a + 500

    #     x = random.randint(lowerBound, upperBound)
    #     y = random.randint(lowerBound, upperBound)
    #     c = [x,y]
    #     centroids.append(c)

    # centroids = [[1000,80], [-100,80], [-2000,-100], [100,-200]]



    maxMinLimit = 100
    dataList = []
    for c in centroids: # make points for every cluster

        # interval from where data point can be chosen
        minLimx = c[0] - maxMinLimit
        maxLimx = c[0] + maxMinLimit

        minLimy = c[1] - maxMinLimit
        maxLimy = c[1] + maxMinLimit


        for j in range(333):     # make 100 data points for every cluster

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
def plotData(data, k):

    
    fig = plt.figure()

    # plot data points
    n = len(data)  # nr of data points
    for j in range(n):

        x = data[j][0]                 # x-coordinate
        y = data[j][1]                 # y-coordinate

        plt.scatter(x, y, c = 'black', s = 5)
        
    plt.title('k-means clustering: ' + str(k) + ' clusters')
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    #plt.show()
    figName = 'dataSet_' +  str(k) + 'clusters' + '.pdf'
    plt.savefig(os.path.join(figPath, figName))
    

##################################################################################################################


def main():

    global filePath

    
    k = 3      # nr of clusters
    
    data = makeDataSet(k)

    print('nr of data points: ' + str(len(data)))

    plotData(data, k)

    fileName = filePath + str(k) +'clusters.txt'

    saveDocument(fileName, data)



main()