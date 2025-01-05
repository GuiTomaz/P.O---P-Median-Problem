from typing import List
from optframe import *
from optframe.protocols import *
import random
class SolutionPMedian(object):
    def __init__(self, p: int):
        #consideramos cada vertice como um "cliente" e cada median um "centro de distribuição"
        #num de medians a serem escolhidos
        self.p=p
        #indice dos medians
        self.medians=[]
        #lista que associa cada "cliente" para um median
        self.allocations = []
    
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
        return SolutionPMedian(self.num_locations, self.num_medians,medians, allocations)