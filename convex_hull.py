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
            print('PIVOT to calculate tanget: ', pivot)
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
                # print("new values of i: ", i)

            elif direction == "counter-clockwise" :

                if current_slope is not None :
                    if current_slope < prev_slope :
                        prev_slope = current_slope
                    else :
                        found = True
                        highest_point = (i+1)%len(hull)

                i = (i-1)%len(hull)

        # # return pivot, highest_point
        print ("highest point index: ", highest_point)
        print("ACTUAL POINT: ", hull[highest_point])
        print("At direction ",direction)
        print("@@@ SLOPE FOUND @@@\n")
        return highest_point


    def calculate_slope(self, left_point, right_point) :

        # print()
        # print('calculating slope::: ')
        # print('left point: ', left_point)
        # print('right point: ', right_point)
        # print()
        x = left_point.x() - right_point.x()
        y = left_point.y() - right_point.y()

        if x == 0 or y == 0 :
        	return 0
        else:
        	return y/x

    def get_farthes_right (self, hull) :

        # print("hull to get MAX: ", hull)
        max_x = max(hull, key=lambda p: p.x())
        index_max = hull.index(max(hull, key=lambda p: p.x()))

        # print("Comming all the way here: ", max_x)
        # print("Index Max: ", index_max)
        return index_max

    def append_rest_of_hull (self, hull, start_index, last_index ) :

        # if len(hull) == 2 : return hull
        # if hull[start_index] == hull[last_index] : return []

        point_list = []
        print("HULL appending: ", hull)
        print("Start Index from appending: ", start_index)
        print("Last Index from appending: ", last_index)

        for i, points in enumerate(hull, start=start_index):

            # if len(hull) == 2 and start_index != 0:
            #     print("Comming here: ", hull[start_index])
            #     point_list.append(hull[start_index])
            #     break

            if (start_index == last_index):
                point_list.append(hull[i%len(hull)])
                break

            point_list.append(hull[i%len(hull)])
            if i == last_index : break


        print("Point list to return from appending: ", point_list)
        return point_list

    def merge ( self, left_hull, right_hull ):

        if right_hull : print('RIGHT HULL FROM MERGE: ', right_hull)
        if left_hull : print('LEFT_HULL FROM MERGE: ', left_hull)
        farthes_left_point_index = 0
        index_zero_left_hull = 0

        if len(left_hull) == 1 :
            pivot = left_hull
        else :
            farthest_right = self.get_farthes_right(left_hull)
            pivot = farthest_right

        # print("len left hull: ", len(left_hull) )
        # print("len right hull: ", len(right_hull) )
        print("pivot for left hull: ", pivot)

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

            right_point = self.calculate_tanget(left_hull[pivot], right_hull, farthes_left_point_index, 'clockwise')
            left_point = self.calculate_tanget(right_hull[right_point], left_hull, pivot, 'counter-clockwise')

            if (upper_right_point is not None and (upper_right_point == right_point)): upper_right_point_found = True
            if (upper_left_point is not None and (upper_left_point == left_point)): upper_left_point_found = True

            upper_right_point = right_point
            upper_left_point = left_point

            print("upper_right_point so far: ", upper_right_point)
            print("upper_left_point so far: ", upper_left_point)

            print("Has it found upper RIGHT?? ",upper_right_point_found)
            print("Has it found upper LEFT?? ",upper_right_point_found)

            if(upper_left_point_found is True and upper_right_point_found is True) : upper_bound_found = True

            # pivot = left_point
            pivot = farthest_right
            farthes_left_point_index = right_point

            print("Set the pivot to: ", pivot)
            print("Farthest left point to: ", farthes_left_point_index)

        if (upper_bound_found == True) : print("======= FOUND UPPER BOUND EXITING ===L", left_hull[upper_left_point])
        if (upper_bound_found == True) : print("======= FOUND UPPER BOUND EXITING ===R", right_hull[upper_right_point])

        while lower_bound_found is False :

            right_point = self.calculate_tanget(left_hull[pivot], right_hull, farthes_left_point_index, 'counter-clockwise')
            left_point = self.calculate_tanget(right_hull[right_point], left_hull, pivot, 'clockwise')

            if (lower_right_point is not None and (lower_right_point == right_point)): lower_right_point_found = True
            if (lower_left_point is not None and (lower_left_point == left_point)): lower_left_point_found = True

            lower_right_point = right_point
            lower_left_point = left_point

            # print("lower_right_point so far: ", lower_right_point)
            # print("lower_left_point so far: ", lower_left_point)
            #
            # print("Has it found lower RIGHT?? ",lower_right_point_found)
            # print("Has it found lower LEFT?? ",lower_right_point_found)

            if(lower_left_point_found is True and lower_right_point_found is True) : lower_bound_found = True

            pivot = left_point
            farthes_left_point_index = right_point

            # print("Set the L pivot to: ", pivot)
            # print("Farthest left point to: ", farthes_left_point_index)

        if (lower_bound_found == True) : print("======= FOUND LOWER BOUND EXITING ===L", left_hull[lower_left_point])
        if (lower_bound_found == True) : print("======= FOUND LOWER BOUND EXITING ===R", right_hull[lower_right_point])




        # if ((upper_left_point == lower_left_point) and upper_left_point == index_zero_left_hull) :
        #     print("gonna return here-->>>")
        #     print("right hull: ", right_hull)
        #     return [left_hull[upper_left_point]] + self.append_rest_of_hull(right_hull, upper_right_point, lower_right_point) + [right_hull[lower_right_point]]
        #
        # if ((upper_right_point == lower_right_point) and upper_right_point == index_zero_left_hull) :
        #     print("gonna return here--<<<<<<<<")
        #     return [right_hull[upper_right_point]] + self.append_rest_of_hull(left_hull, upper_left_point, lower_left_point) + [left_hull[lower_left_point]]

        # new_hull = self.append_rest_of_hull(left_hull, index_zero_left_hull, upper_left_point) + [left_hull[upper_left_point]] + self.append_rest_of_hull(right_hull, upper_right_point, lower_right_point) + [right_hull[lower_right_point]] + self.append_rest_of_hull(left_hull, lower_left_point, len(left_hull))


        # points_to_erase_left_hull = left_hull[upper_left_point:lower_left_point]
        # # print("points to delete, left: ", points_to_erase_left_hull)
        # print()
        # print("Right hull: ", right_hull)
        # print("UPPER RIGZHT POINT INDEX: ",upper_right_point)
        # print("LOWER RIGZHT POINT INDEX: ",lower_right_point)
        # if (upper_right_point > lower_right_point):
        #     points_to_erase_right_hull = right_hull[lower_right_point : upper_right_point]
        # else :
        #     points_to_erase_right_hull = right_hull[upper_right_point:lower_right_point]
        # # print("points to delete, right: ", points_to_erase_right_hull)

        # self.erase_tangent.emit(points_to_erase_left_hull)
        # self.erase_tangent.emit(points_to_erase_right_hull)
        # print("left_hull: ", left_hull)
        # print("right hull: ", right_hull)
        # if len(left_hull) == 2 and len(right_hull) == 1 :
        #     new_hull = self.append_rest_of_hull(left_hull, index_zero_left_hull, upper_left_point) + self.append_rest_of_hull(right_hull, index_zero_left_hull, 0)
        # # if lower_right_point != 0:
        # else :
        new_hull = self.append_rest_of_hull(left_hull, index_zero_left_hull, upper_left_point) + self.append_rest_of_hull(right_hull, upper_right_point, lower_right_point) + self.append_rest_of_hull(left_hull, lower_left_point, len(left_hull)-1)
        # else :
        #     new_hull = self.append_rest_of_hull(left_hull, index_zero_left_hull, upper_left_point) + self.append_rest_of_hull(right_hull, upper_right_point, lower_right_point)
        print("New hull just formed", new_hull)
        print()
        # return (new_hull, points_to_erase_left_hull, points_to_erase_right_hull)
        return new_hull


    def find_hull( self, points ):

        if len(points) == 1 :
            # return (points, None, None)
            return points

        middle_index = math.ceil(len(points)/2)

        # (left_hull, erase_from_left_lhull, erase_from_right_lhull) = self.find_hull(points[:middle_index])
        # (right_hull, erase_from_left_rhull, erase_from_right_rhull) = self.find_hull(points[middle_index:])
        left_hull = self.find_hull(points[:middle_index])
        right_hull = self.find_hull(points[middle_index:])

        # if left_hull : print('LEFT_HULL: ', left_hull)
        # if right_hull : print('RIGHT HULL: ', right_hull)
        print()




        l_polygon = [QLineF(left_hull[i], left_hull[(i+1)%len(left_hull)]) for i in range(len(left_hull))]
        self.show_hull.emit(l_polygon,(0,255,0))
        r_polygon = [QLineF(right_hull[i], right_hull[(i+1)%len(right_hull)]) for i in range(len(right_hull))]
        self.show_hull.emit(r_polygon,(0,255,0))

        # if erase_from_left_lhull is not None : self.erase_tangent.emit(erase_from_left_lhull)
        # if erase_from_right_lhull is not None : self.erase_tangent.emit(erase_from_right_lhull)
        # if erase_from_left_rhull is not None : self.erase_tangent.emit(erase_from_left_rhull)
        # if erase_from_right_rhull is not None : self.erase_tangent.emit(erase_from_right_rhull)

        if(right_hull is None and left_hull is not None ) :
            print("Gonna return one xuz right hull was null")
            # return (left_hull, None, None)
            return left_hull
        if(left_hull is None and right_hull is not None ) :
            print("Gonna return one xuz left hull was null")
            # return (right_hull, None, None)
            return right_hull


        # if (len(right_hull) == 1 and len(left_hull) == 1) : return (left_hull + right_hull, None, None)
        if (len(right_hull) == 1 and len(left_hull) == 1) : return left_hull + right_hull

        return self.merge(left_hull, right_hull)



    def find_bound(self, left_hull, right_hull):
        QLineF(points[i],points[(i+1)%len(points)])


    def run(self):
        assert( type(self.points) == list and type(self.points[0]) == QPointF )
        # self.points =  [QPointF(15, 3),QPointF(3, 5),QPointF(1,2),QPointF(18, 19)]
        # self.points = [QPointF(3, 10),QPointF(1, 2),QPointF(4,5),QPointF(12, 15),QPointF(10, 4),QPointF(15, 7)]
        # self.points = [QPointF(-0.43632431120059234, 0.5116084083144479), QPointF(-0.15885683833831, -0.4821664994140733),QPointF(-0.04680609169528838, 0.1667640789100624), QPointF(0.02254944273721704, -0.19013172509917142)]

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
        print("Last polygon: ", hull)
        self.show_hull.emit(polygon,(0,255,0))
        pass


        # Send a signal to the GUI thread with the time used to compute the
        # hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
