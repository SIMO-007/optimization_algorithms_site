import numpy as np
np.set_printoptions(suppress=True)


class simplex():
    def __init__(self,a,b,obj):
        self.A = a
        self.cont = len(self.A)
        
        self.B = b
        self.OBJ = obj
        self.out = ''
        self.inn = ''
        self.info = [f"S{i}" for i in range(1,len(self.OBJ)+1)] + ['Z']
        print(f'\n constraints : {self.cont}')
        print("\n")
        print(self.A,self.B,self.OBJ)
        print("\n")
        self.A = np.array(self.A,dtype=float)
        self.B = np.array(self.B,dtype=float)
        self.OBJ = np.array(self.OBJ,dtype=float)

        print(self.A,self.B,self.OBJ)
        print(f'A :{self.A} B : {self.B} OBJ : {self.OBJ}')
        print("\n")
        #self.A = np.transpose(self.A)
        x = self.B
        self.B = self.OBJ
        self.OBJ = x

        self.SOL = np.zeros(len(self.OBJ))
        self.C = np.append(self.OBJ,np.zeros(len(self.A)+1))
        self.S = np.identity(len(self.A))
        self.PIVOT = [0,0]
    
    def extend(self):
        A = (self.A)
        OBJ = self.OBJ
        B = self.B
        C = self.C
        S = self.S
        a = 0
        for i in range(len(A)):
            r=np.append(A[i],S[i])
            r=np.append(r,B[i])
            if i==0 :
                a = r
            else : a = np.vstack([a,r])
        a = np.vstack([a,C])
        A = a
        
        self.A = A
        self.B = B
        self.OBJ = OBJ
        self.C = C
        self.S = S
        print(f" THE A : {self.A}")

    def halt(self):
        for x in self.A[-1,:-1]:
            if x > 0 : return False
        return True

    def pivot_search(self):
        PIVOT = self.PIVOT
        A = self.A
        
        PIVOT[1] = np.argmax(A[-1,:-1]) # type: ignore
        PIVOT[0] = np.argmin(np.abs(A[:-1,-1]/A[:-1,PIVOT[1]])) # type: ignore
           
        self.PIVOT = PIVOT
    
    def rotate(self):
        A = self.A    
        PIVOT = self.PIVOT   
        A[PIVOT[0]] = A[PIVOT[0]]/A[PIVOT[0],PIVOT[1]]
        self.A = A


    def check_identiy(self,a):
        zero = 0
        one = 0
        for x in a:
            if x == 0 : zero+=1
            elif x == 1 : one+=1
        if one == 1 and zero == len(a)-1:
            return True
        return False
    
    def calc_obj(self):
        A = self.A
        OBJ = self.OBJ
        SOL = self.SOL

        sum = 0
        for i in range(len(OBJ)):
            if self.check_identiy(A[:,i]):
                for j in range(len(A[:,i])):
                    if A[:,i][j] == 1:
                        sum += OBJ[i]*A[j,-1]
                        SOL[i] = A[j,-1]
                        break            
        A[-1,-1] = sum
        self.A = A
        self.OBJ = OBJ
        self.SOL = SOL
    
    def gauss(self):
        A = self.A    
        PIVOT = self.PIVOT  
        for i in range(len(A)-1):
            if i == PIVOT[0] : continue
            A[i] = A[i] - A[i,PIVOT[1]]*A[PIVOT[0]]

        A[-1,:-1] = A[-1,:-1] - A[-1,PIVOT[1]]*A[PIVOT[0],:-1]
        A = self.A




    def clean(self,M):
        res = dict()
        res['iter'] = M[1]
        res['sol'] = M[-1]
        res['z'] = M[0]
        i=0
        for t in M[2]:
            res[f'Iteration {i} '] = t
            i+=1
            
        
        return res
        
    def in_out(self,p,a):
        base = ['Base'] + [f'X{i}' for i in range(1,len(self.OBJ)+1)] + [f'S{i}' for i in range(1,self.cont + 1)] + ['R']
        info = self.info
        for i in range(len(a)):
            a[i].insert(0,info[i]) 
            
        a.insert(0,base)
        print(f'\nPIVOT = {p} ')
        print(f' \n base = {base}  \n info = {info}')
        info[1] = 'X'+str(p[0]+1)
        self.info = info
        
        return a

    def algo(self):
        self.extend()
        A = self.A
        SOL = self.SOL
        i=0
        tabs = list()
        
        tabs.append(self.in_out(self.PIVOT,A.tolist()))
        while True:
            #print(f'\n PIVOT = {self.PIVOT} \n')
            #self.in_out(self.PIVOT)
            
            self.pivot_search()
            self.rotate()
            self.gauss()
            self.calc_obj()
            i+=1
            #print(np.round(A,3),"\n")
            tabs.append(self.in_out(self.PIVOT,np.round(A,2).tolist())) # type : ignore
            if self.halt():
                #print(f'\n PIVOT = {self.PIVOT} \n')
                #self.in_out(self.PIVOT)
                
                res = np.round(SOL,2).tolist()
                Z = A[-1][-1]
                print(f'Z ====== {Z}')
                #tabs.append(np.round(SOL,2).tolist())
                self.A = A
                self.SOL = SOL
                return self.clean([np.round(Z,2),i,tabs,res])
            

def main(i1,i2,i3):
    a = np.array(i1)
    b = np.array(i2)
    obj = np.array(i3)
    s = simplex(a,b,obj)
    res = s.algo()
    
    print(res)
    #print(f"solution : {res['sol']} ; number of iterations : {res['iter']}")
    
    return res

