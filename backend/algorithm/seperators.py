from typing import  List, Tuple, Dict, Optional
from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float

    class Config:
        frozen= True
        #frozen makes the model immutable and hashable

class Rectangle:
    def __init__(self,x:float,y:float,width:float,height:float):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def contains(self, point:Point)->bool:
        return (self.x <= point.x <= self.x + self.width) and (self.y <= point.y <= self.y + self.height)
    # Converts the rect to dict
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }


#Implementing the logic for rectangle seperator
# PRoblem statement 6.1
# TC: O(m+n) with O(mlogm+nlogn) preprocessing
# SC O(m+n)

class RectangleSeperator:
    def __init__(self,red_points:List[Point],blue_points:List[Point]):
        self.red_points=red_points
        self.blue_points=blue_points

    def find_bounding_rect(self,points:List[Point])->Optional[Tuple[float,float,float,float]]:
        if not points:
            return None
        min_x=min(p.x for p in points)
        max_x=max(p.x for p in points)
        min_y=min(p.y for p in points)
        max_y=max(p.y for p in points)
        return (min_x,max_x,min_y,max_y)

    def count_blue_in_rect(self,rect:Rectangle)->int:
        count=0
        for bp in self.blue_points:
            if rect.contains(bp):
                count+=1
        return count
    
    def solve(self)->Dict:
        if not self.red_points:
            return {'rectangles':[], 'blue_covered': 0, 'red_covered': 0}
        best_rects=None
        min_blue_count=float('inf')
        # First veertical sweep line
        red_sorted_y=sorted(self.red_points,key=lambda p:p.y)
        for i in range(len(red_sorted_y)-1):
            split_y=(red_sorted_y[i].y + red_sorted_y[i+1].y)/2
            # Get red points above and below the split
            lower_red=[p for p in self.red_points if p.y <= split_y]
            upper_red=[p for p in self.red_points if p.y > split_y]
            if not lower_red or upper_red:
                continue
            lower_bounds=(self.find_bounding_rect(lower_red))
            upper_bounds=(self.find_bounding_rect(upper_red))

            rect1=Rectangle(
                lower_bounds[0],
                lower_bounds[2],
                lower_bounds[1]-lower_bounds[0],
                lower_bounds[3]-lower_bounds[2]
                # add some buffer if required
            )

            rect2=Rectangle(
                upper_bounds[0],
                upper_bounds[2],
                upper_bounds[1]-upper_bounds[0],
                upper_bounds[3]-upper_bounds[2]
                # add some buffer if required
            )
            blue_count=self.count_blue_in_rect(rect1)+
                self.count_blue_in_rect(rect2)
            if blue_count < min_blue_count:
                min_blue_count=blue_count
                best_rects=(rect1,rect2)
            
            #Vertical Line Sweep
        red_sorted_x=sorted(self.red_points,key=lambda p:p.x)
        for i in range(len(red_sorted_x)-1):
            split_x=(red_sorted_x[i].x + red_sorted_x[i+1].x)/2
            left_red=[p for p in self.red_points if p.x <= split_x]
            right_red=[p for p in self.red_points if p.x > split_x]
            if not left_red or not right_red:
                continue
            left_bounds=self.find_bounding_rect(left_red)
            right_bounds=self.find_bounding_rect(right_red)

            rect1=Rectangle(
                left_bounds[0],
                left_bounds[2],
                left_bounds[1]-left_bounds[0],
                left_bounds[3]-left_bounds[2]
            )

            rect2=Rectangle(
                right_bounds[0],
                right_bounds[2],
                right_bounds[1]-right_bounds[0],
                right_bounds[3]-right_bounds[2]
            )

            blue_count=self.count_blue_in_rect(rect1)+
                self.count_blue_in_rect(rect2)
            if blue_count < min_blue_count:
                min_blue_count=blue_count
                best_rects=(rect1,rect2)
        return {
            'rectangles': [r.to_ddict() for r in best_rects] if best_rects else [],
            'blue_covered': int(min_blue_count) if min_blue_count!=float('inf') else 0,
            'red_covered': len(self.red_points)
        }

