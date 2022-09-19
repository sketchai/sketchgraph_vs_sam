import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/sam/')

from sketchgraphs.data.sequence import NodeOp
from sketchgraphs_vs_sam.convert.convert_primitive import SGtoExchangePrimitive
import logging
import unittest


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestConvert(unittest.TestCase):


    def test_convert_point(self):
        # Test 1
        sg_point = NodeOp(label=0, parameters={'isConstruction': True,'x': 0.5,'y': 0.4})
        logger.info(f"sg_point: {sg_point}")
        ex_point = SGtoExchangePrimitive.convert(op = sg_point)
        self.assertEqual('Point P(0.5, 0.4)', str(ex_point))
        self.assertTrue(ex_point.is_construction())

        # Test 2
        sg_point = NodeOp(label=0, parameters={'isConstruction': False,'x': 0.8,'y': 1.4})
        logger.info(f"sg_point: {sg_point}")
        ex_point = SGtoExchangePrimitive.convert(op = sg_point)
        self.assertEqual('Point P(0.8, 1.4)', str(ex_point))
        self.assertFalse(ex_point.is_construction())

    def test_convert_line(self):
        # Test 1
        sg_format = NodeOp(label=1, parameters={'isConstruction': True,'pntX': 0.5,'pntY': 0.4, 
                                                'dirX': 0.5, 'dirY':0.1, 'startParam' : 0., 'endParam': 1.})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format )
        self.assertEqual('Line p1=Point P(0.5, 0.4), p2=Point P(1.0, 0.5)', str(exchange_format))
        self.assertTrue(exchange_format.is_construction())

        # Test 2
        sg_format = NodeOp(label=1, parameters={'isConstruction': False,'pntX': 0.2,'pntY': 0.1, 
                                                'dirX': 1., 'dirY':1., 'startParam' : 0.5, 'endParam':0.3})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format)
        self.assertEqual('Line p1=Point P(0.7, 0.6), p2=Point P(0.5, 0.4)', str(exchange_format))
        self.assertFalse(exchange_format.is_construction())

    def test_convert_circle(self):
        # Test 1
        sg_format = NodeOp(label=2, parameters={'isConstruction': True,'xCenter': 0.5,'yCenter': 0.4, 
                                                'xDir': 0.5, 'yDir':0.1, 'radius' : 6., 'clockwise': 1.})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format )
        self.assertEqual('Circle: center=Point P(0.5, 0.4), radius=  6.0', str(exchange_format))
        self.assertTrue(exchange_format.is_construction())

        # Test 2
        sg_format = NodeOp(label=2, parameters={'isConstruction': False,'xCenter': 10.5,'yCenter': 5.4, 
                                                'xDir': 0.5, 'yDir':0.1, 'radius' : 3., 'clockwise': 1.})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format)
        self.assertEqual('Circle: center=Point P(10.5, 5.4), radius=  3.0', str(exchange_format))
        self.assertFalse(exchange_format.is_construction())

    def test_convert_arc(self):
        # Test 1
        sg_format = NodeOp(label=6, parameters={'isConstruction': True,'xCenter': 0.5,'yCenter': 0.4, 
                                                'xDir': 0.5, 'yDir':0.1, 'radius' : 6., 'clockwise': 1.,
                                                'startParam' : 0., 'endParam': 0.1})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format )
        self.assertEqual('Arc center=Point P(0.5, 0.4),  radius= 6.0, start angle= 5.580354522711981, end angle= 11.309932474020213', str(exchange_format))
        self.assertTrue(exchange_format.is_construction())

        # Test 2
        sg_format = NodeOp(label=6, parameters={'isConstruction': False,'xCenter': 0.5,'yCenter': 0.4, 
                                                'xDir': 10.5, 'yDir':4.1, 'radius' : 6., 'clockwise': 1.,
                                                'startParam' : 0., 'endParam': 0.1})
        logger.info(f"sg_point: {sg_format}")
        exchange_format = SGtoExchangePrimitive.convert(op = sg_format)
        self.assertEqual('Arc center=Point P(0.5, 0.4),  radius= 6.0, start angle= 15.59988356397131, end angle= 21.329461515279544', str(exchange_format))
        self.assertFalse(exchange_format.is_construction())