
import optframe as op
from optframe import *
from optframe.protocols import *
from mainPMedian_fcore_ils import SolutionPMedian, ProblemContextPMedian

def callback_construtor(ctx:ProblemContextPMedian):

    return ctx.generateSolution()

def callback_avaliador(ctx:ProblemContextPMedian, solucao:SolutionPMedian):

    return ctx.evaluate_solution(solucao)

engine = op.Engine(op.APILevel.API1d)


contexto = ProblemContextPMedian()
contexto.load_data('example1.txt')

avaliador = engine.minimize(contexto,callback_avaliador)


contructive = engine.add_constructive(contexto,callback_construtor)

initialSolution = engine.create_initial_search(avaliador,contructive)

avl = engine.get_evaluator(avaliador)

ct = engine.get_constructive(contructive)

solxx = engine.fconstructive_gensolution(ct)
print(solxx)

z1 = engine.fevaluator_evaluate(avl,False,solxx)
print(z1)
