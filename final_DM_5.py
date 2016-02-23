
 
import math
import time
kUsers=30
    
def main():
    print("inside main")
    
def extractTrainData(file_name):
    print("extracting base file",file_name)
    userMovieRatingDict ={}
    #file = open("ml-100k//u1.base", "r+")
    file = open(file_name, 'r')
    print ("Filepath is:" + file.name)
    for everyLine in file:
        if not everyLine.strip() =='':
            user,movie,rating,time=everyLine.strip().split("\t")
            userMovieRatingDict[int(user),int(movie)]=int(rating)
            
    print("done")        
    return userMovieRatingDict

def extractTestData(file_name):
    print("extracting u1test",file_name)
    userMovieRatingTestDict ={}
    #file = open("ml-100k//u1.test", "r+")
    file = open(file_name, 'r')
    print ("Filepath is:" + file.name)
    for everyLine in file:
        if not everyLine.strip() =='':
            user,movie,rating,time=everyLine.strip().split("\t")
            userMovieRatingTestDict[int(user),int(movie)]=int(rating)
            
    print("done")        
    return userMovieRatingTestDict

def prediction(userMovieTestRatings,similarUsers,userMovieRatings):
    print("enter prediction")
    madValue=0.0
    unseenElse=0
    for line in userMovieTestRatings:
        rating=0.0
        user=line[0]
        movie=line[1]-1
        #print(user)
        #print(movie)
        #print(similarUsers[user])
        similarWithUsersInTest=similarUsers[user]
        unseen=notSeenCounter(movie,similarWithUsersInTest, userMovieRatings)
        if not unseen == kUsers:
            #print("if count zero")
            for user in similarWithUsersInTest:
                if (user+1,movie) in userMovieRatings:
                    rating=rating+userMovieRatings[(user+1,movie)]
                else:
                    unseenElse+=1        
                    continue
                
            rating=round(rating/(kUsers-unseen))
            
        else:
            #print("else")
            rating = round(avgerageRating(movie, userMovieRatings))
        print("actual rating",rating)    
        print("testValue",userMovieTestRatings[line])
        madValue=madValue+abs(rating-userMovieTestRatings[line])
    print("madValue",madValue)
    print("(len(userMovieTestRatings))",(len(userMovieTestRatings)))
    testLength=len(userMovieTestRatings)
    madValue=madValue/testLength
    
    print("MAD value is",madValue)
                
    return madValue



def notSeenCounter(movie,similarUsers,userMovieRatings):
    notSeenCount = 0
    for user in similarUsers:
        if not (user+1, movie) in userMovieRatings or  userMovieRatings[(user+1, movie)] == 0:  
            notSeenCount = notSeenCount + 1
            #print("notSeen value is",notSeen)
    return notSeenCount


def avgerageRating(movie,userMovieRatings):
    rating = 0
    ratedcount = 0
    for each in userMovieRatings:
        #print("here1")
        if userMovieRatings[each] !=0:
            if each[1] == movie:
            #print("here2")
                ratedcount = ratedcount + 1
                rating = rating + userMovieRatings[each]
        else:
            ratedcount = 0        
    if not ratedcount == 0:
                #print("count =0,total" is total)
        #print("count=0,count" is count)    
        return rating/ratedcount        
    else:
        #print("total" is total)
        #print("count" is count)
        return 0


   

def lmaxDistance(user1,user2):
    lmaxDist = max([abs(a-b) for a, b in zip(user1,user2)])
    lmaxDist = 1/(1+round(lmaxDist))
    print(lmaxDist)
    return lmaxDist

def euclideanDistance(user1, user2):
    euclideanDist = [(a-b)**2 for a, b in zip(user1, user2)]
    euclideanDist = math.sqrt(sum(euclideanDist))
    euclideanDist = 1/(1+round(euclideanDist))
    print(euclideanDist)
    return(euclideanDist)

