import sys
from turtle import circle
sys.path.append('src/sketchgraphs/')
sys.path.append('src/sketch_data/')

from sketchgraphs.data.sequence import EdgeOp
from sketchgraphs.data.sketch import DirectionValue
from src.convert.convert_constraint import SGtoExchangeConstraint
from src.sketch_data.sketch_data.catalog_primitive import Point, Line, Circle
import logging
import unittest


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestConvert(unittest.TestCase):

    def test_convert_coincident(self):
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=0, references= [pnt_1,pnt_2])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('COINCIDENT: ref_1: Point P(0.1, 0.5)-- COINCIDENT: ref_2: Point P(0.1, 0.5)', str(ex_format))

    def test_convert_horizontal(self):
        sg_format = EdgeOp(label=4, references= [0,1])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('HORIZONTAL: ref_1: 0, ref_2: 1', str(ex_format))


    def test_convert_distance(self):
        sg_format = EdgeOp(label=3, references= [0,1], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('DISTANCE: ref_1: 0, ref_2: 1, distance_min = 0.4', str(ex_format))

    def test_convert_distance(self):
        sg_format = EdgeOp(label=3, references= [0,1], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('DISTANCE: ref_1: 0, ref_2: 1, distance_min = 0.4', str(ex_format))


    def test_convert_length(self):
        sg_format = EdgeOp(label=8, references= [0,1], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('LENGTH: ref= 0, length = 0.4', str(ex_format))

        sg_format = EdgeOp(label=8, references= [0,1], parameters = {'length' : 0.4, 'direction' : DirectionValue.HORIZONTAL})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('HORIZONTAL_LENGTH: ref= 0, length = 0.4', str(ex_format))



    def test_convert_midpoint(self):
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=10, references= [pnt_1,pnt_2])
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertIsNone(ex_format)

        pnt_1 = Point(point = [0.1, 0.5])
        line =  Line(pnt1 = [0.2,0.2], pnt2= [0.3, 0.7])
        sg_format = EdgeOp(label=10, references= [pnt_1,line])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('MIDPOINT: ref_1: Point P(0.1, 0.5), ref_2: Line p1=Point P(0.2, 0.2), p2=Point P(0.3, 0.7)', str(ex_format))

    def test_convert_radius(self):
        sg_format = EdgeOp(label=14, references= [0], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('RADIUS: ref= 0, radius_constraint = 0.4', str(ex_format))

    def test_convert_diameter(self):
        sg_format = EdgeOp(label=12, references= [0], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('RADIUS: ref= 0, radius_constraint = 0.2', str(ex_format))

    def test_convert_concentric(self):

        # Test 1: two circles
        circle_1 = Circle(status_construction=False, center=[0., 5.], radius=1)
        circle_2 = Circle(status_construction=False, center=[0., 5.], radius=2)
        sg_format = EdgeOp(label=15, references= [circle_1, circle_2])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('COINCIDENT: ref_1: Circle: center=Point P(0.0, 5.0), radius=  1-- COINCIDENT: ref_2: Circle: center=Point P(0.0, 5.0), radius=  2', str(ex_format))

        # Test 2: two points
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=15, references= [pnt_1,pnt_2])
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertIsNone(ex_format)

    def test_angle(self):

        # Test 1: clockwise
        sg_format = EdgeOp(label=17, references= [0, 1], parameters = {'angle': 30, 'clockwise' : True})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('ANGLE: ref_1: 0, ref_2: 1, angle = 30', str(ex_format))

        # Test 2: counter-clockwise
        sg_format = EdgeOp(label=17, references= [0, 1], parameters = {'angle': 30, 'clockwise' : False})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format)
        self.assertEqual('ANGLE: ref_1: 0, ref_2: 1, angle = -30', str(ex_format))