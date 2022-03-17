from re import I
from typing_extensions import runtime
import numpy as np
import gurobipy as gp 
import random
import matplotlib.pyplot as plt
import math



###################################################################################################################
# TEXT DOCUMENTS WITH DATA
D128C2File = 'g2-128-10.txt'    # 128-dimenisional data with 2 clusters
D64C2File = 'g2-64-10.txt'      # 64-dimenisional data with 2 clusters
D32C2File = 'g2-32-10.txt'      # 32-dimenisional data with 2 clusters
D8C2File = 'g2-8-10.txt'        # 8-dimenisional data with 2 clusters
D4C2File = 'g2-4-10.txt'        # 4-dimenisional data with 2 clusters
D2C9File = 'D2.txt'             # 2-dimenisional data with 9 clusters
D2C2File = 'g2-2-10.txt'        # 2-dimenisional data with 2 clusters


# SET PARAMETERS
clusters = 2     # nr of clusters of data chosen above
iterations = 9  # nr of iterations the program will do.
nodesVector = []    #list where the number of nodes per iteration is stored
runtimeVector = []  #list where the runtime of  each iteration is stored
for i in range(iterations):
    nodesVector.append(0)
    runtimeVector.append(0)



###################################################################################################################

# IN: fileName (string), .txt file
# OUT: numpy array where each element corresponds to a list representing a data point
# reads .txt documents 
def readFile(fileName):

    with open(fileName, 'r') as f:

        # makes every line in .txt file into list with string
        content = f.readlines()

        # make list where list of strings will be saved
        dataList = []
        for line in content:
            
            newLine = line.strip('\n').split()  # remove line end
            
            dataPoint = []
            for data in newLine:
                dataPoint.append(int(data)) 
            
            dataList.append(dataPoint)   # adds every dataPoint list to list
            
        dataArray = np.array(dataList, dtype=float)

    return dataArray



###################################################################################################################

# IN: dataArray: numpy array where each element corresponds to a list representing a data point
#     n: int, how many random data points we want
# OUT: randomArray: numpy array of shorter version of dataArray
# picks n random data points from dataList and returns them in a numpy array
def chooseRandomData(dataArray ,n, ite):
    
    random.seed(ite)
    # make list of n unique random index
    nrOfData = len(dataArray)
    randomIndexList = random.sample(range(nrOfData), n)

    # collect data in every dimension for the n random index 
    randomList = []
    for i in randomIndexList:   # for every index

        dataPoint = dataArray[i] # data point at index i in dataList 

        # add data point to randomList
        randomList.append(dataPoint)

    # make numpy array
    randomArray = np.array(randomList, dtype=float)

    return randomArray



###################################################################################################################

# IN: dataArary: numpy array where each element corresponds to a list representing a data point
# OUT: same array but normalized in range (0,1)
#
def normalizeData(dataArray):

    nrOfDimensions = len(dataArray[0])

    for i in range(0, nrOfDimensions):
        
        temp = dataArray[0:,i]
        temp = np.array(temp) - temp.min()
        temp = np.array(temp / temp.max())
        
        dataArray[0:, i] = temp

    return dataArray



###################################################################################################################

# IN: dataArray, numpy array of data points
# OUT: MList: list of integers, each element corresponding to a data point in dataList
# calculating the smallest valid M coefficients (not the most efficient way,but it works)
def getM(dataArray):

    nrOfPoints = len(dataArray)
    
    MList = [0] * nrOfPoints
    
    for i in range(0, nrOfPoints):

        for j in range(0, nrOfPoints):
            
            M = (np.linalg.norm(dataArray[i] - dataArray[j])) ** 2
            
            if M > MList[i]:
                MList[i] = M
    
    return MList


###################################################################################################################

