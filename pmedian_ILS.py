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
context.load_data('gen_example2.txt')
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

ilsl = ILSLevels(context.engine,0,0,1,0,100,20)
print("will start ILS for 3 seconds")
lout = ilsl.search(20.0)
print("Best solution: ",   lout.best_s)
print("Best evaluation: ", lout.best_e)

print("FINISHED")
print("--- tempo: %s seconds ---" % (time.time() - start_time))