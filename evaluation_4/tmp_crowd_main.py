from Preprocess import Preprocess
from Questions import Question

prior_obj = Preprocess()
graph = prior_obj.get_graph()

dummy_input = "dummmmmmmy dummmmmmmy"
qe = Question(dummy_input, prior_obj, graph)


ent_dict, pred_ids = {'The Princess and the Frog':{'id':'Q171300'}}, ['P2142']
qe.process(ent_dict, pred_ids)
qe.chooseResponse()
print(qe.getResponse())
print()

ent_dict, pred_ids = {'Tom Meets Zizou':{'id':'Q1410031'}}, ['P577']
qe.process(ent_dict, pred_ids)
qe.chooseResponse()
print(qe.getResponse())
print()

ent_dict, pred_ids = {'X-Men: First Class':{'id':'Q223596'}}, ['P1431']
qe.process(ent_dict, pred_ids)
qe.chooseResponse()
print(qe.getResponse())
print()