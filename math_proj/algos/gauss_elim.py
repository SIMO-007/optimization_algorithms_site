import numpy as np
np.seterr(divide = 'ignore')
class GaussEliminationSolver:
    def __init__(self, mat):
        self.mat = np.array(mat, dtype=np.float64)
        self.N = self.mat.shape[0]
        self.response = []

    def gauss(self):
        if self.elim() == -1:
            print("Inconsistent system")
            return
        res = self.backsub()
        return res

    def elim(self):
        for i in range(self.N):
            imax = i
            vmax = self.mat[imax][i]
            for j in range(i + 1, self.N):
                if np.abs(self.mat[j][i]) > vmax:
                    imax = j
                    vmax = self.mat[j][i]
            #print(f"i = {i} et imax = {imax}")
            if imax != i:
                self.swap(i, imax)

        c = 0
        print(np.round(self.mat,2))
        print("\n")
        #print(np.round(self.mat,2))
        for i in range(self.N):
            if self.mat[i][i] == 0:
                return -1
            if not self.mat[i][-1]:
                c += 1

        if c == self.N:
            return -1
        print(f'\n iter 0 : ')
        print(np.round(self.mat,2))
        self.response.append((np.round(self.mat,2)).tolist())
        
        iter = 0
        
        for i in range(self.N):
            for k in range(i + 1, self.N):
                iter += 1
                print(f"fact = {np.round(self.mat[k][i],2)} / {np.round(self.mat[i][i],2)} \n")
                fact = self.mat[k][i] / self.mat[i][i]
                self.response.append(f"fact = {np.round(self.mat[k][i],2)} / {np.round(self.mat[i][i],2)}")
                
                for j in range(i + 1, self.N + 1):
                    self.mat[k][j] -= self.mat[i][j] * fact
                self.mat[k][i] = 0
                
                print(f'\n iter {iter} : ')
                print(np.round(self.mat,2))
                self.response.append((np.round(self.mat,2)).tolist())
                
        #print(np.round(self.mat,2))
        
        for i in range(self.N):
            
            op = (self.mat[i][i]) - 1 / self.mat[i][i]
            if op == - np.inf : return -2
            self.mat_op(i, i, op)
          
            for j in range(self.N + 1):
                self.mat[i][j] = round(self.mat[i][j], 2)

    def mat_op(self, l1, l2, fact):
        try:
            self.mat[l2] = self.mat[l2] - fact * self.mat[l1]
        except : 
            return -1

    def swap(self, i, j):
        temp = np.array(self.mat[i])
        self.mat[i] = self.mat[j]
        self.mat[j] = temp
        #print(f'swapped mat : \n {self.mat} \n')

    def backsub(self):
        if self.response[-1][0] == np.nan:
            print(f'response : {self.response[-1]}')
            sols = ['system has no solutions']
            self.response.append(sols.tolist())
        sols = []
        x = 1
        
        sols.append(self.mat[self.N - 1][self.N] / self.mat[self.N - 1][self.N - 1])

        for i in range(self.N - 2, -1, -1):
            sol = self.mat[i][self.N]
            for j in range(i + 1, self.N):
                sol -= self.mat[i][j] * sols[i-j]
            sol /= self.mat[i][i]
            sols.append(round(sol, 2))
        print(f'\n\nsolutions : {sols} ,type : {type(sols[0])}')
        sols.reverse()
        if sols[0] == - np.inf or sols[0] == np.inf :
            sols = ['system has no solutions']
            self.response.append(sols
                                 )
        else : self.response.append((np.round(sols,2).tolist()))
        
        return self.response
        

def main(mat):
    
    solver = GaussEliminationSolver(mat)
    res = solver.gauss()
    print('\n')
    print(res)
    #print(f"solution : {res['sol']} ; number of iterations : {res['iter']}")
    
    return res

#main(mat)
