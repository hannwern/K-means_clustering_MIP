import numpy
import matplotlib.pyplot as plt
import math



# RESULTS NR OF DATA POINTS

#
#
#
def test1():

    nVec = [10, 30, 50]
    nodesExpl = [[39.0, 40.0, 61.0, 35.0, 35.0], [76.0, 84.0, 67.0, 61.0, 68.0], [763.0, 212.0, 1.0, 193.0, 114.0]]
    solTime = [[0.35259246826171875, 0.14630126953125, 0.12816810607910156, 0.07232666015625, 0.08226585388183594], [0.3099403381347656, 0.10167312622070312, 0.17832183837890625, 0.19997215270996094, 0.16625595092773438], [0.6478767395019531, 0.4001197814941406, 0.3057212829589844, 0.40549659729003906, 0.24067115783691406]]

    plt.figure()
    for i in range(len(nVec)):

        for j in range(len(nodesExpl[i])):

            n = nVec[i]

            nodes = nodesExpl[i][j]

            plt.scatter(n, nodes, s = 10, c = 'black')

    plt.title('Explored nodes')
    plt.xlabel('nr of data points')
    plt.ylabel('nr of nodes')
    plt.show()


    plt.figure()
    for i in range(len(nVec)):

        for j in range(len( solTime[i])):

            plt.scatter(nVec[i], solTime[i][j], s = 10, c = 'black')

    plt.title('Solver run time')
    plt.xlabel('nr of data points')
    plt.ylabel('time [s]')
    plt.show()

############################################################################################

#
#
#
def test2():

    dimVec = [2, 4, 8, 16, 32, 64, 128]

    nodesExpl = [ [...] , [...] , [...] , [...] , [...] , [...] , [...] ]
    solTime = [ [...] , [...] , [...] , [...] , [...] , [...] , [...] ]


    plt.figure()
    for i in range(len(dimVec)):

        for j in range(len(nodesExpl[i])):

            dim = dimVec[i]

            nodes = nodesExpl[i][j]

            plt.scatter(dim, nodes, s = 10, c = 'black')

    plt.title('Explored nodes')
    plt.xlabel('dimension of data')
    plt.ylabel('nr of nodes')
    plt.show()


    plt.figure()
    for i in range(len(dimVec)):

        for j in range(len( solTime[i])):

            plt.scatter(dimVec[i], solTime[i][j], s = 10, c = 'black')

    plt.title('Solver run time')
    plt.xlabel('dimension of data')
    plt.ylabel('time [s]')
    plt.show()



############################################################################################

#
#
#
def test3():

    clusterVec = [2, 3, 4, 5, 6, 7, 8, 9]

    nodesExpl = [ [...] , [...] , [...] , [...] , [...] , [...] , [...] ]
    solTime = [ [...] , [...] , [...] , [...] , [...] , [...] , [...] ]


    plt.figure()
    for i in range(len(clusterVec)):

        for j in range(len(nodesExpl[i])):

            dim = clusterVec[i]

            nodes = nodesExpl[i][j]

            plt.scatter(dim, nodes, s = 10, c = 'black')

    plt.title('Explored nodes')
    plt.xlabel('nr of clusters')
    plt.ylabel('nr of nodes')
    plt.show()


    plt.figure()
    for i in range(len(clusterVec)):

        for j in range(len( solTime[i])):

            plt.scatter(clusterVec[i], solTime[i][j], s = 10, c = 'black')

    plt.title('Solver run time')
    plt.xlabel('nr of clusters')
    plt.ylabel('time [s]')
    plt.show()




