import numpy as np
import gurobipy as gp 
import random
import matplotlib.pyplot as plt
import math
import os


###################################################################################################################
###################################################################################################################
# TEXT DOCUMENTS WITH DATA
D128C2File = 'g2-128-10.txt'    # 128-dimenisional data with 2 clusters
D64C2File = 'g2-64-10.txt'      # 64-dimenisional data with 2 clusters
D32C2File = 'g2-32-10.txt'      # 32-dimenisional data with 2 clusters
D16C2File = 'g2-16-10'          # 16-dimenisional data with 2 clusters
D8C2File = 'g2-8-10.txt'        # 8-dimenisional data with 2 clusters
D4C2File = 'g2-4-10.txt'        # 4-dimenisional data with 2 clusters

D2C9File = 'D2.txt'             # 2-dimenisional data with 9 clusters
D2C2File = 'g2-2-10.txt'        # 2-dimenisional data with 2 clusters

# data files created from makeData.py
# ....


# PARAMETERS
dimVec = [2, 4, 8, 16, 32, 64, 128]
clusterVec = [2, 3, 4, 5, 6, 7, 8, 9]
iterations = 5  # nr of iterations the program will do



# PLOTTING COLORS
# add more colors if there are more than 9 clusters
# color of centroid point
centroidColors = ['dodgerblue', 'crimson' , 'purple', 'darkgreen', 'darkorange', 'hotpink', 'black', 'teal', 'olive']

# color of data points in clusters corresponding to color of centroid
dataColors = ['lightskyblue', 'palevioletred', 'm', 'forestgreen', 'orange', 'pink', 'dimgrey', 'c', 'y']


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
                dataPoint.append(float(data)) 
            
            dataList.append(dataPoint)   # adds every dataPoint list to list
            
        dataArray = np.array(dataList, dtype=float)

    return dataArray



###################################################################################################################

