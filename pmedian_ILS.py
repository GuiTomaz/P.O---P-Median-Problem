import optframe as op
from optframe.components import *
from optframe.protocols import *
from optframe.heuristics import *

from pmedian_core import *
import random

import time
start_time = time.time()

random.seed()

# Load the problem
context =  ProblemContextPMedian()
#context.load_data('example2.txt')
#context.load_data('gen_example1.txt')
#context.load_data('gen_example2.txt')
context.load_data('example3.txt')
print(context)

#Registrando componentes basicos
comp_list = context.engine.setup(context)
#print(comp_list)

#acessa o indice da NS
ns_idx = context.engine.add_ns_class(context, NSSwap)
nsseq_idx = context.engine.add_nsseq_class(context, NSSeqSwap)
gev_idx = comp_list[0]
ev_idx = comp_list[1]
c_idx = comp_list[2]
is_idx = comp_list[3]


fev = context.engine.get_evaluator(ev_idx)

fc = context.engine.get_constructive(c_idx)

initialSolution = context.engine.fconstructive_gensolution(fc)
#print(initialSolution)
iniSolEvaluation = context.engine.fevaluator_evaluate(fev, True, initialSolution)
#print(iniSolEvaluation)

# move = SwapMedian(initialSolution.medians[0], 1)
# print("move= ", move)

# m1 = NSSwap.randomMove(context, initialSolution)
# print("m1=",m1)

# print("Testando o iterador")
# iterator = NSSeqSwap.getIterator(context, initialSolution)
# iterator.first(context)
# while not iterator.isDone(context):
#     m = iterator.current(context)
#     print(m)
#     iterator.next(context)
# print("end test with iterator")

# pack NS into a NS list
list_idx = context.engine.create_component_list(
    "[ OptFrame:NS 0 ]", "OptFrame:NS[]")
#print("list_idx=", list_idx)
# print("Listing registered components:")
# context.engine.list_components("OptFrame:")
#print(context.engine.list_builders("OptFrame:"))
context.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "0")

print("building 'BI' neighborhood exploration as local search", flush=True)
bi = BestImprovement(context.engine, 0, 0)
ls_idx = bi.get_id()
#print("ls_idx=", ls_idx, flush=True)

print("creating local search list", flush=True)
list_vnd_idx = context.engine.create_component_list( "[ OptFrame:LocalSearch 0 ]", "OptFrame:LocalSearch[]")
#print("list_vnd_idx", list_vnd_idx)

print("building 'VND' local search")
vnd = VariableNeighborhoodDescent(context.engine, 0,0)
vnd_idx = vnd.get_id()
#print("vnd_idx=", vnd_idx)

#context.engine.list_components("OptFrame:")

ilsl_pert = ILSLevelPertLPlus2(context.engine, 0,0)
pert_idx = ilsl_pert.get_id()
#print("pert_idx=",pert_idx)

#context.engine.list_components("OptFrame:")

context.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "3")


def find_best_ILS_params(max_iter_params, max_pert_params, num_runs=10, search_time=10):
   
    best_params = [0, 0]
    best_evaluation = float('inf') 
    results = []

    for mx_it in max_iter_params:
        for mx_pt in max_pert_params:
            ilsl = ILSLevels(context.engine, 0, 0, 1, 0, mx_it, mx_pt)
            total_eval = 0
            
            for i in range(num_runs):
                lout = ilsl.search(search_time)  # Executa por search_time segundos
                total_eval += lout.best_e
            
            avg_eval = total_eval / num_runs
            results.append((mx_it, mx_pt, avg_eval))
            
            if avg_eval < best_evaluation:
                best_evaluation = avg_eval
                best_params = [mx_it, mx_pt]
    
    # Exibe os melhores parâmetros encontrados
    print("Melhores parâmetros encontrados:")
    print("Resultados gerais", results)
    print(f"Max-iter: {best_params[0]}")
    print(f"Max-pert: {best_params[1]}")
    print(f"Avaliação média: {best_evaluation}")
    
    return best_params, best_evaluation, results


def run_ILS(num_runs=10, search_time=10, iterMax=150, maxPert=10):

    #Melhores parametros encontrados usando a find_best_ILS, iterMax= 150, maxPert=10
    #padrão: 10 execucoes e 15 segundos cada
    ilsl = ILSLevels(context.engine, 0, 0, 1, 0, iterMax, maxPert)
    total_eval = 0

    best_evaluation = float('inf') 
    best_solution = []

    tempo_total = 0
    for i in range(num_runs):
        start = time.time()
        lout = ilsl.search(search_time)
        end = time.time()
        tempo_total += (end - start)  
        if(lout.best_e < best_evaluation):
            best_evaluation = lout.best_e
            best_solution = lout.best_s
        total_eval += lout.best_e
    avg_eval = total_eval / num_runs
    tempo_medio = tempo_total / num_runs
    print("Tempo médio computacional", tempo_medio)
    return avg_eval, best_evaluation, best_solution

 

#best_params, best_evaluation, results = find_best_ILS_params(max_iter_params, max_pert_params)

#Melhores parametros encontrados usando a find_best_ILS, (150, 10)
"""ilsl = ILSLevels(context.engine,0,0,1,0,150,10)
sum = 0
for i in range (10):
    lout = ilsl.search(10)
    print("Best solution: ",   lout.best_s)
    print("Best evaluation: ", lout.best_e)
    sum += lout.best_e

print("FIM DO LOOP, valor de i=", i)
avg = sum/10
print("Average: ", avg)"""
avg_eval, best_ev, best_sol = run_ILS(10, 30)

print("Melhor solução encontrada: ", best_sol)
print("Valor da melhor solução encontrada:", best_ev)
print("Valor médio da solução (10 execuções): ", avg_eval)
print("FINISHED")
print("--- Tempo total: %s seconds ---" % (time.time() - start_time))