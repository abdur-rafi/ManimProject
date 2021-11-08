from math import floor
from manim import *

class CircleArea(Scene):
    

    ringColor = BLUE
    ringOpacity = .4

    def slicesAnimation(self):

        def getArc(center, startAngle,angleDelta,fill_color):
            arc = Arc(self.circle.radius, startAngle,angleDelta,
            arc_center=center, stroke_width = sliceStrokeWidth)
            arc.set_fill(BLUE, .4)
            fLine = Line(center,arc.get_start(),stroke_width = sliceStrokeWidth)
            sLine = Line(center,arc.get_end(),stroke_width = sliceStrokeWidth)
            triangle = Polygon(center, arc.get_start(), arc.get_end(),stroke_width = 0)
            triangle.set_fill(BLUE, .4)
            # self.add(triangle)
            return arc, fLine, sLine, triangle

        def createSlices(n, thinSlices):
            center = RIGHT +.5 * DOWN
            angleDelta = (PI * 2) / n
            slices = []
            thinSliceWidth = 1
            arcs = []
            for i in range(floor(n / 2)):   
                arc, sLine, fLine, triangle = getArc(center,.5 * PI - angleDelta / 2,angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                if thinSlices:
                    for i in group:
                        i.set_stroke(width = thinSliceWidth)
                slices.append(group)

                center = arc.get_start()
                
                arc, sLine, fLine, triangle = getArc(center,1.5 * PI - angleDelta / 2, angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                
                if thinSlices:
                    for i in group:
                        i.set_stroke(width = thinSliceWidth)
                slices.append(group)

                center = arc.get_end()
            return slices

        def highlightSlices(slices, animateEach = True):
            highlightSlicesGroup = VGroup()
            nArcs = []
            fPoint = slices[0][0].get_end()
            ePoint = slices[len(slices) - 1][0].get_arc_center()


            angleDelta = (2 * PI) / len(slices)
            angleSum = 0
            colorArcs = VGroup()
            for i,item in enumerate(slices):
                if (i % 2 == 1):
                    continue
                arc = Arc(self.circle.radius, i * angleDelta, angleDelta, arc_center=self.circle.get_center(),color = ORANGE)
                colorArcs.add(arc)
                arc : Arc = item[0].copy()
                arc.set_fill(None, 0)
                arc.set_stroke(width=2 * sliceStrokeWidth)
                arc.set_color(ORANGE)
                nArcs.append(arc)
                # self.play(Create(arc))
            nArcs.reverse()
            arcGroups = VGroup()
            for i, item in enumerate(nArcs):
                if animateEach:
                    self.play(Create(item),Create(colorArcs[i]) , run_time = 2 / len(slices))
                arcGroups.add(item)
            if animateEach == False:
                line = Line(fPoint, ePoint, stroke_width = 2 * sliceStrokeWidth, color = ORANGE)
                self.play(Create(line), Create(colorArcs))
                arcGroups.add(line)
                # self.play(FadeIn(arcGroups))

            topBrace = Brace(arcGroups, UP)
            topBraceText = topBrace.get_tex(r"{\pi}r")
            self.play(FadeIn(topBrace), FadeIn(topBraceText))
            # self.play(arcGroups.animate.move_to(2 * DOWN))


            nArcs.reverse()


            radiusLine = Line(self.circle.point_at_angle(0), self.circle.get_center(), color = ORANGE)
            fLine = slices[0][2].copy()
            fLine.set_stroke(ORANGE, width = 2 * sliceStrokeWidth)
            self.play(Create(fLine), Create(radiusLine))

            leftBrace = Brace(fLine,  direction=fLine.copy().rotate(PI / 2).get_unit_vector())
            leftBraceText = leftBrace.get_tex(r"r")
            self.play(FadeIn(leftBrace), FadeIn(leftBraceText))
            
            highlightSlicesGroup.add(arcGroups,fLine, leftBrace, leftBraceText, topBrace, topBraceText, colorArcs, radiusLine)

            return highlightSlicesGroup

            # center = nArcs[0].get_center()


            # angleDelta = (2 * PI) / len(slices)
            # for i, item in enumerate(nArcs):
            #     arc = item 
            #     self.play(arc.animate.move_to(center))
            #     self.play(arc.animate.rotate(-i * angleDelta))
            # arc,_,_,_ = getArc(2 * DOWN, 1.5 * PI, PI / 2, '')
            # self.play(arcGroups.animate.become(arc))
              
        def divideCircle(n, thinSlices = False):
            angleDelta = (PI * 2) / n
            angle = 0
            thinSliceWidth = .5
            lines = VGroup()
            for i in range(n):
                line = Line(self.circle.get_center(),self.circle.point_at_angle(angle), stroke_width = sliceStrokeWidth)
                if thinSlices:
                    lines.set_stroke(width=thinSliceWidth)
                angle += angleDelta
                lines.add(line)
            # self.play(GrowFromCenter(lines))

            return lines

        def transition(pSlices, nSlices, animateNewSlice = True):
            nGroup = VGroup()
            pGroup = VGroup()
            remGroup = VGroup()
            remGroupList = []
            for i in pSlices:
                pGroup.add(i)
            for index, item in enumerate(nSlices):
                if(index < len(pSlices)):
                    nGroup.add(item)
                else:
                    remGroup.add(item)
                    remGroupList.append(item)
            self.play(pGroup.animate.become(nGroup))
            if animateNewSlice:
                for i in remGroupList:
                    self.play(FadeIn(i), run_time = 1 / (len(remGroupList)))
            else:
                self.play(FadeIn(remGroup))
            return pSlices + remGroupList


        def increaseSlice(n, incr,pSlices, animateNewSlice = True, thinSlices = False):
            nonlocal pLines
            noOfSlices = n + incr
            # if(pLines != None):
            #     self.remove(pLines)
            nLines = divideCircle(noOfSlices, thinSlices)
            # pLines = nLines
            self.play(GrowFromCenter(nLines))
            if pLines:
                self.remove(pLines)
            pLines = nLines
            # if(pLines != None):
            #     self.play(pLines.animate.become(nLines))
            # else:
            #     self.play(GrowFromCenter(nLines))
                # pLines = nLines
            nSlices = createSlices(noOfSlices, thinSlices)
            nSlices = transition(pSlices, nSlices, animateNewSlice)
            # gr = highlightSlices(nSlices)
            # self.play(FadeOut(gr))
            # self.play(nSlices[0][0].animate.set_stroke(ORANGE))


            return nSlices, pLines



        slices = 6
        angleDelta = (PI * 2) / slices
        arcLineGroup = []
        rotationAngles = []
        startAngle = 0
        lines = VGroup()
        arcs = VGroup()
        triangles = VGroup()
        circleAndSectionGroup = VGroup(self.circle)
        sliceStrokeWidth = 2
        arcStrokeWidth = 2
        colors = color_gradient([ORANGE, PURPLE] , 2)
        for i in range(slices):
            arc, sLine, fLine, triangle = getArc(
                self.circle.get_center(),startAngle,angleDelta,''
            )
            # arc.set_fill(colors[i % 2], 1)
            # triangle.set_fill(colors[i % 2], 1)
            
            # if i % 2:
            #     arc.set_color_by_gradient(BLUE, GREEN, GOLD)
            #     triangle.set_color_by_gradient(BLUE, GREEN, GOLD)
            # else:
            #     arc.set_color_by_gradient(ORANGE, PURPLE)
            #     triangle.set_color_by_gradient(ORANGE, PURPLE)

            group = VGroup(arc, sLine, fLine, triangle)
            arcLineGroup.append(group)
            triangles.add(triangle)
            # group.set_fill(BLUE)
            lines.add( fLine, sLine)
            lines.set_fill(self.ringColor, self.ringOpacity)
            # self.play(Create(group))
            rotationAngles.append(PI / 2 - startAngle - angleDelta / 2)
            startAngle += angleDelta
            arcs.add(arc)

            circleAndSectionGroup.add(group)

        # self.play(GrowFromCenter(lines))
        cuts = divideCircle(slices)
        circleAndSectionGroup.add(cuts)
        self.play(GrowFromCenter(cuts))
        self.add(arcs)
        self.add(triangles)
        self.circle.set_fill(BLUE, 0)
        self.play(
            circleAndSectionGroup.animate.move_to(2 * LEFT)
        )

        newArcLineGroup = createSlices(slices, False)
        for i in range(slices):
            gr : VGroup = arcLineGroup[i]
            self.play(gr.animate.become(newArcLineGroup[i]), run_time = .5)
        

        gr = highlightSlices(newArcLineGroup)
        self.play(FadeOut(gr))

        pLines = cuts

        pSlices = arcLineGroup

        for i in range(2):
            incr = slices
            pSlices, lines = increaseSlice(slices,incr,pSlices, True)
            slices += incr

        pSlices, lines = increaseSlice(slices, 100, pSlices, False, False)

        gr = highlightSlices(pSlices, False)

        areaText = self.areaTextSlice()

        self.play(FadeOut(areaText))
        self.play(FadeOut(gr))

        sliceGroup = VGroup()
        for i in (pSlices):
            sliceGroup.add(i)
        
        self.play(FadeOut(sliceGroup))
        
        # self.play(FadeOut(lines))
        # self.play(self.circleanimate.move_to(ORIGIN))
        # self.play(FadeOut())
        # self.f


        
    
    def areaTextSlice(self, triangle = False):
        
        textPos = 2 * DOWN
        text = MathTex(r"Area")
        text.move_to(textPos)
        self.play(FadeIn(text))

        nText = MathTex(r"Height * Width")
        if triangle:
            nText = MathTex(r".5 * Base * Height")
        nText.move_to(textPos)
        self.play(text.animate.become(nText))

        nText = MathTex(r"r * {\pi}r")
        if triangle:
            nText = MathTex(r".5 * r * 2{\pi}r")
        nText.move_to(textPos)
        self.play(text.animate.become(nText))

        nText = MathTex(r"{\pi}r^2")
        nText.move_to(textPos)
        self.play(text.animate.become(nText))
        return text
        


    def intro(self):
        circleRadius = 1
        circleBuff = .1
        self.circle = Circle(circleRadius, color = WHITE)
        self.play(Create(self.circle))

        radiusLine = Line(self.circle.get_center(),RIGHT)
        self.play(Create(radiusLine))
        
        brace = Brace(radiusLine,DOWN, buff=circleBuff)
        braceText = brace.get_tex(r"r" , buff = circleBuff)

        self.play(FadeIn(brace))
        self.play(FadeIn(braceText))


        self.circleGroup = VGroup(self.circle, radiusLine,brace,braceText)
        
        self.play(FadeOut(braceText), FadeOut(brace), FadeOut(radiusLine))
        # self.play(Create(self.circle), run_time = 1)

        circleBottomPoint = self.circle.point_at_angle(1.5 * PI)
        lineStartPoint = circleBottomPoint.copy()
        lineStartPoint[0]-= PI * self.circle.radius
        lineStartPoint[1]-= .1
        lineEndPoint = circleBottomPoint.copy()
        lineEndPoint[0] += PI * self.circle.radius
        lineEndPoint[1]-= .1


        c2 = Circle(circleRadius, color = ORANGE)

        self.play(Create(c2))

        line = Line(lineStartPoint, lineEndPoint, color = c2.color)

        self.play(c2.animate.become(line))

        brace = Brace(c2, DOWN)
        braceText = brace.get_tex(r"2{\pi}r")
        self.play(FadeIn(brace))
        self.play(FadeIn(braceText))

        self.play(FadeOut(brace), FadeOut(braceText))
        self.play(FadeOut(c2))


        

        # self.circle.set_fill(BLUE, .4)
        # self.add(self.circle)


        # self.play(FadeOut(braceText, brace, radiusLine))
        self.play(self.circle.animate.set_fill(self.ringColor, self.ringOpacity))



    def construct(self):

        self.intro()
        self.slicesAnimation()

        # rectangles, cutGr = self.ringAnimation(5)
        
        # self.play(
        #     self.circle.animate.move_to(3 * LEFT + 3 * UP),
        #     rectangles.animate.move_to( 3 * RIGHT + 3 * UP),
        #     cutGr.animate.move_to( 3 * LEFT + 3 * UP)
        
        # )
        # self.circle = Circle(1, WHITE)
        # self.circle.set_fill(self.ringColor, self.ringOpacity)
        # self.play(FadeIn(self.circle))
        # # self.ringAnimation(10)
        # rectangles, cutGr = self.ringAnimation(10)
        
        # self.play(
        #     self.circle.animate.move_to(3 * LEFT + 3 * DOWN),
        #     rectangles.animate.move_to( 3 * RIGHT + 3 * DOWN),
        #     cutGr.animate.move_to( 3 * LEFT + 3 * DOWN)
        
        # )
        # self.play()
        # self.slicesAnimation()
        
        # self.circle = Circle(1, color = WHITE).set_color_by_gradient(GREEN,)
        # self.play(Create(self.circle))
        # self.ringAnimation()
        # circleRadius = 1
        # circleBuff = .1
        # self.circle = Circle(circleRadius, color = BLUE)
        # # self.play(FadeIn(circle))
        # # self.play(Create(circle))
        # radiusLine = Line(self.circle.get_center(),RIGHT)
        # # self.play(Create(radiusLine))
        # brace = Brace(radiusLine,DOWN, buff=circleBuff)
        # braceText = brace.get_tex(r"r" , buff = circleBuff)
        
        # self.circleGroup = VGroup(self.circle, radiusLine,brace,braceText)
        # self.play(Create(self.circle), run_time = 1)

        # # self.circle.set_fill(BLUE, .4)
        # # self.add(self.circle)


        # # self.play(FadeOut(braceText, brace, radiusLine))
        # self.play(self.circle.animate.set_fill(BLUE, .6))


        # self.slicesAnimation()

        # self.ringAnimation()


    def ringAnimation(self, count):

        strokeColor = BLACK
        strokeWidth = 0

        def cutCircle(n):
            gap = self.circle.radius / n
            circlesGroup = VGroup()
            for i in range(n):
                sCircle = Circle((i + 1) * gap, stroke_width = .5)
                sCircle.move_to(self.circle.get_center())
                # sCircle.set_color(WHITE)
                sCircle.set_stroke(WHITE)
                circlesGroup.add(sCircle)
            return circlesGroup
 
        def bottomLeftBrace(prevRectangles):
            brace = Brace(prevRectangles, DOWN)
            txt = brace.get_tex(r"2{\pi}r")
            brace2 = Brace(prevRectangles, LEFT)
            txt2 = brace2.get_tex(r"r")
            labelGroup = VGroup(brace, txt, brace2, txt2)
            self.play(FadeIn(labelGroup))
            self.wait(1)
            self.play(FadeOut(labelGroup))



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



        center = 3 * LEFT
        self.play(self.circle.animate.move_to(center))
        # count = 5
        colors = color_gradient([BLUE, GREEN], length_of_output=count)
        gap = 1 / count
        prRings = VGroup()
        

        for i in range(count):
            ringRadius = 1 - (i + 1) * gap
            prRings.add(createRing(center, ringRadius, gap, colors[i]))
        
        cutGr = cutCircle(count)

        for i, item in enumerate(prRings):
            self.play(FadeIn(item), run_time = 1 / count)
            # self.add(cutGr[-i - 1])
        

        center = ORIGIN

        self.add(cutGr)
        self.play(prRings.animate.move_to(center))

        x = ValueTracker(0)
        
        def setRing(radius, zIndex, gap, color, time , animateCircle = False):
            
            ring = createRing(center, radius, gap, color)
            if animateCircle:
                self.play(FadeIn(ring), run_time = time)
            else:
                self.add(ring)

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
            self.remove(prRings[i])
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




        self.play(x.animate.set_value(2 * PI), run_time = 2)

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
        
        self.wait(1)

        return rectangles, cutGr
        




        # rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom = createRect(rings[0], True, True)
        # rectangle2, rectLeftTop2, rectLeftBottom2, rectRightTop2, rectRightBottom2 = createRect(rings[-1], True, True)
        # triangle = Polygon(rectLeftBottom, rectRightBottom, rectLeftTop2)
        # self.play(Create(triangle))
        # bottomLeftBrace(triangle)
        # self.areaTextSlice(True)

        

        