#Implements the logic for Square Sperator
# TC : O(n*m) with O(mlogm + nlogn) preprocessing
# SC O(m+n)
class SquareSeperator:
    def __init__(self,red_points:List[Point],blue_points:List[Point]):
        self.red_points=red_points
        self.blue_points=blue_points
    def find_bouding_square(self,points:List[Point])->Optional[Tuple[float,float,float,float]]:
        if not points:
            return None
        min_x=min(p.x for p in points)
        max_x=max(p.x for p in points)
        min_y=min(p.y for p in points)
        max_y=max(p.y for p in points)

        return (min_x,max_x,min_y,max_y)
    
    def count_blue_in_square(self,square:Rectangle)->int:
        count=0
        for bp in self.blue_points:
            if square.contains(bp):
                count+=1
        return count
    # Find set of squares that cover all red points while minimizing blue points
    def solve(self)->Dict:
        if not self.red_points:
            return {"squares":[],"blue_covered":0,"red_coverd":0}
        
        best_squares=None
        min_blue_count=float('inf')
        red_sorted_y=sorted(self.red_points,key=lambda p:p.y)
        for i in range(len(red_sorted_y)-1):
            split_y=(red_sorted_y[i].y + red_sorted_y[i+1].y)/2
            lower_red=[p for p in self.red_points if p.y <= split_y]
            upper_red=[p for p in self.red_points if p.y > split_y]
            if not lower_red or not upper_red:
                continue
            lower_bounds=self.find_bouding_square(lower_red)
            upper_bounds=self.find_bouding_square(upper_red)

            side1=max(lower_bounds[1]-lower_bounds[0],lower_bounds[3]-lower_bounds[2])
            side2=max(upper_bounds[1]-upper_bounds[0],upper_bounds[3]-upper_bounds[2])

            square1=Rectangle(
                lower_bounds[0],
                lower_bounds[2],
                side1,
                side1
            )
            #Add buffer if required

            square2=Rectangle(
                upper_bounds[0],
                upper_bounds[2],
                side2,
                side2
            )
            # Add buffer if required
            blue_count=self.count_blue_in_square(square1)+
                self.count_blue_in_square(square2)
            if blue_count < min_blue_count:
                min_blue_count=blue_count
                best_squares=(square1,square2)
            # Vertical Line Sweep
        red_sorted_x=sorted(self.red_points,key=lambda p:p.x)
        for i in range(len(red_sorted_x)-1):
            split_x=(red_sorted_x[i].x + red_sorted_x[i+1].x)/2
            left_red=[p for p in self.red_points if p.x <= split_x]
            right_red=[p for p in self.red_points if p.x > split_x]
            if not left_red or not right_red:
                continue
            left_bounds=self.find_bouding_square(left_red)
            right_bounds=self.find_bouding_square(right_red)

            side1=max(left_bounds[1]-left_bounds[0],left_bounds[3]-left_bounds[2])
            side2=max(right_bounds[1]-right_bounds[0],right_bounds[3]-right_bounds[2])

            square1=Rectangle(
                left_bounds[0],
                left_bounds[2],
                side1,
                side1
            )

            square2=Rectangle(
                right_bounds[0],
                right_bounds[2],
                side2,
                side2
            )

            blue_count=self.count_blue_in_square(square1)+
                self.count_blue_in_square(square2)
            if blue_count < min_blue_count:
                min_blue_count=blue_count
                best_squares=(square1,square2)

        return {
            "squares":[s.to_doct for s in best_squares] if best_squares else [],
            "blue_covered": int(min_blue_count) if min_blue_count!=float('inf') else 0,
            "red_covered": len(self.red_points)
        }
# Updated and completed Algorithm Logic