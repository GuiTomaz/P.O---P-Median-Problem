
import optframe as op
from optframe import *
from optframe.protocols import *

from optframe.heuristics import *
from mainPMedian_fcore_ils import SolutionPMedian, ProblemContextPMedian, SwapMedian
import random

#funcao callback do optframe que gera uma solucao inicial
def callback_construtor(ctx:ProblemContextPMedian):

    return ctx.generateSolution()

#funcao callback do optframe que avalia uma solucao
def callback_avaliador(ctx:ProblemContextPMedian, solucao:SolutionPMedian):

    return ctx.evaluate_solution(solucao)

#incializacao do engine do optframe
engine = op.Engine(op.APILevel.API1d)

#criacao do contexto do problema
contexto = ProblemContextPMedian()
contexto.load_data('example1.txt')

#criacao do avaliador e construtor
avaliador = engine.minimize(contexto,callback_avaliador)

contructive = engine.add_constructive(contexto,callback_construtor)

#criacao da solucao inicial
initialSolution = engine.create_initial_search(avaliador,contructive)

avl = engine.get_evaluator(avaliador)

ct = engine.get_constructive(contructive)

soln = engine.fconstructive_gensolution(ct)
print("Solucao do teste: ", soln)

#avaliacao da solucao
z1 = engine.fevaluator_evaluate(avl,False,soln)
print("Avalicao do teste: ",z1)
print()
#------------------------------------------------
class callback_move(object):
    def randomMove(ctx:ProblemContextPMedian, sol:SolutionPMedian) -> SwapMedian:

        return SwapMedian(random.randint(0, ctx.num_locations-1), random.randint(0, ctx.num_locations-1))
    

# get index of new NS
ns_idx = engine.add_ns_class(contexto, callback_move)

# pack NS into a NS list
list_idx = engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
alpha= 0.80
IterMax = 100
T0= 99999
# gs_idx = engine.build_global_search("OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA","OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0 OptFrame:NS[] 0 " + str(alpha) + " " + str(T0) + " " + str(IterMax))

# # run Simulated Annealing for 10.0 seconds
# lout = engine.run_global_search(gs_idx, 30.0)
# print('lout=', lout)

sa = BasicSimulatedAnnealing(engine, 0, 0, list_idx, alpha, IterMax, T0)
print("will invoke Simulated Annealing")
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)