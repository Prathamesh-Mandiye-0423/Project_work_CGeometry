from typing import List, Tuple

def distance(p1: Tuple[float,float], p2: Tuple[float,float])->float:
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(0.5)

def point_in_rect(point: Tuple[float,float], rect: Tuple[float,float,float,float])-> bool:
    x,y,w,h=rect
    px,py=point
    return x<=px<=x+w and y<=py<=y+h