from math import floor
from manim import *

class CircleArea(Scene):
    

    ringColor = BLUE
    ringOpacity = .4

    def construct(self):
        strokeColor = BLACK
        strokeWidth = 0
        
        def createRect(ring : VGroup, extended, returnCorner, color):
            gap = ring[0].radius - ring[1].radius
            rectLeftBottom = ring[0].point_at_angle(1.5 * PI);
            rectLeftTop = rectLeftBottom.copy()
            rectLeftTop[1] = rectLeftTop[1] + gap
            rectRightTop = rectLeftTop
            rectRightBottom = rectLeftBottom
            if extended:
                rectRightBottom = rectLeftBottom.copy()
                rectRightTop = rectLeftTop.copy()
                rectRightTop[0] += ring[0].radius * 2 * PI
                rectRightBottom[0] += ring[0].radius * 2 * PI
                rectRightTop[0] -= PI * gap
                rectLeftTop[0] += PI * gap

            
            rectangle = Polygon(rectLeftBottom, rectLeftTop, rectRightTop, rectRightBottom)
            rectangle.set_stroke(width=0)
            rectangle.set_fill(color = color, opacity= 1)

            if returnCorner:
                return rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom
            return rectangle

        def createRing(center, innerRadius, gap, color):
            ring = Circle(radius=innerRadius + gap)
            ring.set_stroke(strokeColor, strokeWidth)
            ring.move_to(center)
            ring.set_fill(self.ringColor, self.ringOpacity)
            ring.set_fill(color, opacity=1)
            innerRing = Circle(innerRadius)
            innerRing.move_to(center)
            innerRing.set_fill(BLACK, 1)
            innerRing.set_stroke(strokeColor, strokeWidth)
            return VGroup(ring, innerRing)


        center = ORIGIN

        x = ValueTracker(0)
        
        def setRing(radius, zIndex, gap, color, time):
            
            ring = createRing(center, radius, gap, color)
            self.play(FadeIn(ring), run_time = time)

            def createConveringArc(center, angle, side):
                startAngle = 1.5 * PI
                arc = None
                if side == 'LEFT':
                    arc = Arc(
                        radius + gap,startAngle,-angle, arc_center = center
                        )
                else:
                    arc = Arc(
                        radius + gap,.5 * PI,-(angle - PI), arc_center = center
                        )
                
                triangle = Polygon(
                    center, arc.get_start(), arc.get_end(),stroke_width = 0
                    )

                arc.set_fill(BLACK, 1)
                triangle.set_fill(BLACK, 1)
                arc.set_stroke(strokeColor, width=strokeWidth)
                triangle.set_stroke(strokeColor, strokeWidth)
                arcGroup = VGroup(arc, triangle)

                return arcGroup
            
            leftArcGroup = createConveringArc(center, 0, 'LEFT')
            rightArcGroup = createConveringArc(center, PI, 'RIGHT')
            self.add(leftArcGroup)
            self.add(rightArcGroup)

            def getNewCenterRadius():
                rotationAngle = x.get_value()
                distance = rotationAngle * (radius + gap)
                newCenter = center.copy()
                newCenter[0] += distance
                return rotationAngle, distance, newCenter

            def ringUpdater(r):
                _, _, newCenter = getNewCenterRadius()
                nRing = createRing(newCenter, radius, gap, color)
                r.become(nRing)

            def leftUpdater(lft):
                rotationAngle, distance, newCenter = getNewCenterRadius()
                if rotationAngle > PI:
                    rotationAngle = PI
                newArc = createConveringArc(newCenter, rotationAngle, 'LEFT')
                lft.become(newArc)

            def rightUpdater(rt):
                rotationAngle, distance, newCenter = getNewCenterRadius()
                if rotationAngle < PI:
                    return
                newArc = createConveringArc(newCenter, rotationAngle, 'RIGHT')
                rt.become(newArc)

            ring.add_updater(ringUpdater)
            leftArcGroup.add_updater(leftUpdater)
            rightArcGroup.add_updater(rightUpdater)

            triangle = Polygon(center, center, center)
            self.add(triangle)

            def triangleUpdater(tr):
                rotationAngle, distance, newCenter = getNewCenterRadius()
                if radius == 0 and rotationAngle < PI: 
                    return
                distort = (rotationAngle / (2 * PI)) * PI * gap
                distortAngle = distort / radius
                laggingAngle = rotationAngle + distortAngle
                if rotationAngle < 1.5 * PI:
                    rotationAngle = 1.5 * PI - rotationAngle
                else:
                    rotationAngle = 2*PI - rotationAngle + 1.5 * PI

                rt = laggingAngle > 2 * PI
                if laggingAngle < 1.5 * PI:
                    laggingAngle = 1.5 * PI - laggingAngle
                else:
                    laggingAngle = 2*PI - laggingAngle + 1.5 * PI
                
                p1 = ring[0].point_at_angle(rotationAngle)
                p2 = ring[1].point_at_angle(rotationAngle)
                p3 = ring[1].point_at_angle(max(0, laggingAngle))
                if rt:
                    newCenter = center + (radius + gap) * DOWN
                    newCenter[0] += 2 * PI * (radius + gap)
                    newCenter[0] -= PI * gap
                    newCenter[1] += gap
                    p3 = newCenter
                nTriangle = Polygon(p1, p2, p3)
                # nTriangle.set_z_index(20)
                nTriangle.set_fill(BLACK, opacity=1)
                nTriangle.set_stroke(strokeColor, strokeWidth)
                tr.become(nTriangle)
                tr.set_z_index(20)
                
        
            triangle.add_updater(triangleUpdater)

            rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom = createRect(ring, False, True, color)
            self.add(rectangle)
            

            def rectUpdater(rect):
                rotationAngle, distance, newCenter = getNewCenterRadius()
                extra = (rotationAngle / (2 * PI)) * PI * gap
                RLT = rectLeftTop.copy()
                RLT[0] += extra
                rectRightTop = rectLeftTop.copy()
                rectRightBottom = rectLeftBottom.copy()
                rectRightBottom[0] = rectRightTop[0] = rectRightBottom[0] + distance
            
                rectangle = Polygon(rectLeftBottom, RLT, rectRightTop, rectRightBottom)
                rectangle.set_stroke(width=0)
                rectangle.set_fill(color, 1)
                rect.become(rectangle)
                rect.set_z_index(10)
            
            rectangle.add_updater(rectUpdater)

            return ring, leftArcGroup, rightArcGroup, rectangle, triangle, ringUpdater, leftUpdater, rightUpdater, rectUpdater, triangleUpdater
            

        # radius = 1
        # gap = .2

        count = 60
        colors = color_gradient([BLUE, GREEN], length_of_output=count)
        gap = 1 / count
        ringGr = VGroup()
        arcGr = VGroup()
        ringUpdaters = []
        arcUpdaters = []
        rectangles = VGroup()
        triangles = VGroup()
        rectangleUpdaters = []
        triangleUpdaters = []
        tmpRings = []
        for i in range(count):
            ringRadius = 1 - (i + 1) * gap
            ring, leftArcGroup, rightArcGroup, rectangle, triangle,\
            ringUpdater, leftUpdater, rightUpdater,\
            rectUpdater, triangleUpdater = setRing(ringRadius, i + 1, gap, colors[i] , 1 / count)
            tmpRings.append(createRing(center,ringRadius, gap, colors[i]))
            ringGr.add(ring)
            ringUpdaters.append(ringUpdater)
            arcUpdaters.append(leftUpdater)
            arcUpdaters.append(ringUpdater)
            arcGr.add(leftArcGroup, rightArcGroup)
            rectangles.add(rectangle)
            triangles.add(triangle)
            rectangleUpdaters.append(rectUpdater)
            triangleUpdaters.append(triangleUpdater)
            # ringGr.add(r)


        # setRing(radius, 1, gap, BLUE, 1)
        self.play(x.animate.set_value(2 * PI), run_time = 2)
        # for index, item in enumerate(ringGr):
        #     item.remove_updater(ringUpdaters[i])
        
        # i = 0
        # for j in arcGr:
        #     j.remove_updater(arcUpdaters[i])
        #     i += 1
        # self.remove(ringGr, arcGr, triangles)
        # self.wait(1)

        newRects = []

        for index, item in enumerate(rectangles):
            rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom \
                = createRect(tmpRings[index], True, True, colors[index])

            item.remove_updater(rectangleUpdaters[index])
            item.become(rectangle)

            r0 = tmpRings[0][0].radius
            r = tmpRings[index][0].radius
            delta = PI * (r0 - r)
            rectLeftBottom[0] += delta
            rectLeftTop[0] += delta
            rectRightBottom[0] += delta
            rectRightTop[0] += delta
            
            rectangle = Polygon(rectLeftBottom, rectLeftTop, rectRightTop, rectRightBottom)
            rectangle.set_stroke(width=0)
            rectangle.set_fill(color = colors[index], opacity= 1)

            self.remove(triangles[index])
            newRects.append(rectangle)
            # self.play(item.animate.become(rectangle))
        
        self.play( *[item.animate.become(newRects[i]) for i, item in enumerate(rectangles)])
        
        arr = []
        

        # for i in rectangles:
        #     self.play(FadeOut(i))
        self.wait(1)

            
            
