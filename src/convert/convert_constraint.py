import math

from src.sketch_data.sketch_data.catalog_constraint import *
from src.sketch_data.sketch_data.catalog_primitive import Arc, Line, Circle, Point
from sketchgraphs.data.sketch import ConstraintType, DirectionValue
from sketchgraphs.data.sketch import EntityType

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

GEOMETRIC_CONSTRAINTS = {
    ConstraintType.Coincident : Coincident,
    ConstraintType.Horizontal : Horizontal,
    ConstraintType.Parallel : Parallel,
    ConstraintType.Vertical : Vertical,
    ConstraintType.Perpendicular : Perpendicular,
    ConstraintType.Tangent : Tangent, 
    ConstraintType.Equal : Equal,
}

class SGtoExchangeConstraint:

    def convert(op):
        
        # Check for geometric constraints
        if op.label in GEOMETRIC_CONSTRAINTS.keys():
            return GEOMETRIC_CONSTRAINTS[op.label](references = op.references)

        if op.label == ConstraintType.Distance:
            return SGtoExchangeConstraint.convert_distance(op)

        if op.label == ConstraintType.Length:
            return SGtoExchangeConstraint.convert_length(op)

        if op.label == ConstraintType.Midpoint:
            return SGtoExchangeConstraint.convert_midpoint(op)

        if op.label == ConstraintType.Diameter:
            return SGtoExchangeConstraint.convert_diameter(op)

        if op.label == ConstraintType.Radius:
            return SGtoExchangeConstraint.convert_radius(op)

        if op.label == ConstraintType.Concentric:
            return SGtoExchangeConstraint.convert_concentric(op)

        if op.label == ConstraintType.Angle:
            return SGtoExchangeConstraint.convert_angle(op)
        
        if op.label == ConstraintType.Subnode :
            return 'is_subnode'

        return None

    def convert_distance(op):
        d = op.parameters.get('length')
        return Distance(references= op.references, distance_min= d)

    def convert_length(op):
        direction = op.parameters.get('direction')
        if direction == DirectionValue.HORIZONTAL:
            return HorizontalLength(references= op.references, length= op.parameters.get('length'))
        else :
            return Length(references= op.references, length= op.parameters.get('length'))

    def convert_midpoint(op):
        references = op.references 
        opt_1 = isinstance(references[0], Point) and isinstance(references[1], Line)
        opt_2 = isinstance(references[0], Line) and isinstance(references[1], Point)
        if opt_1 or opt_2 :
            return Midpoint(references= op.references)
        else :
            return None

    def convert_diameter(op):
        return Radius(references=op.references, radius= op.parameters.get('length')/2.)

    def convert_radius(op):
        return Radius(references=op.references, radius= op.parameters.get('length'))

    def convert_concentric(op):
        references = op.references 
        if isinstance(references[0], Circle) and isinstance(references[1], Circle):
            return Coincident(references= op.references)
        else :
            return None

    def convert_angle(op):
        if op.parameters.get('clockwise') :
            return Angle(references=op.references, angle =  op.parameters.get('angle')) 
        else :
            return Angle(references=op.references, angle = - op.parameters.get('angle')) 
