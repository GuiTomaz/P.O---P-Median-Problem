
import optframe as op
from optframe import *
from optframe.protocols import *
from mainPMedian_fcore_ils import SolutionPMedian, ProblemContextPMedian

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

solxx = engine.fconstructive_gensolution(ct)
print(solxx)

#avaliacao da solucao
z1 = engine.fevaluator_evaluate(avl,False,solxx)
print(z1)
