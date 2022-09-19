from turtle import distance
from sam.catalog_constraint import *
from sam.catalog_primitive import Arc, Line, Circle, Point
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

    def convert(op, new_ref):
        
        # Check for geometric constraints
        if op.label in GEOMETRIC_CONSTRAINTS.keys():
            return GEOMETRIC_CONSTRAINTS[op.label](references = new_ref)

        if op.label == ConstraintType.Distance:
            return SGtoExchangeConstraint.convert_distance(op, new_ref)

        if op.label == ConstraintType.Length:
            return SGtoExchangeConstraint.convert_length(op, new_ref)

        if op.label == ConstraintType.Midpoint:
            return SGtoExchangeConstraint.convert_midpoint(op, new_ref)

        if op.label == ConstraintType.Diameter:
            return SGtoExchangeConstraint.convert_diameter(op, new_ref)

        if op.label == ConstraintType.Radius:
            return SGtoExchangeConstraint.convert_radius(op, new_ref)

        if op.label == ConstraintType.Concentric:
            return SGtoExchangeConstraint.convert_concentric(op, new_ref)

        if op.label == ConstraintType.Angle:
            return SGtoExchangeConstraint.convert_angle(op, new_ref)
        

        return None

    def convert_distance(op, new_ref):
        d = op.parameters.get('length')
        return Distance(references= new_ref, distance_min= d)

    def convert_length(op,new_ref):
        direction = op.parameters.get('direction')
        if direction == DirectionValue.HORIZONTAL:
            return HorizontalDistance(references= new_ref, distance_min= op.parameters.get('length'))
        else :
            return Length(references= new_ref, length= op.parameters.get('length'))

    def convert_midpoint(op, new_ref):
        opt_1 = isinstance(new_ref[0], Point) and isinstance(new_ref[1], Line)
        opt_2 = isinstance(new_ref[0], Line) and isinstance(new_ref[1], Point)

       
        if opt_1 or opt_2 :
            return Midpoint(references= new_ref)
        else :
            return None

    def convert_diameter(op, new_ref):
        return Radius(references=new_ref, radius= op.parameters.get('length')/2.)

    def convert_radius(op, new_ref):
        return Radius(references=new_ref, radius= op.parameters.get('length'))

    def convert_concentric(op, new_ref):
        if isinstance(new_ref[0], Circle) and isinstance(new_ref[1], Circle):
            return Coincident(references= new_ref)
        else :
            return None

    def convert_angle(op, new_ref):
        if op.parameters.get('clockwise') :
            return Angle(references=new_ref, angle =  op.parameters.get('angle')) 
        else :
            return Angle(references=new_ref, angle = - op.parameters.get('angle')) 