#
#
# solve problem with gurobi
def solveProblem(normArray,ite):
   
    # dimension of data
    dimension = len(normArray[0])  

    # nr of data points
    n = len(normArray) 
   
    # calculate M
    MList = getM(normArray)
    #print('nr of M in list: ' + str(len(MList)))


    # MAKE GUROBI MODEL
    model = gp.Model()


    # ADD VARIABLES
    # store centroids coordinates in dictionary 
    centroids = {}

    for category in range(clusters):
        centroids[category] = {}
        for dim in range(dimension):
            centroids[category][dim] = model.addVar(0, 1, name='c_' + str(category) + '_p' + str(dim))


    # store binary variables of every data point in dictionary
    b = {}
    for data in range(n):
        b[data] = {}
        for category in range(clusters):
            b[data][category] = model.addVar(0, 1, vtype=gp.GRB.BINARY, name='b_' + str(category) + '_d' + str(data))


    # store distances between cluster center and data points in dictionary
    r = {}
    for data in range(n):
        r[data] = model.addVar(0, MList[data], name='r_' + str(data))


    # UPDATE MODEL to include variables
    model.update()


    # ADD CONSTRAINTS
    for data in range(n):

        # every data point must be assigned to one center
        # sum of binary variables must be equal to one
        model.addConstr(sum(b[data][category] for category in range(clusters)) == 1)


        # Quadratic constraints for the distances (big M)
        for category in range(clusters):
            model.addQConstr(sum(
            (normArray[data][dim] - centroids[category][dim]) * (normArray[data][dim] - centroids[category][dim]) for dim in
            range(dimension)) <= r[data] + MList[data] * (1 - b[data][category]))


    
    # ADD SYMMETRY BREAKING CONSTRAINT
    # The following constraints removes some symmetries, by imposing an ordering of the centroids along the first axis
    # The constraints are of the type: the first coordinate of the first center must be smaller than that of the second
    # second center and so on. Without these constraints we can create two different equally good solutions by switching
    # the location of two centroids. 
    for category in range(clusters - 1):
        model.addConstr(centroids[category][0] <= centroids[category + 1][0])


   # DEFINE OBJECTIVE FUNCTION
    model.setObjective(sum(r[data] for data in range(n)))

    # SET TIME LIMIT
    model.setParam('TimeLimit', 900) # you don't want to wait much longer! Consider test that are faster
    
    # UPDATE MODEL
    model.update()

    # SOLVE
    model.optimize()

    nodesVector[ite] = model.nodecount  #saves how many nodes it explored in the current iteration.
    runtimeVector[ite] = model.Runtime  #saves how long time it took to solve the problem this iteration

    #########################################################################################
    print(' ')
    print('-------------------------------------------------')
    print('some interesting data')
    print('Number of branch and bound nodes explored: ' + str(model.nodecount))


    print(' ')
    print('-------------------------------------------------')
    # the centroids are stored in centroids[category][dim]
    # example how you can access the coordinates of the centroids#

    # coordinates of centroids
    # saves centroid coordinates of each cluster as lists in a big list: [ [coord. cent. 1] , [coord. cent. 2] , ... ]
    centroidCoordinates = []
    for center in range(clusters):  # for every cluster

        coordinate = []

        for dim in range(dimension): # get coordinate of every dimension
            
            coordinate.append(centroids[center][dim].X) 

        centroidCoordinates.append(coordinate)

    # print coordinates of centroids
    for i, centroid in enumerate(centroidCoordinates):
        print('centroid ' + str(i+1) + ': ')
        print(centroid)


    
    # what cluster each data point belongs to
    belongsToCluster = []   
    for data in range(n):   # check all data points
        
        added = False

        for category in range(clusters):    # check all clusters
            
            if b[data][category].X == 1:      # if the binary variable is 1, it belongs to cluster

                belongsToCluster.append(category)
                
                added = True    # help variable

            else:   # if binary variable is 0, check if it belongs to next cluster
                pass

        
        # uses help varible to see if data belonged to any cluster
        if not added:   # if datapoint does not belong to any cluster, set it to None
            belongsToCluster.append(None)



    # plot 2D clusters
    if dimension == 2:
        plot2D(normArray, belongsToCluster, centroidCoordinates,ite)



###################################################################################################################  

