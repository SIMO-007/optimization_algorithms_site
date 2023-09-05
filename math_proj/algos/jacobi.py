import numpy as np

mat=np.array([[2, 1, -1, 8],[-3, -1, 2, -11],[-2, 1, 2,-3]])
N=mat.shape[0] # nb of lines of the matrix



def jacobi(mat):
    if check_diag(mat): print("diagonal element is 0"); return 0
    dc=0
    nc=0
    for i in range(N):
        for j in range(N):
            if j==i: dc+=np.abs(mat[i][j])
            else: nc+=np.abs(mat[i][j])
    if dc>nc: print("matrix diagonally dominant")
    else : print("matrix not diagonally dominant") 

    #ln=[0 for x in range(N)]
    ln=np.zeros(N)

    #D=np.diag(mat)
    #b=mat[:,N]
    a=mat[:,:N]
    D=np.diag(mat)
    r=a-np.diagflat(D)
    print(r)
    for i in range(3):
        ln=(mat[:,N]-np.dot(r,ln)) / np.diag(mat)
    print(ln)

    

def check_diag(mat):
    for i in range(N):
        if mat[i][i] == 0 : return 1
    return 0

jacobi(mat)
#print(mat)