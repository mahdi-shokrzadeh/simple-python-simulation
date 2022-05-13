import random
from matplotlib.cbook import ls_mapper
import matplotlib.pyplot as plt

#inputs :

#number of days
d = 100
#number of hours per day
h = 24
# lenght of table
m = 20 
# width of table
n = 20
# number of people (by default [p/2] will be self-giving people and [p/2] will be selfish people)
p = 100

l = [] 
l_k = []
l_f = []


people = []
for i in range(int(p/2)) :
    # [ "" => state , "" => position , "" => used resources]
    people.append(["selfish" , 0 , 0 ])
    people.append(["self-giving" , 0  , 0])

# resources 
r = 300

# m : i
for i in range(m) :
    # n : j
    # l : [ "" => number of available resources , "" => number of people ]
    l.append([[ 0 , 0 ] for j in range(n)])
    

for i in range(1 , d+1):

    # randomly put resources in squares 

    for j in range(r):

        g = True

        while g :
            x = random.randint(0 , m-1)
            y = random.randint(0 , n-1)

            if l[x][y][0] < 2 :
                l[x][y][0] += 1 
                g = False


    # randomly put people in squares

    for j in range(p) :

        g = True

        while g :
            x = random.randint(0 , m-1)
            y = random.randint(0 , n-1)
            if l[x][y][1] < 1 :
                l[x][y][1] += 1
                
                people[j][1] = [x , y]
                g = False


    # process of moving per hour 

    for j in range(h) :

        # moving


        for k in range(p) :
            
            if l[ people[k][1][0] ][ people[k][1][1] ][0] == 0 :
               
                # person should move 

                if people[k][1][0] + 1 < m  :
                    if l[people[k][1][0] + 1][people[k][1][1]][1] < 2 :
                        l[people[k][1][0] + 1][people[k][1][1]][1] += 1
                        people[k][1][0] += 1
                        

                elif people[k][1][1] + 1 < n :
                    if l[people[k][1][0]][people[k][1][1] + 1][1] < 2 :
                        l[people[k][1][0]][people[k][1][1] + 1][1] += 1
                        people[k][1][1] += 1
                       

                elif people[k][1][0] - 1 >= 0  :
                    if l[people[k][1][0] - 1][people[k][1][1]][1] < 2 :
                        l[people[k][1][0] - 1][people[k][1][1]][1] += 1
                        people[k][1][0] -= 1
                        


                elif people[k][1][1] - 1 >= 0 :
                    if l[people[k][1][0]][people[k][1][1] -1][1] < 2 :
                        l[people[k][1][0]][people[k][1][1] -1][1] += 1
                        people[k][1][1] -= 1
                

        # process confilcts 
        
        for k in range(m) :
            for q in range(n) :

                index_of_people = []

                for indx , w in enumerate(people) :
                    
                    if w[1][0] == k and w[1][1] == q :
                        index_of_people.append(indx)

                

                # rules 
                if len(index_of_people) == 1 :
                    people[index_of_people[0]][2] += l[k][q][0]
                    l[k][q][0] = 0
                    
                    


                elif len(index_of_people) == 2 :
                    
                    # different cases :
                    if people[index_of_people[0]][0] == "selfish" and people[index_of_people[1]][0] == "selfish" :

                        if l[k][q][0] != 0 :
                            people[index_of_people[0]][2] += l[k][q][0] / 2
                            people[index_of_people[1]][2] += l[k][q][0] / 2
                            l[k][q][0] = 0

                    elif people[index_of_people[0]][0] == "selfish" and people[index_of_people[1]][0] == "self-giving" :
                        if l[k][q][0] != 0 :

                            if l[k][q][0] == 1 :

                                people[index_of_people[0]][2] += 1
                                l[k][q][0] = 0 

                            else :
                                people[index_of_people[0]][2] += 3/2
                                people[index_of_people[1]][2] += 1/2
                                l[k][q][0] = 0

                    elif people[index_of_people[0]][0] == "self-giving" and people[index_of_people[1]][0] == "self-giving" :

                        if l[k][q][0] != 0 :
                            people[index_of_people[0]][2] += l[k][q][0] / 2
                            people[index_of_people[1]][2] += l[k][q][0] / 2
                            l[k][q][0] = 0


                    elif people[index_of_people[0]][0] == "self-giving" and people[index_of_people[1]][0] == "selfish" :
                        if l[k][q][0] != 0 :

                            if l[k][q][0] == 1 :

                                people[index_of_people[1]][2] += 1 
                                l[k][q][0] = 0

                            else :
                                people[index_of_people[1]][2] += 3/2
                                people[index_of_people[0]][2] += 1/2
                                l[k][q][0] = 0
                



    # process statistics for each person 

    for indx , j in enumerate(people) :

        j[1] = []

        x = random.randint(0 , 1)
        if j[2] == 0 :
            
            del(people[indx])

            p -= 1

        elif j[2] == 1/2 :

            if x == 1 :
                people[indx][2] = 0
                # still alive
                pass

            else :
                
                del(people[indx])
                p -= 1

        elif j[2] == 1 :
            people[indx][2] = 0
            #alive
            pass

        elif j[2] == 3/2 :
            people[indx][2] = 0
            if x == 1 :
                # Reproduction
                people.append([people[indx][0] , [0 , 0] , 0 ])
                p += 1
        
        elif j[2] >= 2 :
            people.append([people[indx][0] , [0 , 0] , 0])
            people[indx][2] = 0
            p += 1

            

    k = 0
    f = 0

    for j in people :
        if j[0] == "selfish" :
            k += 1
        else:
            f += 1
    l_k.append(k)
    l_f.append(f)

    print("day " + str(i) + " is over")
    print("self-giving : " + str(f))
    print("selfish prople : " + str(k))
    print("--------------")
    
    # clear resources from table at the end of day
    
    for j in l :
        for k in j :
            k[0] = 0
            k[1] = 0

plt.plot( [j for j in range(1 , d+1)] , [l_k[i] for i in range(d)] )
plt.ylabel('number of selfish people')
plt.xlabel("days")
plt.show()

plt.plot( [j for j in range(1 , d+1)] , [l_f[i] for i in range(d)] )
plt.ylabel('number of self-giving people')
plt.xlabel("days")
plt.show()