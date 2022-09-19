from collections import OrderedDict
import enum
from re import sub
from typing import Dict

from sketchgraphs.data.sequence import NodeOp, EdgeOp
from sketchgraphs.data.sketch import ConstraintType, SubnodeType, EntityType
from sam.sketch import Sketch
from .convert_constraint import SGtoExchangeConstraint
from .convert_primitive import SGtoExchangePrimitive

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def collect_node(seq) :
    d_nodes = {'subnode' : {}, 'normal': OrderedDict({}), 'external': [], 'order' : {}}
    cpt = 0
    for i,op in enumerate(seq) :
        if isinstance(op, NodeOp):
            if op.label == EntityType.External:
                d_nodes['external'].append(cpt)
            elif op.label == EntityType.Stop :
                continue
            elif op.label in [SubnodeType.SN_Start, SubnodeType.SN_End, SubnodeType.SN_Center]:
                d_nodes['subnode'][cpt] = op.label
            else :
                d_nodes['normal'][i] = SGtoExchangePrimitive.convert(op = op)
                d_nodes['order'][cpt] = i
            cpt += 1
    return d_nodes

def recover_primitive(references, d_nodes, d_subnode):

    # Catch the subnode index
    if references[0] in d_nodes['subnode']:
        subnode_index = references[0] 
        primitive_index = d_nodes['order'][references[1]]
    else:
        subnode_index = references[1] 
        primitive_index = d_nodes['order'][references[0]]

    if d_nodes['subnode'][subnode_index] == SubnodeType.SN_Center: # Arc or Circle
        d_subnode[subnode_index] = d_nodes['normal'][primitive_index].center
    elif d_nodes['subnode'][subnode_index] == SubnodeType.SN_Start : #Line, pnt1
        d_subnode[subnode_index] = d_nodes['normal'][primitive_index].pnt1
    else : #Line, pnt1
        d_subnode[subnode_index] = d_nodes['normal'][primitive_index].pnt2

def collect_edge(seq, d_nodes : Dict = {}):
    d_edges = OrderedDict({}) 
    d_subnode = {}

    for i,op in enumerate(seq) :
        if isinstance(op, EdgeOp):    
            references = op.references
            # Check if one of the references refers to an external
            if len(list(set(references) & set(d_nodes['external']))) > 0 : 
                continue
            
            if op.label == ConstraintType.Subnode: # Recover the original primitive
                recover_primitive(references, d_nodes, d_subnode)
            else: 
                # Change the references by their associated primitives
                new_ref = []
                for index_ref in references :
                    if index_ref in d_nodes['subnode'] :
                        ref= d_subnode[index_ref] 
                    else :
                        primitive_index = d_nodes['order'][index_ref]
                        ref = d_nodes['normal'][primitive_index]
                    new_ref.append(ref)
                
                converted_constraint = SGtoExchangeConstraint.convert(op = op, new_ref = new_ref)
                if converted_constraint is not None:
                    d_edges[i] = converted_constraint

    
    return d_edges


def convert_sequence(seq:object):
    sketch = Sketch()

    
    d_nodes = collect_node(seq)
    d_edges = collect_edge(seq, d_nodes)
    nb_nodes = len(d_nodes.get('normal'))
    nb_edges = len(d_edges)

    d = d_nodes.get('normal')
    d.update(d_edges)

    for i,elt in d.items():
        sketch.add(elt)


    return sketch, nb_edges, nb_nodes

