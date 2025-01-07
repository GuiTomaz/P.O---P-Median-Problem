
import optframe as op
from optframe import *
from optframe.protocols import *

from optframe.heuristics import *
from pmedian_core import SolutionPMedian, ProblemContextPMedian, SwapMedian
import random

#funcao callback do optframe que gera uma solucao inicial
def callback_construtor(ctx:ProblemContextPMedian):

    return ctx.generateSolution(ctx)

#funcao callback do optframe que avalia uma solucao
def callback_avaliador(ctx:ProblemContextPMedian, solucao:SolutionPMedian):

    return ctx.minimize(ctx, solucao)




#criacao do contexto do problema
context = ProblemContextPMedian()
context.load_data('example1.txt')

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

# build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
alpha= 0.80
IterMax = 100
T0= 99999
# gs_idx = engine.build_global_search("OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA","OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0 OptFrame:NS[] 0 " + str(alpha) + " " + str(T0) + " " + str(IterMax))

# # run Simulated Annealing for 10.0 seconds
# lout = engine.run_global_search(gs_idx, 30.0)
# print('lout=', lout)

sa = BasicSimulatedAnnealing(context.engine, 0, 0, list_idx, alpha, IterMax, T0)
print("will invoke Simulated Annealing")
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)