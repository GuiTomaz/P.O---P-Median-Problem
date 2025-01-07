from typing import List
from optframe import *
from optframe.protocols import *
from optframe.components import Move
import random
from optframe.components import NSIterator

class SolutionPMedian(object):
    
    def __init__(self, p: int, medians: List[int] = [], allocations: List[int] = []):
        #consideramos cada vertice como um "cliente" e cada median um "centro de distribuição"
        #num de medians a serem escolhidos
        self.p=p
        #indice dos medians
        self.medians= medians
        #lista que associa cada "cliente" para um median
        self.allocations = allocations

    def __str__(self):
        return f"SolutionPMedian(p={self.p}, medians={self.medians}, allocations={self.allocations})"

class ProblemContextPMedian(object):
    def __init__(self):
        # float engine for OptFrame
        self.engine = Engine(APILevel.API1d)
        self.num_locations: int = 0 #numero de total de locais(vértices)
        self.num_medians: int = 0 #numero de medians que devemos escolher
        self.distance_matrix: List[List[float]] = [] #Matriz de distancias entre os locais(vertices), a matriz é nxn
        self.capacity: int = 0
    
    def __str__(self):
        return f"ProblemContextPMedian(num_locations={self.num_locations}, num_medians={self.num_medians}, distance_matrix={self.distance_matrix})"
    
    #Formato da entrada
    #numero total de locais/vertices
    #numero de medians
    #linha 1 da matriz de distancias associada ao vertice 1
    #linha n da matriz de distancias associada ao vertice n
    #a matriz de distancia mostra a distancia de um vertice a outro
    #Cheque o arquivo para entender melhor o formato da entrada
    def load_data(self, filename:str):
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        self.num_locations = int(lines[0].strip()) #lembrando: num total de vertices
        self.num_medians = int(lines[1].strip()) #num de medians
        self.capacity = int(lines[2].strip())
        #Aqui carregamos a matriz de distancias
        self.distance_matrix=[]
        for i in range(self.num_locations):
            row = list(map(float, lines[3+i].strip().split()))
            self.distance_matrix.append(row)
    
    # def evaluate_solution(self, solution:SolutionPMedian) -> float:
    #     #Esse metodo será útil caso no futuro queiramos avaliar se a solução atende a possíveis outras restrições da solução. Checa se a solução é válida.
    #     total_cost = 0.0
    #     for i in range(self.num_locations):
    #         median = solution.allocations[i]
    #         total_cost += self.distance_matrix[i][median]
    #     return total_cost
    
    @staticmethod
    def generateSolution(self) -> SolutionPMedian:
        medians = random.sample(range(self.num_locations), self.num_medians)

        allocations = []
        for i in range(self.num_locations):
            closest_median = min(medians, key=lambda m: self.distance_matrix[i][m])
            allocations.append(closest_median)
        
        return SolutionPMedian(self.num_medians,medians, allocations)
    
    @staticmethod
    def minimize(self, solution:SolutionPMedian) -> float:
        total_cost = 0.0
        for i in range(self.num_locations):
            allocated_median=solution.allocations[i]
            distance = self.distance_matrix[i][allocated_median]
            total_cost+=distance
        penalty = 10000
        for mdn in solution.medians:
            count = 0
            for z in range(self.num_locations):
                if(mdn == solution.allocations[z]):
                    count += 1
                if(count > self.capacity):
                    total_cost += penalty
                    break
        return total_cost
assert isinstance(SolutionPMedian, XSolution)            # composition tests 
assert isinstance(ProblemContextPMedian,  XProblem)      # composition tests 
assert isinstance(ProblemContextPMedian,  XConstructive) # composition tests    
assert isinstance(ProblemContextPMedian,  XMinimize)     # composition tests
class SwapMedian(Move):
    def __init__(self, _old_median:int, __new_median:int):
        #Troca um median existente por outro, old_median = median a ser trocado new_median=median a ser adicionado a soluçao
        self.old_median = _old_median
        self.new_median = __new_median 
    
    def apply(self, ctx, solution: SolutionPMedian) -> 'SwapMedian':
    # Verifica se a troca de median é válida
        if self.old_median in solution.medians and self.new_median not in solution.medians:
            # Troca o median antigo pelo novo
            solution.medians.remove(self.old_median)
            solution.medians.append(self.new_median)

        # Recalcula as alocações para todos os vértices
        for i in range(ctx.num_locations):  # Corrigido para usar ctx.num_locations
            closest_median = min(solution.medians, key=lambda m: ctx.distance_matrix[i][m])
            solution.allocations[i] = closest_median

        return SwapMedian(self.new_median, self.old_median)

    def canBeApplied(self, ctx , solution: SolutionPMedian) -> bool:
        return True
    
    def eq(self, ctx, mv: 'SwapMedian') -> bool:
        return self.old_median == mv.old_median and self.new_median == mv.new_median
    
    # def undo(self, solution: SolutionPMedian):
    #     #desfaz o movimento
    #     if self.new_median in solution.medians:
    #         solution.medians.remove(self.new_median)
    #         solution.medians.append(self.old_median)
    #         self.update_allocations(solution)
    def __str__(self):
        return "SwapMedian(old_median="+str(self.old_median)+";new_median="+str(self.new_median)+")"
        
assert isinstance(SwapMedian, XMove)       # composition tests
assert SwapMedian in Move.__subclasses__() # classmethod style

class NSSwap(object):
    @staticmethod
    def randomMove(ctx, solution: SolutionPMedian) -> SwapMedian:
        old_median = random.choice(solution.medians)
        new_median = random.choice([m for m in range(ctx.num_locations) if m not in solution.medians])
        return SwapMedian(old_median, new_median)
    
   
class IteratorSwap(NSIterator):
    def __init__(self, medians, num_locations):
        self.medians = medians
        self.num_locations = num_locations
        self.i = 0
        self.j = 0

    def first(self, ctx):
        self.i = 0
        self.j = 0

    def next(self, ctx):
        if self.j < self.num_locations - 1:
            self.j += 1
        else:
            self.i += 1
            self.j = 0

    def isDone(self, ctx):
        return self.i >= len(self.medians) - 1

    def current(self, ctx):
        old_median = self.medians[self.i]
        new_median = self.j

        # Verifica se new_median não é um dos medians já presentes
        if new_median not in self.medians:
            return SwapMedian(old_median, new_median)
        else:
            self.next(ctx)  # Avança para o próximo par válido
            return self.current(ctx)

       
assert IteratorSwap in NSIterator.__subclasses__()   # optional test
class NSSeqSwap(object):
    @staticmethod
    def randomMove(ctx, solution:SolutionPMedian) -> SwapMedian:
        return NSSwap.randomMove(ctx, solution)
    
    @staticmethod
    def getIterator(ctx, solution:SolutionPMedian) -> IteratorSwap:
        return IteratorSwap(solution.medians, ctx.num_locations)