def manhattanDistance(user1, user2):
    manhattanDist = [abs(a-b) for a, b in zip(user1, user2)]
    manhattanDist = round(sum(manhattanDist), 2)
    manhattanDist =1/(1+round(manhattanDist))
    #print(manhattanDist)
    return manhattanDist


def calculateDistance(userMovieMatrix,userCount):
    userMatrix=[[0 for i in range(userCount)]for j in range(userCount)]
    print("user matrix length is" ,len(userMatrix))
    topSimilar={}
    for row in userMovieMatrix:
        #print("user1 value is",userMovieMatrix.index(row))
        #comparisionRow=userMovieMatrix.index(row)+1
        comparisionRow=0
        #print(len(userMovieMatrix))
        while comparisionRow<len(userMovieMatrix):
            #print("user2 value is",comparisionRow)
            #print(userMovieMatrix[comparisionRow])
            #print("cell value is",j)
            distance=euclideanDistance(row, userMovieMatrix[comparisionRow])
            userMatrix[userMovieMatrix.index(row)][comparisionRow]=distance
            #for i in userMatrix:
            
            #print("row,column value is",userMovieMatrix.index(row),comparisionRow)
            comparisionRow=comparisionRow+1
    for row in userMatrix:
        temp=sorted(range(len(userMatrix[userMatrix.index(row)])), key=lambda i: userMatrix[userMatrix.index(row)][i])[:kUsers]
        #temp=sorted(range(len(userMatrix[userMatrix.index(row)])), key=lambda i: userMatrix[userMatrix.index(row)][i])[:40]
        user,similarUserslist=userMatrix.index(row)+1,temp
        topSimilar[int(user)]=similarUserslist
            #print("topSimilar",topSimilar)
            
              
            
        #topSimilar[userMovieMatrix.index(row)+1]=sorted(range(len(row)), key=lambda i: row[i], reverse=True)[:20]    
        #print("topSimilar",topSimilar)    
        #print("random")
    #print(userMatrix[0])
    return topSimilar
    #calculateTopSimilar(userMatrix,topSimilar)
 

def calculateTopSimilar(userMatrix,topSimilar):
        print("topSimilar",topSimilar)
    
    
def matrixUpdate(userMovieRatings,userMovieMatrix):
    for userMovieRating in userMovieRatings:
        if userMovieMatrix[userMovieRating[0]-1][userMovieRating[1]-1] ==0:
            # -1 to adjust the index for matrix,0 for movie and user does not exist
            userMovieMatrix[userMovieRating[0]-1][userMovieRating[1]-1] = userMovieRatings[userMovieRating]
        
    return userMovieMatrix

if __name__ == "__main__":main() ## with if
start_time = time.time()
userMovieTestRatings = {}
userMovieRatings = {}
userMovieRatingInfo={}



for trainFiles in range(1, 2):
    userMovieRatings.update(extractTrainData("ml-100k/u" + str(trainFiles) + ".base"))


for testFiles in range(1, 2):
    userMovieTestRatings.update(extractTestData("ml-100k/u" + str(testFiles) + ".test"))

#userMovieRatings=extractData()
#testData=extractTestData()
#print(userMovieRatings)
# userMovieRatingInfo=extractuserMovieOnly()
# print(userMovieRatingInfo)

# intialise the userMovie matrix
#count taken from u.info file

userCount=943
moviesCount=1682
userMovieMatrix=[[0 for i in range(moviesCount)]for j in range(userCount)]

userMovieMatrix=matrixUpdate(userMovieRatings,userMovieMatrix)
print("matrix done")
#print(userMovieMatrix)
#print(len(userMovieMatrix))
#print(len(userMovieMatrix[0]))
#print(userMovieMatrix[0])

similarUsers=calculateDistance(userMovieMatrix,userCount)
#print(similar)
final=prediction(userMovieTestRatings,similarUsers,userMovieRatings)
print("final is",final)
#unseenMovies(userMovieRatings,similar)
#unseenMovies(userMovieMatrix,moviesCount)
print("--- %s seconds ---" % (time.time() - start_time))








