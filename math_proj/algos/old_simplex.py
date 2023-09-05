import numpy as np
np.set_printoptions(suppress=True)


A = np.array(
    [[1,1],
     [2,1]])

B = np.array([12,
              16])

OBJ = np.array([40,30])


def convert():
    global A;
    global B;
    global OBJ;
    #print(A)
    A = np.array(A,dtype=float)
    B = np.array(B,dtype=float)
    OBJ = np.array(OBJ,dtype=float)
    #print(A)
    #A = np.transpose(A)
    #x = B
    #B = OBJ
    #OBJ = x
convert()

SOL = np.zeros(len(OBJ))
C = np.append(OBJ,np.zeros(len(A)+1))
S = np.identity(len(A))
PIVOT = [0,0]
print(A)
def extend():
    a=0
    for i in range(len(A)):
        r=np.append(A[i],S[i])
        r=np.append(r,B[i])
        if i==0 :
            a = r
        else : a = np.vstack([a,r])
    a = np.vstack([a,C])
    return a
A = extend()
print(A)

def halt():
    for x in A[-1,:-1]:
        if x > 0 : return False
    return True


def pivot_search():

    PIVOT[1] = np.argmax(A[-1,:-1]) # #type: ignor
    PIVOT[0] = np.argmin(np.abs(A[:-1,-1]/A[:-1,PIVOT[1]])) # #type: ignor

def rotate():
    A[PIVOT[0]] = A[PIVOT[0]]/A[PIVOT[0],PIVOT[1]]

def check_identiy(a):
    zero = 0
    one = 0
    for x in a:
        if x == 0 : zero+=1
        elif x == 1 : one+=1
    if one == 1 and zero == len(a)-1:
        return True
    return False

def calc_obj():
    sum = 0
    for i in range(len(OBJ)):
        if check_identiy(A[:,i]):
            for j in range(len(A[:,i])):
                if A[:,i][j] == 1:
                    sum += OBJ[i]*A[j,-1]
                    SOL[i] = A[j,-1]
                    break              
    A[-1,-1] = sum
   
def gauss():
    for i in range(len(A)-1):
        if i == PIVOT[0] : continue
        A[i] = A[i] - A[i,PIVOT[1]]*A[PIVOT[0]]

    A[-1,:-1] = A[-1,:-1] - A[-1,PIVOT[1]]*A[PIVOT[0],:-1]

def simplex():
    i=0
    tabs = list()
    print(tabs)
    while True:
        i+=1
        pivot_search()
        rotate()
        gauss()
        calc_obj()
        print(np.round(A,3),"\n")
        tabs.append(np.round(A,3))
        if halt():
            tabs.append(SOL)
            return (i,tabs)

def main():
    res = simplex()
    print(f"solution : {res[1][-1]} ; number of iterations : {res[0]}")
    return res[1]

if __name__ == '__main__':   
    main()

