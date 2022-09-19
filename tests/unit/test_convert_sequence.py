import sys

sys.path.append('src/sketchgraphs/')
sys.path.append('src/sam/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs_vs_sam.convert.convert_sequence import convert_sequence
from tests.asset.mock.source_fromflatarray import SourceFromFlatArray
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *

import logging
import unittest

from sketchgraphs.data.sequence import NodeOp

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import matplotlib.pyplot as plt

def show_result(sketch):
    sketch.draw()
    plt.show()

def print_sequence(seq):
    logger.debug(f'--- Original Sequencen')
    cpt = 0
    for i,e in enumerate(seq) :
        if isinstance(e, NodeOp):
            logger.info(f'  {cpt}. {e}')
            cpt += 1
        else :
            logger.info(f'     - {e}')

def print_convert_sequence(seq):
    logger.debug(f'--- Convert sequence')
    for i,e in enumerate(seq) :
        logger.info(f'     . {e}')

class TestConvert(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.source = SourceFromFlatArray(conf={'file_path': 'tests/asset/sg_t16_mini.npy'})

    def test_convert_sequence(self):
        gen = self.source.generator()

        # Test 1 : 2 circles
        m = next(gen)
        seq = m.get('sequence')
        sketch, nb_edges, nb_nodes = convert_sequence(seq)
        print_sequence(seq)
        print_convert_sequence(sketch.sequence)
        # show_result(sketch)
        self.assertListEqual([nb_edges, nb_nodes], [1,2])
        self.assertTrue(isinstance(sketch.sequence[0], Circle))
        self.assertTrue(isinstance(sketch.sequence[1], Circle))
        self.assertTrue(isinstance(sketch.sequence[2], Coincident))

        # Test 2 : Triangle 
        for i in range(4) :
            m = next(gen)

        seq = m.get('sequence')
        sketch, nb_edges, nb_nodes = convert_sequence(seq)
        print_sequence(seq)
        print_convert_sequence(sketch.sequence)
        # show_result(sketch)
        self.assertListEqual([nb_edges, nb_nodes], [3,3])
        for i in range(3):
            self.assertTrue(isinstance(sketch.sequence[i], Line))
            self.assertTrue(isinstance(sketch.sequence[i+3], Coincident))




