
 
import math
import time
    
def main():
    print("inside main")
    
def extractTrainData(file):
    print("extracting base file",file)
    userMovieRatingDict ={}
    #file = open("ml-100k//u1.base", "r+")
    file = open(file, 'r')
    print ("Filepath is:" + file.name)
    for everyLine in file:
        if not everyLine.strip() =='':
            user,movie,rating,time=everyLine.strip().split("\t")
            userMovieRatingDict[int(user),int(movie)]=int(rating)
            
    print("done")        
    return userMovieRatingDict

def getGender():
    file = open("ml-100k/u.user", "r+")
    dict = {}
    for everyLine in file:
        # user id | age | gender | occupation | zip code
        if everyLine.strip() != '':
            user_id, age, gender, occupation, zip_code = everyLine.strip().split("|")
            dict[int(user_id)] = gender

    return dict


def extractTestData(file):
    print("extracting u1test",file)
    userMovieRatingTestDict ={}
    #file = open("ml-100k//u1.test", "r+")
    file = open(file, 'r')
    print ("Filepath is:" + file.name)
    for everyLine in file:
        if not everyLine.strip() =='':
            user,movie,rating,time=everyLine.strip().split("\t")
            userMovieRatingTestDict[int(user),int(movie)]=int(rating)
            
    print("done")        
    return userMovieRatingTestDict

def prediction(userMovieTestRatings,similarUsers,userMovieRatings,userGender):
    print("enter prediction")
    madValue=0
    unseenElse=0
    for line in userMovieTestRatings:
        rating=0
        user=line[0]
        movie=line[1]-1
        #print(user)
        #print(movie)
        #print(similarUsers[user])
        similarWithUsersInTest=similarUsers[user]
        unseen=notSeenCounter(movie,similarWithUsersInTest, userMovieRatings)
        if not unseen == 30:
            #print("if count zero")
            for user in similarWithUsersInTest:
                if (user+1,movie) in userMovieRatings:
                    if user+1 in userGender[line[0]]:
                        rating=rating+(1.5*(userMovieRatings[(user+1,movie)]))
                    else:
                        rating=(0.5*rating+userMovieRatings[(user+1,movie)])    
                else:
                    unseenElse+=1        
                    continue
                
            rating=rating/(30-unseen)
            
        else:
            #print("else")
            rating = avgerageRating(movie, userMovieRatings)
            
            
        madValue=madValue+abs(rating-userMovieTestRatings[line])
    print("madValue",madValue)
    print("(len(userMovieTestRatings))",(len(userMovieTestRatings)))
    testLength=(len(userMovieTestRatings))
    madValue=((madValue/testLengt)/2)
    
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
    #print(lmaxDist)
    return lmaxDist

def euclideanDistance(user1, user2):
    euclideanDist = [(a-b)**2 for a, b in zip(user1, user2)]
    euclideanDist = math.sqrt(sum(euclideanDist))
    euclideanDist = 1/(1+round(euclideanDist))
    #print(euclideanDist)
    return(euclideanDist)

def manhattan_dist(user1, user2):
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
        temp=sorted(range(len(userMatrix[userMatrix.index(row)])), key=lambda i: userMatrix[userMatrix.index(row)][i])[:30]
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

def getGenderSimilarList(userGender):
    similarGender={}
    temp=[]
    for user1 in userGender:
        genderPrimaryUser=userGender[user1]
        #print(genderPrimaryUser)
        for user2 in userGender:
            genderAnotherUser=userGender[user2]
            if genderPrimaryUser==genderAnotherUser:
                temp.append(user2)
                primaryUser,compareUser=user1,temp
        #print(primaryUser,compareUser)        
        similarGender[int(primaryUser)]= compareUser
    return similarGender


if __name__ == "__main__":main() ## with if
start_time = time.time()
userMovieTestRatings = {}
userMovieRatings = {}
userMovieRatingInfo={}
userGender={}



for trainFiles in range(1, 2):
    userMovieRatings.update(extractTrainData("ml-100k/u" + str(trainFiles) + ".base"))


for testFiles in range(1, 2):
    userMovieTestRatings.update(extractTestData("ml-100k/u" + str(testFiles) + ".test"))

userGender=getGender()
print(userGender)
userGender=getGenderSimilarList(userGender)
#print(userGender)
#userMovieRatings=extractData()
#testData=extractTestData()
#print(userMovieRatings)
# userMovieRatingInfo=extractuserMovieOnly()
# print(userMovieRatingInfo)

# intialise the userMovie matrix
#count taken from u.info file


#matrix update code
userCount=943
moviesCount=1682
userMovieMatrix=[[0 for i in range(moviesCount)]for j in range(userCount)]
for userMovieRating in userMovieRatings:
        if userMovieMatrix[userMovieRating[0]-1][userMovieRating[1]-1] ==0:
            # -1 to adjust the index for matrix,0 for movie and user does not exist
            userMovieMatrix[userMovieRating[0]-1][userMovieRating[1]-1] = userMovieRatings[userMovieRating]


#userMovieMatrix=matrixUpdate(userMovieRatings,userMovieMatrix)
print("matrix done")
#matrix insertion done



#print(userMovieMatrix)
#print(len(userMovieMatrix))
#print(len(userMovieMatrix[0]))
#print(userMovieMatrix[0])

similarUsers=calculateDistance(userMovieMatrix,userCount)
#print(similar)
final=prediction(userMovieTestRatings,similarUsers,userMovieRatings,userGender)
#print("final is",final)
#unseenMovies(userMovieRatings,similar)
#unseenMovies(userMovieMatrix,moviesCount)
print("--- %s seconds ---" % (time.time() - start_time))








