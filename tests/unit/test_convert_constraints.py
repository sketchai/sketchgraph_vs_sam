import sys

sys.path.append('src/sketchgraphs/')
sys.path.append('src/sam/')

from sketchgraphs.data.sequence import EdgeOp
from sketchgraphs.data.sketch import DirectionValue
from sam.catalog_primitive import Point, Line, Circle

from sketchgraphs_vs_sam.convert.convert_constraint import SGtoExchangeConstraint

import logging
import unittest


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestConvert(unittest.TestCase):

    def test_convert_coincident(self):
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=0, references= [0,1])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[pnt_1, pnt_2])
        self.assertEqual('COINCIDENT: ref_1: Point P(0.1, 0.5)-- COINCIDENT: ref_2: Point P(0.1, 0.5)', str(ex_format))

    def test_convert_horizontal(self):
        line = Line(pnt1 = [1,0], pnt2= [2,0])
        sg_format = EdgeOp(label=4, references= [1,])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[line])
        self.assertEqual('HORIZONTAL: ref_1: Line p1=Point P(1, 0), p2=Point P(2, 0)', str(ex_format))


    def test_convert_distance(self):
        pnt_1 = Point(point = [0.0, 0.0])
        pnt_2 = Point(point = [0.4, 0.0])
        sg_format = EdgeOp(label=3, references= [0,1], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[pnt_1, pnt_2])
        self.assertEqual('DISTANCE: ref_1: Point P(0.0, 0.0), ref_2: Point P(0.4, 0.0), distance_min = 0.4', str(ex_format))


    def test_convert_length(self):
        line = Line(pnt1 = [0.,0], pnt2= [0.4,0])
        sg_format = EdgeOp(label=8, references= [2,], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[line])
        self.assertEqual('LENGTH: ref= Line p1=Point P(0.0, 0), p2=Point P(0.4, 0), length = 0.4', str(ex_format))

        line = Line(pnt1 = [0.,1.], pnt2= [0.4,10.0])
        sg_format = EdgeOp(label=8, references= [1], parameters = {'length' : 0.4, 'direction' : DirectionValue.HORIZONTAL})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[line])
        self.assertEqual('HORIZONTAL_DISTANCE: ref_1: Line p1=Point P(0.0, 1.0), p2=Point P(0.4, 10.0), distance_min = 0.4', str(ex_format))


    def test_convert_midpoint(self):
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=10, references= [0,5])
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref = [pnt_1,pnt_2])
        self.assertIsNone(ex_format)

        pnt_1 = Point(point = [0.1, 0.5])
        line =  Line(pnt1 = [0.2,0.2], pnt2= [0.3, 0.7])
        sg_format = EdgeOp(label=10, references=  [0,5])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref = [pnt_1,line])
        self.assertEqual('MIDPOINT: ref_1: Point P(0.1, 0.5), ref_2: Line p1=Point P(0.2, 0.2), p2=Point P(0.3, 0.7)', str(ex_format))

    def test_convert_radius(self):
        circle = Circle(center=[0., 5.], radius=1)
        sg_format = EdgeOp(label=14, references= [0], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref= [circle])
        self.assertEqual('RADIUS: ref= Circle: center=Point P(0.0, 5.0), radius=  1, radius = 0.4', str(ex_format))

    def test_convert_diameter(self):
        circle = Circle(center=[0., 5.], radius=1)
        sg_format = EdgeOp(label=12, references= [0], parameters = {'length' : 0.4})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref= [circle])
        self.assertEqual('RADIUS: ref= Circle: center=Point P(0.0, 5.0), radius=  1, radius = 0.2', str(ex_format))

    def test_convert_concentric(self):

        # Test 1: two circles
        circle_1 = Circle(status_construction=False, center=[0., 5.], radius=1)
        circle_2 = Circle(status_construction=False, center=[0., 5.], radius=2)
        sg_format = EdgeOp(label=15, references= [4, 18])
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref= [circle_1, circle_2])
        self.assertEqual('COINCIDENT: ref_1: Circle: center=Point P(0.0, 5.0), radius=  1-- COINCIDENT: ref_2: Circle: center=Point P(0.0, 5.0), radius=  2', str(ex_format))

        # Test 2: two points
        pnt_1 = Point(point = [0.1, 0.5])
        pnt_2 = Point(point = [0.1, 0.5])
        sg_format = EdgeOp(label=15, references= [4, 18])
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref=[pnt_1,pnt_2])
        self.assertIsNone(ex_format)

    def test_angle(self):

        # Test 1: clockwise
        line_1 = Line(pnt1 = [1,0], pnt2= [2,0])
        line_2 = Line(pnt1 = [1,0], pnt2= [2,1])
        sg_format = EdgeOp(label=17, references= [0, 1], parameters = {'angle': 45, 'clockwise' : True})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref = [line_1, line_2])
        self.assertEqual('ANGLE: ref_1: Line p1=Point P(1, 0), p2=Point P(2, 0), ref_2: Line p1=Point P(1, 0), p2=Point P(2, 1), angle = 45', str(ex_format))

        # Test 2: counter-clockwise
        sg_format = EdgeOp(label=17, references= [0, 1], parameters = {'angle': 30, 'clockwise' : False})
        logger.info(f"sg_point: {sg_format}")
        ex_format = SGtoExchangeConstraint.convert(op = sg_format, new_ref = [line_1, line_2])
        self.assertEqual('ANGLE: ref_1: Line p1=Point P(1, 0), p2=Point P(2, 0), ref_2: Line p1=Point P(1, 0), p2=Point P(2, 1), angle = -30', str(ex_format))