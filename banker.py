import numpy as np
import sys
import pandas as pd

def takeInput():
    """Function that takes the user inputs and does formatting on it."""
    avail = []
    max = []
    alloc = []
    processes = []
    letters = ["A", "B", "C", "D", "E", "F", "G", "H",
               "I", "J", "K", "L", "M", "N", "O", "P"
               , "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
    P = int(input("Please enter the number of processes: "))
    R = int(input("Please enter the number of resources available: "))
    
    for p in range(P):
        processes.append(p)
    
    print("Now let's enter the resources allocation matrix row by row where there is a single space between each element...")
    for i in range(P):
        x = input("Please enter row "+ str(i)+ " of the allocation matrix: ")
        x = [int(element) for element in x.split(" ")]
        for i in x:
           alloc.append(i)
           
    print("\n Now let's enter the max matrix row by row where there is a single space between each element...")
    for i in range(P):
        x = input("Please enter row "+ str(i)+ " of the maximum matrix: ")
        x = [int(element) for element in x.split(" ")]
        for i in x:
            max.append(i)
            
    x = input("Please enter the available instances of resources: ")
    x = [int(element) for element in x.split(" ")]
    for i in x:
        avail.append(i)
            
    max = np.array_split(max, P)
    alloc = np.array_split(alloc, P)
    
    enquiry = int(input("Type 1 if you want to know if system is in safe state or not.\n and type 2 to ask if request can be granted with safe state..."))

    need = needMatrix(R,P, max, alloc)
    p = []
    r = []
    for i in range(P):
        p.append("P"+str(i))
        

    table = pd.DataFrame(need, index = p, columns = letters[0:R])
    print("\nFirst, the need matrix is ")
    print(table)

    
    # Check system is in safe state or not 
    if enquiry ==1:
        flag, l1 = isSafe(R,P,processes,avail,max,alloc)
        if flag ==1:
            print("\nYes, Safe State <", *l1, ">")
            
        else:
            print("No, the system is not in safe state!")
            
    elif enquiry==2:
        request = []
        process = int(input("Please enter the requesting process: "))
        x = input("Please enter resources to allocate as a vector with a single space between each element: ")
        x = [int(element) for element in x.split(" ")]
        for i in x:
            request.append(i)
            
        requestGrant(R,P,process,request, processes,avail,max,alloc)
        
        
        
  
def needMatrix(R,P, Max, alloc):
    """Calculates the need matrix."""
    need = []
    
    for i in range(P):
        l1 = []
        for j in range(R):
            l1.append(0)
        need.append(l1)

    for i in range(P):
        for j in range(R):
            need[i][j] = Max[i][j] - alloc[i][j]
    return need

def isSafe(R,P,processes, avail, max, alloc):
    """Checks whether the system is in safe state or not."""
    need = needMatrix(R,P,max, alloc)
    finish = [0] * P
    seq = [0] * P 
    work = [0] * R 
    count = 0
    l1 = []
    
    for i in range(R):
        work[i] = avail[i] 
        
    while (count < P):

        found = False
        for i in range(P): 
            if (finish[i] == 0): 
                for j in range(R):
                    if (need[i][j] > work[j]):
                        break
                      
                if (j == R - 1): 
                    for r in range(R): 
                        work[r] += alloc[i][r] 
  
                    seq[count] = i
                    count += 1
                    finish[i] = 1
                    found = True

        if (found == False):
            return 0, l1
          
    for i in seq:
        l1.append("P" + str(i))

  
    return 1, l1

def requestGrant(R,P,process,request, processes,avail,max,alloc):
    """Checks whether granting a request will violate the safe state or not."""
    need = needMatrix(R,P,max, alloc)

    for i in range(R):
        x=i
        if request[i] <= need[process][i]:
            continue
        else:
            print("Error: Process has exceeded maximum claim!!")
            sys.exit()
            
    if (x == R-1):
        for i in range(R):
            x=i
            if request[i] <= avail[i]:
                continue
            else:
                print("No, request is denied because of insufficient resources!")
                sys.exit()
                
    if (x == R-1):     
        for i in range(R):
            avail[i] = avail[i] - request[i]
            alloc[process][i] = alloc[process][i] + request[i]
            need[process][i] = need[process][i] - request[i]
                
        safe, l1 = isSafe(R,P,processes, avail, max, alloc)
    
        if(safe==1):
            print("Yes request can be granted with safe state, Safe state <P" + str(process)+"req", *l1 , ">")
        else:
            for i in range(R):
                avail[i] = avail[i] - request[i]
                alloc[process][i] = alloc[process][i] + request[i]
                need[process][i] = need[process][i] - request[i]
                
            print("No, Request Denied!")
            
 
#R = 3
#P = 5
#avail = [3,3,2]
#alloc = [[0,1,0], [2,0,0] , [3,0,2] , [2,1,1] , [0,0,2]]
#max = [[7,5,3], [3,2,2], [9,0,2] , [2,2,2] , [4,3,3]]
#process = 1
#request = [1,0,2]
#processes = [0, 1, 2, 3, 4]
#print(isSafe(R,P,processes,avail,max,alloc))
            
#R = 4
#P = 5
#avail = [1,5,2,0]
#alloc = [[0,0,1,2], [1,0,0,0] , [1,3,5,4] , [0,6,3,2] , [0,0,1,4]]
#max = [[0,0,1,2], [1,7,5,0], [2,3,5,6] , [0,6,5,2] , [0,6,5,6]]
#process = 1
#request = [0,4,2,0]
#processes = [0, 1, 2, 3, 4]


#requestGrant(R,P,process,request, processes,avail,max,alloc)
#print(isSafe(R,P, processes,avail,max,alloc))
takeInput() 


    
    
    
    
    
    
    
    
    
    
    
    
    