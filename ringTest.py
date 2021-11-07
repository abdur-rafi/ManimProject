from math import floor
from manim import *

class CircleArea(Scene):
    

    ringColor = BLUE
    ringOpacity = .4




    def construct(self):

        strokeColor = BLACK
        strokeWidth = .1

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
       
        
        def createConveringArc(angle,side, radius, center):
            startAngle = .5 * PI
            arc = None
            if side == 'LEFT':
                arc = Arc(radius,startAngle,angle, arc_center=center)
            else:
                arc = Arc(radius,.5 * PI,-angle, arc_center=center)
            triangle = Polygon(center, arc.get_start(), arc.get_end())
            fill = ORANGE
            fill = BLACK
            arc.set_fill(fill, 1)
            triangle.set_fill(fill, 1)
            arc.set_stroke(strokeColor, width=strokeWidth)
            triangle.set_stroke(strokeColor, width=strokeWidth)
            arcGroup = VGroup(arc, triangle)
            return arcGroup

        # self.circle = Circle(1, color = WHITE)
        # self.play(Create(self.circle))

        center = ORIGIN
        x = ValueTracker(0)
        mid = 20
        end = 500
        
        def setRing(radius, zIndex, gap, color, time):
            
            oldInnerRadius = radius
            oldOuterRadius = oldInnerRadius + gap

            ring = createRing(ORIGIN, oldInnerRadius, gap, color)
            ring.set_z_index(zIndex)

            leftCoveringArc = createConveringArc(0, 'LEFT',oldOuterRadius,center )
            rightCoveringArc = createConveringArc(0, 'RIGHT',oldOuterRadius,center )
            leftCoveringArc.set_z_index(zIndex)
            rightCoveringArc.set_z_index(zIndex)
            
            leftTr = Polygon(center, center, center)
            leftTr.set_z_index(zIndex)
            leftTr.set_stroke(color, width=0)
            leftTr.set_fill(BLACK, 1)


            rightTr = Polygon(center, center, center)
            rightTr.set_z_index(zIndex)
            rightTr.set_stroke(color,width=0)
            rightTr.set_fill(BLACK, 1)

            
            self.play(FadeIn(ring), run_time = time)
            self.add(leftCoveringArc, rightCoveringArc, leftTr, rightTr)

            def updater(r):
                newRadius = x.get_value() + oldInnerRadius
                newCenter = center + x.get_value() * UP
                newRing = createRing(newCenter, newRadius, gap, color)
                r.become(newRing)

            ring.add_updater(updater)

            def createArchUpdater(side):
                def updater(arc):
                    newRadius = x.get_value() + oldInnerRadius
                    newCenter = center + x.get_value() * UP
                    bottomAngle = (PI * oldOuterRadius) / (newRadius + gap)
                    bottomAngle = PI - bottomAngle
                    nArc = createConveringArc(bottomAngle, side, newRadius + gap, newCenter)
                    arc.become(nArc)
                return updater

            def createTrUpdater(side):
                def triangleUpdater(tr):
                    newRadius = x.get_value() + oldInnerRadius
                    newCenter = center + x.get_value() * UP
                    outerAngle = (PI * oldOuterRadius) / (newRadius + gap)
                    innerAngle = outerAngle
                    if newRadius != 0:
                        innerAngle =  (PI * oldInnerRadius) / (newRadius)
                    
                    if side == 'LEFT':
                        outerAngle = 1.5 * PI - outerAngle
                        innerAngle = 1.5 * PI - innerAngle
                    else:
                        outerAngle = PI - outerAngle
                        innerAngle = PI - innerAngle
                        def between(angle):
                            if angle > .5 * PI:
                                return PI - angle + 1.5 * PI
                            else:
                                return .5 * PI - angle

                        outerAngle = between(outerAngle)
                        innerAngle = between(innerAngle)
                        
                    p1 = ring[0].point_at_angle(outerAngle)
                    p2 = ring[1].point_at_angle(outerAngle)
                    p3 = ring[1].point_at_angle(innerAngle)
                    nTr = Polygon(p1, p2, p3)
                    nTr.set_stroke(width=0)
                    nTr.set_fill(BLACK, 1)
                    tr.become(nTr)
                return triangleUpdater
                
            leftTrUpdater = createTrUpdater('LEFT')
            rightTrUpdater = createTrUpdater('RIGHT')
            
            leftTr.add_updater(leftTrUpdater)
            rightTr.add_updater(rightTrUpdater)

            leftArcUpdater = createArchUpdater('LEFT')
            rightArcUpdater = createArchUpdater('RIGHT')

            leftCoveringArc.add_updater(leftArcUpdater)
            rightCoveringArc.add_updater(rightArcUpdater)
            return ring

        count = 10
        colors = color_gradient([BLUE, GREEN], length_of_output=count)
        gap = 1 / count
        ringGr = VGroup()
        for i in range(count):
            r = setRing(1 - (i + 1) * gap, i + 1, gap, colors[i] , 1 / count)
            ringGr.add(r)

        # self.play(Create(ringGr))

        self.play(x.animate.set_value(mid), run_time = 2)
        self.play(x.animate.set_value(end), run_time = 1)

        
