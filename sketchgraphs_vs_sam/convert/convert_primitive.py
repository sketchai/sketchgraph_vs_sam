from sam.catalog_primitive import Arc, Line, Circle, Point
from sketchgraphs.data.sketch import EntityType

import math

class SGtoExchangePrimitive:

    def convert(op):
        
        if op.label == EntityType.Point:
            return SGtoExchangePrimitive.convert_point(op)
        if op.label == EntityType.Arc:
            return SGtoExchangePrimitive.convert_arc(op)
        if op.label == EntityType.Circle:
            return SGtoExchangePrimitive.convert_circle(op)
        if op.label == EntityType.Line:
            return SGtoExchangePrimitive.convert_line(op)
        return None
    
    def convert_point(op):
        parms = op.parameters
        return Point(status_construction=parms.get('isConstruction'), point = [parms.get('x'), parms.get('y')])

    def convert_line(op):
        parms = op.parameters
        # Formule SG
        pnt1 = [parms.get('pntX') + parms.get('startParam') * parms.get('dirX'), 
                parms.get('pntY') + parms.get('startParam') * parms.get('dirY')]
        pnt2 = [parms.get('pntX') + parms.get('endParam') * parms.get('dirX'), 
                parms.get('pntY') + parms.get('endParam') * parms.get('dirY')]
        return Line(status_construction=parms.get('isConstruction'), pnt1=pnt1, pnt2=pnt2)

    def convert_circle(op):
        parms = op.parameters
        
        return Circle(status_construction=parms.get('isConstruction'), 
                        center = [parms.get('xCenter'), parms.get('yCenter')],
                        radius= parms.get('radius'))

    def convert_arc(op):
        parms = op.parameters
        
        angle = math.atan2(parms.get('yDir'), parms.get('xDir')) * 180 / math.pi # angle de reference
        startParam = parms.get('startParam') * 180 / math.pi # angle debut
        endParam = parms.get('endParam') * 180 / math.pi # angle fin

        if parms.get('clockwise'):
            startParam, endParam = -endParam, -startParam

        start_angle = angle + startParam
        end_angle = angle + endParam
        arc = Arc(status_construction=parms.get('isConstruction'), 
                        center = [parms.get('xCenter'), parms.get('yCenter')],
                        radius= parms.get('radius'),
                        angles= [start_angle, end_angle])
        arc.add_points_startend()
        return arc