# IN: normArray: numpy array of data points
#     clusterList: list of what cluster each data point belongs to
#     centroidCoordinates: list of coordinates of all centroids
# saves a scatter plot as a png of the data. Plot shows which cluster each data point belongs to
def plot2D(normArray, clusterList, centroidCoordinates,ite):


    # add more colors if there are more than 9 clusters
    # color of centroid point
    centroidColors = ['dodgerblue', 'crimson' , 'purple', 'darkgreen', 'darkorange', 'hotpink', 'black', 'teal', 'olive']

    # color of data points in clusters corresponding to color of centroid
    dataColors = ['lightskyblue', 'palevioletred', 'm', 'forestgreen', 'orange', 'pink', 'dimgrey', 'c', 'y']


    plt.figure(1)   # The (1) gets all of the subplots to the same figure
    # E.g. iterations = 8 -> rootOfIterations = 3. Calculates rootOfIterations so all the subplots have the same height as length.
    rootOfIterations = math.ceil(np.sqrt(iterations))   
    plt.subplot(rootOfIterations ,rootOfIterations,ite+1)   #Makes a subplot

    for j in range(len(normArray)):

        c = dataColors[clusterList[j]]
        x = normArray[j][0]
        y = normArray[j][1]

        plt.scatter(x, y, color = c)



    for i in range(len(centroidCoordinates)):

        c = centroidColors[i]
        x = centroidCoordinates[i][0]
        y = centroidCoordinates[i][1]

        plt.scatter(x,y, color = c)


    plt.title('iteration' + str(ite))
    plt.xlabel('x_1')
    plt.ylabel('x_2')
    
    #Makes a line inbetween each cluster centroid. Does not look good :(
    '''
    for firstCluster in range(len(centroidCoordinates)):
        for secondCluster in range(firstCluster+1, len(centroidCoordinates)):
            nX = centroidCoordinates[secondCluster][0] - centroidCoordinates[firstCluster][0] #Normalvektorn till hyperplanets x-koordinat.
            nY = centroidCoordinates[secondCluster][1] - centroidCoordinates[firstCluster][1] #Normalvektorn till hyperplanets y-koordinat.

            punktPaHyperplanX = (centroidCoordinates[firstCluster][0] + centroidCoordinates[secondCluster][0]) /2
            pphX = punktPaHyperplanX    #Punkten mittemmellan clustercentrenas x-koordinat
            punktPaHyperplanY = (centroidCoordinates[firstCluster][1] + centroidCoordinates[secondCluster][1]) /2
            pphY = punktPaHyperplanY    ##Punkten mittemmellan clustercentrenas y-koordinat

            k = -nX /nY
            m = (nX*pphX + nY*pphY) / nY

            if m <=1 and m >= 0:
                hyperplaneX = np.linspace(-0.1,1.1)
                hyperplaneY = k*hyperplaneX + m
            else:
                hyperplaneY = np.linspace(-0.1,1.1)
                hyperplaneX = (hyperplaneY-m)/k
            
            plt.plot(hyperplaneX,  hyperplaneY, color = 'k', linewidth = 1)

    plt.xlim(-0.1,1.1)  #Only needed if you have the line inbetween each cluster centroid
    plt.ylim(-0.1,1.1)  #Only needed if you have the line inbetween each cluster centroid
    '''

  


   

###################################################################################################################
###################################################################################################################

def main():

    # PARAMETERS
    global clusters         # nr of clusters
    global iterations       # nr of iterations the program will do
    global nodesVector      # a list where you put how many branch and bound nodes you explored.
    global runtimeVector    #list where the runtime of each iteration is stored

    # MAKE ARRAY of data in txt document
    dataArray = readFile(D2C2File)

    # CHOOSE n RANDOM DATA POINTS
    n = 50      # nr of data point we want to look at

    for ite in range(iterations):
        print('We are on iteration: ' + str(ite))
        randomArray = chooseRandomData(dataArray, n, ite)
        print('length of data: ' + str(len(randomArray)))
        

        # NORMALIZE DATA
        normArray = normalizeData(randomArray)
        dimension = len(normArray[0])   # dimension of data
        
        # OPTIMIZE NORMALIZED DATA WITH GUROBI
        solveProblem(normArray,ite)
    
    print(nodesVector)
    print(runtimeVector)
    plt.show()
    plt.savefig('testplot.png')
    
    





main()









