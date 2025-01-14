
import optframe as op
from optframe import *
from optframe.protocols import *

from optframe.heuristics import *
from pmedian_core import SolutionPMedian, ProblemContextPMedian, SwapMedian
import random
import time
start_time = time.time()
#funcao callback do optframe que gera uma solucao inicial
def callback_construtor(ctx:ProblemContextPMedian):

    return ctx.generateSolution(ctx)

#funcao callback do optframe que avalia uma solucao
def callback_avaliador(ctx:ProblemContextPMedian, solucao:SolutionPMedian):

    return ctx.minimize(ctx, solucao)




#criacao do contexto do problema
context = ProblemContextPMedian()
#context.load_data('example2.txt')
#context.load_data('gen_example1.txt')
context.load_data('gen_example2.txt')
#criacao do avaliador e construtor
avaliador =  context.engine.minimize(context,callback_avaliador)

contructive = context.engine.add_constructive(context,callback_construtor)

#criacao da solucao inicial
initialSolution = context.engine.create_initial_search(avaliador,contructive)

avl = context.engine.get_evaluator(avaliador)

ct = context.engine.get_constructive(contructive)

soln = context.engine.fconstructive_gensolution(ct)
print("Solucao do teste: ", soln)

#avaliacao da solucao
z1 = context.engine.fevaluator_evaluate(avl,False,soln)
print("Avalicao do teste: ",z1)
print()
#------------------------------------------------
class callback_move(object):
    def randomMove(ctx:ProblemContextPMedian, sol:SolutionPMedian) -> SwapMedian:

        return SwapMedian(random.randint(0, ctx.num_locations-1), random.randint(0, ctx.num_locations-1))
    

# get index of new NS
ns_idx = context.engine.add_ns_class(context, callback_move)

# pack NS into a NS list
list_idx = context.engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")



def find_best_SA_params(alpha_params, max_iter_params, t0_params, num_runs=10, search_time=10):
    best_params = [0, 0, 0]
    best_evaluation = float('inf') 
    results = []

    for alpha in alpha_params:
        for mx_it in max_iter_params:
            for tp in t0_params:
                sa = BasicSimulatedAnnealing(context.engine, 0, 0, list_idx, alpha, mx_it, tp)
                total_eval = 0

                for i in range(num_runs):
                    sout = sa.search(search_time)
                    total_eval += sout.best_e

                avg_eval = total_eval / num_runs
                results.append((alpha, mx_it, tp, avg_eval))

                if avg_eval < best_evaluation:
                    best_evaluation = avg_eval
                    best_params = [alpha, mx_it, tp]
     # Exibe os melhores parâmetros encontrados
    print("Melhores parâmetros encontrados:")
    print("Resultados gerais", results)
    print(f"Alpha: {best_params[0]}")
    print(f"Iter: {best_params[1]}")
    print(f"T0: {best_params[1]}")
    print(f"Avaliação média: {best_evaluation}")
    return best_params, best_evaluation, results


alpha = [0.8, 0.85, 0.90, 0.95, 0.99]
iterMax = [1000, 2000, 5000, 10000]
T0 = [1000, 2000, 5000, 10000]

best_params, best_evaluation, results = find_best_SA_params(alpha, iterMax, T0)
print("Em resumo, melhores params: ", best_params)

def run_SA(num_runs=10, search_time=10, alpha=0.8, iterMax=1000, T0 = 1000):

    sa = BasicSimulatedAnnealing(context.engine, 0, 0, list_idx, alpha, iterMax, T0)
    total_eval = 0

    best_evaluation = float('inf') 
    best_solution = []

    tempo_total = 0
    for i in range(num_runs):
        start = time.time()
        sout = sa.search(search_time)
        end = time.time()
        tempo_total += (end - start)  
        if(sout.best_e < best_evaluation):
            best_evaluation = sout.best_e
            best_solution = sout.best_s
        total_eval += sout.best_e
    avg_eval = total_eval / num_runs
    tempo_medio = tempo_total / num_runs
    print("Tempo médio computacional", tempo_medio)
    return avg_eval, best_evaluation, best_solution
# gs_idx = engine.build_global_search("OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA","OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0 OptFrame:NS[] 0 " + str(alpha) + " " + str(T0) + " " + str(IterMax))

# # run Simulated Annealing for 10.0 seconds
# lout = engine.run_global_search(gs_idx, 30.0)
# print('lout=', lout)

"""""
# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
#alpha= 0.9
#IterMax = 5000
#T0=1000
sa = BasicSimulatedAnnealing(context.engine, 0, 0, list_idx, alpha, IterMax, T0)
print("will invoke Simulated Annealing")
sout = sa.search(60.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)
"""



avg_eval, best_ev, best_sol = run_SA(10, 60)
print("Melhor solução encontrada: ", best_sol)
print("Valor da melhor solução encontrada:", best_ev)
print("Valor médio da solução (10 execuções): ", avg_eval)

print("FINISHED")
print("--- tempo: %s seconds ---" % (time.time() - start_time))