# this is 4-5 seconds slower on 1000000 points than Ryan's desktop...  Why?


from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal



import time
import math



class ConvexHullSolverThread(QThread):
    def __init__( self, unsorted_points,demo):
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def point_sorting(self, point):
	    print('X value: ', point.x())
	    return point.x()

    # These two signals are used for interacting with the GUI.
    show_hull    = pyqtSignal(list,tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging,
    # if you like
    show_tangent = pyqtSignal(list,tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)


    def set_points( self, unsorted_points, demo):
        self.points = unsorted_points
        self.demo   = demo

    # FROM TA explanation:
    # 1 POINT JUST Return
    # 2 link to each other, pick the higest y as the next point ??

    #For farthest left just return index zero in the graph
    #For farthest right. Loop through array find the largest X and then return that

    #call get Tanget to find upper and lower tangent *you know which points you started looking
    #to the other hull

    #PUT BACK left hull: Start at index 0, keep adding points till you get to the first point FROM
    # the top tangent,then add its couple from the other hull. (heriterate from scuh point in the other
    #hull till you get to the next point from lower bound )
    #   the add the point from the left hull from the lower bound. And keep going till you arrive to
    #   index zero from the left hull. RETUNR THAT ONE



    #before calculating tanget check if array > 1
    def calculate_tanget(self, pivot, hull, hull_farthest_point, direction):

        prev_slope = None
        current_slope = None
        found = False
        highest_point = None

        i = hull_farthest_point
        # pivot = QPointF(12, 3)
        # hull = [QPointF(4, 1),QPointF(8, 10),QPointF(7,11),QPointF(5, 9)]
        # CLOCKWISE 0:-1 1:1.16 2:1.6 3:2
        # COUNTERCLOCKWISE 0:0.25 1:-1.75 2:-1.6 3:-.85
        while not found:
            print("i to slope: ", i)
            slope = self.calculate_slope(pivot, hull[i])
            print('testing point: ', hull[i])
            print('slope value was: ', slope)
            if prev_slope is None :
                prev_slope = slope
            else :
                current_slope = slope

            if direction == "clockwise" :
                print('prev slope: ', prev_slope)
                if current_slope is not None :
                    if current_slope > prev_slope :
                        prev_slope = current_slope
                    else :
                        found = True
                        highest_point = (i-1)%len(hull) #the current point(i) we just look at is smaller therefore we want the one before


                print('New slope: ', current_slope)
                print('value of found', found)
                print('highest point: ', highest_point)
                i = (i+1)%len(hull)
                print("new values of i: ", i)

            elif direction == "counter-clockwise" :

                if current_slope is not None :
                    if current_slope < prev_slope :
                        prev_slope = current_slope
                    else :
                        found = True
                        highest_point = (i+1)%len(hull)

                i = (i-1)%len(hull)

        # return pivot, highest_point
        return highest_point


    def calculate_slope(self, left_point, right_point) :

        print()
        print('calculating slope::: ')
        print('left point: ', left_point)
        print('right point: ', right_point)
        print()
        x = left_point.x() - right_point.x()
        y = left_point.y() - right_point.y()

        if x == 0 or y == 0 :
        	return 0
        else:
        	return y/x

    def get_farthes_right (self, hull) :

        print("hull to get MAX: ", hull)
        max_x = max(hull, key=lambda p: p.x())
        index_max = hull.index(max(hull, key=lambda p: p.x()))

        print("Comming all the way here: ", max_x)
        print("Index Max: ", index_max)
        return index_max

    def append_rest_of_hull (self, hull, start_index, last_index ) :
        

    def merge ( self, left_hull, right_hull ):

        # if right_hull : print('RIGHT HULL FROM MERGE: ', right_hull)
        # if left_hull : print('LEFT_HULL FROM MERGE: ', left_hull)
        farthes_left_point_index = 0

        if len(left_hull) == 1 :
            pivot = left_hull
        else :
            pivot = self.get_farthes_right(left_hull)

        print("len left hull: ", len(left_hull) )
        print("len right hull: ", len(right_hull) )

        upper_bound_found = False
        lower_bound_found = False

        upper_right_point_found = False
        upper_left_point_found = False
        lower_right_point_found = False
        lower_left_point_found = False

        upper_right_point = None
        lower_right_point = None
        upper_left_point = None
        lower_left_point = None

        while upper_bound_found is False :
            print("while not upper bound")
            right_point = self.calculate_tanget(left_hull[pivot], right_hull, farthes_left_point_index, 'clockwise')
            left_point = self.calculate_tanget(right_hull[right_point], left_hull, pivot, 'counter-clockwise')

            if (upper_right_point is not None and (upper_right_point == right_point)): upper_right_point_found = True
            if (upper_left_point is not None and (upper_left_point == left_point)): upper_left_point_found = True

            upper_right_point = right_point
            upper_left_point = left_point

            if(upper_left_point_found is True and upper_right_point_found is True) : upper_bound_found = True

            pivot = left_point
            farthes_left_point_index = right_point

        print("upper point left: ", upper_left_point)
        print("upper point right: ", upper_right_point)

        while lower_bound_found is False :
            print("while not upper bound")
            right_point = self.calculate_tanget(left_hull[pivot], right_hull, farthes_left_point_index, 'counter-clockwise')
            left_point = self.calculate_tanget(right_hull[right_point], left_hull, pivot, 'clockwise')

            if (lower_right_point is not None and (lower_right_point == right_point)): lower_right_point_found = True
            if (lower_left_point is not None and (lower_left_point == left_point)): lower_left_point_found = True

            lower_right_point = right_point
            lower_left_point = left_point

            if(lower_left_point_found is True and lower_right_point_found is True) : lower_bound_found = True

            pivot = left_point
            farthes_left_point_index = right_point

        print("lower point left: ", lower_left_point)
        print("lower point right: ", lower_right_point)





    def find_hull( self, points ):

        # # pivot = QPointF(12, 3)
        # pivot = QPointF(2, 3)
        # hull = [QPointF(4, 1),QPointF(5, 9),QPointF(7,11),QPointF(8, 10)]
        # # highest_index = self.calculate_tanget(pivot, hull, 3, "counter-clockwise")
        # highest_index = self.calculate_tanget(pivot, hull, 0, "clockwise")
        # print("highest_index: ", highest_index);

        if len(points) == 1 :
            return points

        middle_index = math.ceil(len(points)/2)
        # print(middle_index)
        left_hull = self.find_hull(points[:middle_index])
        right_hull = self.find_hull(points[middle_index:])


        # if right_hull : print('RIGHT HULL: ', right_hull)
        # if left_hull : print('LEFT_HULL: ', left_hull)

        if(right_hull is None and left_hull is not None ) : return left_hull
        if(left_hull is None and right_hull is not None ) : return right_hull

        if (len(right_hull) == 1 and len(left_hull) == 1) : return left_hull + right_hull

        self.merge(left_hull, right_hull)



    def find_bound(self, left_hull, right_hull):
        QLineF(points[i],points[(i+1)%len(points)])


    def run(self):
        assert( type(self.points) == list and type(self.points[0]) == QPointF )

        n = len(self.points)
        print( 'Computing Hull for set of {} points'.format(n) )
        print("All the points: ", self.points)
        t1 = time.time()
        sorted_points = sorted(self.points, key=self.point_sorting)
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        hull = self.find_hull(sorted_points)
        t4 = time.time()

        polygon = [QLineF(hull[i], hull[(i+1)%len(hull)]) for i in range(len(hull))]
        self.show_hull.emit(polygon,(0,255,0))
        pass


        # Send a signal to the GUI thread with the time used to compute the
        # hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