# IN: dataArray: numpy array where each element corresponds to a list representing a data point
#     n: int, how many random data points we want
# OUT: randomArray: numpy array of shorter version of dataArray
# picks n random data points from dataList and returns them in a numpy array
def chooseRandomData(dataArray ,n):
    
    # random.seed(6)
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
def solveProblem(dataArray, dimension, clusters, n, ite):
   
   
    # calculate M
    MList = getM(dataArray)


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
        # sum of binary variables must be eaqual to one
        model.addConstr(sum(b[data][category] for category in range(clusters)) == 1)


        # Quadratic constraints for the distances (big M)
        for category in range(clusters):
            model.addQConstr(sum(
            (dataArray[data][dim] - centroids[category][dim]) * (dataArray[data][dim] - centroids[category][dim]) for dim in
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
    model.setParam('TimeLimit', 1800) # you don't want to wait much longer! Consider test that are faster
    
    # UPDATE MODEL
    model.update()

    # SOLVE
    model.optimize()


    #########################################################################################


    # RESULTS

    # get node count and run time
    nodeCount = model.nodecount
    runTime = model.runtime

    # print(' ')
    # print('-------------------------------------------------')
    # print('some interesting data')
    # print('Number of branch and bound nodes explored: ' + str(nodeCount))
    # print('time to solve problem: ' + str(runTime))
    # print(' ')
    # print('-------------------------------------------------')

   
    # coordinates of centroids
    # saves centroid coordinates of each cluster as lists in a big list: [ [coord. cent. 1] , [coord. cent. 2] , ... ]
    centroidCoordinates = []
    for center in range(clusters):  # for every cluster

        coordinate = []
        for dim in range(dimension): # get coordinate of every dimension
            
            coordinate.append(centroids[center][dim].X) 

        centroidCoordinates.append(coordinate)

    # print coordinates of centroids
    # for i, centroid in enumerate(centroidCoordinates):
    #     print('centroid ' + str(i+1) + ': ')
    #     print(centroid)

    
    
    # which cluster each data point belongs to
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
        plot2D(dataArray, belongsToCluster, centroidCoordinates, ite)


    return nodeCount, runTime



###################################################################################################################  

# IN: normArray: numpy array of data points
#     clusterList: list of what cluster each data point belongs to
#     centroidCoordinates: list of coordinates of all centroids
# saves a scatter plot as a png of the data. Plot shows which cluster each data point belongs to
def plot2D(dataArray, clusterList, centroidCoordinates, ite):

    # add more colors if there are more than 9 clusters
    # color of centroid point
    centroidColors = ['dodgerblue', 'crimson' , 'purple', 'darkgreen', 'darkorange', 'hotpink', 'dimgrey', 'teal', 'olive']

    # color of data points in clusters corresponding to color of centroid
    dataColors = ['lightskyblue', 'palevioletred', 'm', 'forestgreen', 'orange', 'pink', 'lightgrey', 'c', 'y']

    n = len(dataArray)  # nr of data points
    k = len(centroidCoordinates)


    plt.figure(1)
    plt.suptitle('k-means clustering: ' + str(k) + ' clusters, ' + str(n) + ' data points')
    
    rootOfIterations = math.ceil(np.sqrt(iterations))   
    plt.subplot(rootOfIterations ,rootOfIterations,ite+1)
    
    # plot data points
    for j in range(n):

        if clusterList[j] is None:
            c = 'black'
        else: 
            c = dataColors[clusterList[j]]      # colour corresponding to which cluster it belongs to
        
        x = dataArray[j][0]                 # x-coordinate
        y = dataArray[j][1]                 # y-coordinate

        plt.scatter(x, y, color = c, s = 1)
        

    # plot cluster centroids
    for i in range(k):

        c = centroidColors[i]           # colour
        x = centroidCoordinates[i][0]   # x-coordinate
        y = centroidCoordinates[i][1]   # y- coordinate

        plt.scatter(x,y, color = c, s = 10, marker='*')
        

    plt.tight_layout()
    plt.title('iteration: ' + str(ite+1))
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    

    

###################################################################################################################

#
#
#
def dataPointTest(normArray, nVec, clusters, dimension):

        # DATA WE WANT TO SAVE FROM SOLVER
    nodeVec = []    # nr of nodes explored
    timeVec = []    # solver run time

    for n in nVec:  # for every n in nVec 

        # temporary vectors to save results from one iteration
        tempNodeVec = []
        tempTimeVec = []
        
        for ite in range(0,iterations):    # test every sample size 5 times

            # choose n random data from normilized data array
            randomArray = chooseRandomData(normArray, n)  

            # gurobi solver  
            nodeCount, runTime = solveProblem(randomArray, dimension, clusters, n, ite)

            # add expl. nodes and runtime of iteration i
            tempNodeVec.append(nodeCount)
            tempTimeVec.append(runTime)

        # add temporary vectors to big vector where all results are saved
        nodeVec.append(tempNodeVec)
        timeVec.append(tempTimeVec)

        # show/save 2D cluster plots
        #plt.show()
        figPath = '/Users/Hanna/Documents/KEX/plottar'
        figName = 'test1_' + str(clusters) + 'C_' + str(n) + 'D.pdf'
        #plt.savefig(figName)
        plt.savefig(os.path.join(figPath, figName))


    print('________________________________________________________________________-')
    print('nr of data points')
    print(nVec)
    print(' ')
    print('nodes explored')
    print(nodeVec)
    print(' ')
    print('solver run time')
    print(timeVec)



###################################################################################################################
###################################################################################################################

def main():

    # PARAMETERS
    global centroidColors
    global dataColors
    global iterations
    global clusterVec
    global dimVec
    
    # TEST 1: NR OF DATA POINTS
    
    # make array of data in txt document
    dataArray1 = readFile(D2C2File)

    # dimension and nr of clusters of data
    cluster1 = clusterVec[0]    # nr of clusters of data chosen above
    dimension1 = dimVec[0]   # dimension of data

    # normalize data in array
    normArray1 = normalizeData(dataArray1)

    nVec = [25, 50, 100, 200, 400, 800]
    dataPointTest(normArray1, nVec, cluster1, dimension1)

    
    
    

main()









