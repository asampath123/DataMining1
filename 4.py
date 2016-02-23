import numpy
import math
from scipy.spatial.distance import pdist
import random
import time

#has the values of r(k) and k
rkGraph=[]
kGraph =[]

#converts the list to numpy array(computation is faster), calculate maximum and minimum. And apply the forumla 
def conversionNdOperations(list,k,n):
    
    list=numpy.array(list)
    afterDistance= pdist(list,'Euclidean')
        
    dminimumDistance=numpy.min(afterDistance[numpy.nonzero(afterDistance)])
    dmaximumDistance=numpy.max(afterDistance)
    return math.log((dmaximumDistance-dminimumDistance)/dminimumDistance,10)
    
    
def main():
    start_time = time.time()
    temp=[]
    #change the value of dimension for different value of n=100,1000,10000
    dimension=100
    print("inside main")
    #k varies from 0-100
    for k_val in range(0,100):
        rkList =[]
        for n_val in range(0,dimension):
            #fill with random values
            temp=(list([random.uniform(0,1) for each in range(k_val+1)]))
            rkList.append(temp)
        #get r(k)
        list1=conversionNdOperations(rkList,k_val,n_val)
        
        rkGraph.append(list1)
        kGraph.append(k_val+1)
    #print(rkGraph)
    #write output to a csv file. 
    f = open('output100.csv', 'w')
    for item in rkGraph:
        f.write("%s\n" % item)
    f.close()    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":main()



