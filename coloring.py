def isSafe(v, colour, c): 
    for i in range(n): 
        if graph[v][i] == 1 and colour[i] == c: 
            return False
    return True
      
def graphColourUtil(m, colour, v): 
    if v == n: 
        return True
  
    for c in range(1, m + 1): 
        if isSafe(v, colour, c) == True: 
            colour[v] = c 
            if graphColourUtil(m, colour, v + 1) == True: 
                return True
            colour[v] = 0
  
def graphColouring(m): 
    colour = [0] * n
    global altitude_append_list
    global altitude_list
    altitude_append_list = []
    altitude_list = []

    if graphColourUtil(m, colour, 0) == None: 
        print("Solution exists False")
        print("try using a smaller n")
        return False
 
    # print("Solution exists True")

    for c in colour: 
#        print(c,)
        altitude_append_list.append(c,)
    altitude_list = altitude_append_list
    return True
