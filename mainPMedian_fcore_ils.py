from typing import List
from optframe import *
from optframe.protocols import *
from optframe.components import Move
import random
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

class ProblemContextPMedian:
    def __init__(self):
        self.num_locations: int = 0 #numero de total de locais(vértices)
        self.num_medians: int = 0 #numero de medians que devemos escolher
        self.distance_matrix: List[List[float]] = [] #Matriz de distancias entre os locais(vertices), a matriz é nxn

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

        #Aqui carregamos a matriz de distancias
        self.distance_matrix=[]
        for i in range(self.num_locations):
            row = list(map(float, lines[2+i].strip().split()))
            self.distance_matrix.append(row)
    
    def evaluate_solution(self, solution:SolutionPMedian) -> float:
        #Esse metodo será útil caso no futuro queiramos avaliar se a solução atende a possíveis outras restrições da solução. Checa se a solução é válida.
        total_cost = 0.0
        for i in range(self.num_locations):
            median = solution.allocations[i]
            total_cost += self.distance_matrix[i][median]
        return total_cost
    
    def generateSolution(self) -> SolutionPMedian:
        medians = random.sample(range(self.num_locations), self.num_medians)

        allocations = []
        for i in range(self.num_locations):
            closest_median = min(medians, key=lambda m: self.distance_matrix[i][m])
            allocations.append(closest_median)
        
        return SolutionPMedian(self.num_medians,medians, allocations)
    
    def minimize(self, solution:SolutionPMedian) -> float:
        total_cost = 0.0
        for i in range(self.num_locations):
            allocated_median=solution.allocations[i]
            distance = self.distance_matrix[i][allocated_median]
            total_cost+=distance
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
        #Solution é a soluçao onde o movimento será aplicado
        if self.old_median in solution.medians and self.new_median not in solution.medians:
            solution.medians.remove(self.old_median)
            solution.medians.append(self.new_median)

            #Recalcula as alocações de cada cliente/vertice para os medians
            for i in range(solution.p):
                closest_median=min(solution.medians, key=lambda m: ctx.distance_matrix[i][m])
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
            
        
assert isinstance(SwapMedian, XMove)       # composition tests
assert SwapMedian in Move.__subclasses__() # classmethod style