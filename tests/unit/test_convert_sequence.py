import sys

sys.path.append('src/sketchgraphs/')
sys.path.append('src/sketch_data/')
sys.path.append('src/filtering-pipeline/')

from src.convert.convert_sequence import convert_sequence
from tests.asset.mock.source_fromflatarray import SourceFromFlatArray

import logging
import unittest

from sketchgraphs.data.sequence import NodeOp

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import matplotlib.pyplot as plt

class TestConvert(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.source = SourceFromFlatArray(conf={'file_path': 'tests/asset/sg_t16_mini.npy'})
        self.nb_elements = 3

    def test_convert_sequence(self):
        gen = self.source.generator()

        m = next(gen)
        # m = next(gen)
        # m = next(gen)
        # m = next(gen)
        # m = next(gen)
        cpt = 0

        logger.debug(f'---')
        for i,e in enumerate(m.get('sequence')) :
            if isinstance(e, NodeOp):
                logger.info(f'  {cpt}. {e}')
                cpt += 1
            else :
                logger.info(f'     . {e}')
        convert = convert_sequence(m.get('sequence'))
        logger.info(f'sequ: {convert}')

        for i,e in enumerate(convert.sequence) :
            logger.info(f'     . {e}')
        convert.draw()
        plt.show()

