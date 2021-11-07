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

            for i,item in enumerate(slices):
                if (i % 2 == 1):
                    continue

                arc : Arc = item[0].copy()
                arc.set_fill(None, 0)
                arc.set_stroke(width=2 * sliceStrokeWidth)
                arc.set_color(ORANGE)
                nArcs.append(arc)
                # self.play(Create(arc))
            nArcs.reverse()
            arcGroups = VGroup()
            for i in nArcs:
                if animateEach:
                    self.play(Create(i), run_time = 1 / len(slices))
                arcGroups.add(i)
            if animateEach == False:
                line = Line(fPoint, ePoint, stroke_width = 2 * sliceStrokeWidth, color = ORANGE)
                self.play(Create(line))
                arcGroups.add(line)
                # self.play(FadeIn(arcGroups))

            topBrace = Brace(arcGroups, UP)
            topBraceText = topBrace.get_tex(r"{\pi}r")
            self.play(FadeIn(topBrace), FadeIn(topBraceText))
            # self.play(arcGroups.animate.move_to(2 * DOWN))


            nArcs.reverse()

            fLine = slices[0][2].copy()
            fLine.set_stroke(ORANGE, width = 2 * sliceStrokeWidth)
            self.play(Create(fLine))

            leftBrace = Brace(fLine,  direction=fLine.copy().rotate(PI / 2).get_unit_vector())
            leftBraceText = leftBrace.get_tex(r"r")
            self.play(FadeIn(leftBrace), FadeIn(leftBraceText))
            
            highlightSlicesGroup.add(arcGroups,fLine, leftBrace, leftBraceText, topBrace, topBraceText)

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
            noOfSlices = n + n
            # if(pLines != None):
            #     self.remove(pLines)
            nLines = divideCircle(noOfSlices, thinSlices)
            # pLines = nLines
            if(pLines != None):
                self.play(pLines.animate.become(nLines))
            else:
                self.play(GrowFromCenter(nLines))
                pLines = nLines
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
        color1 = color_gradient([BLUE, GREEN], 1)
        color2 = color_gradient([ORANGE, PURPLE], 1)
        for i in range(slices):
            arc, sLine, fLine, triangle = getArc(
                self.circle.get_center(),startAngle,angleDelta,''
            )
            if i % 2:
                arc.set_color_by_gradient(BLUE, GREEN, GOLD)
                triangle.set_color_by_gradient(BLUE, GREEN, GOLD)
            else:
                arc.set_color_by_gradient(ORANGE, PURPLE)
                triangle.set_color_by_gradient(ORANGE, PURPLE)

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

        self.play(GrowFromCenter(lines))
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

        pLines = None

        pSlices = arcLineGroup

        for i in range(1):
            incr = 10
            pSlices, lines = increaseSlice(slices,incr,pSlices, True)
            slices += incr

        # pSlices, lines = increaseSlice(slices, 100, pSlices, False, False)

        # gr = highlightSlices(pSlices, False)

        # areaText = self.areaTextSlice()

        # self.play(FadeOut(areaText))
        # self.play(FadeOut(gr))

        # sliceGroup = VGroup()
        # for i in (pSlices):
        #     sliceGroup.add(i)
        
        # self.play(FadeOut(sliceGroup))
        
        # self.play(FadeOut(lines))
        # self.play(self.circle.animate.move_to(ORIGIN))
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

        # self.intro()
        # self.slicesAnimation()
        
        self.circle = Circle(1).set_color_by_gradient(GREEN, BLUE)
        self.play(FadeIn(self.circle))
        self.wait(1)
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


    def ringAnimation(self):


        def createRing(center, innerRadius, gap):
            ring = Circle(radius=innerRadius + gap, stroke_width = 0)
            ring.move_to(center)
            ring.set_fill(self.ringColor, self.ringOpacity)
            innerRing = Circle(innerRadius, stroke_width = 0)
            innerRing.move_to(center)
            innerRing.set_fill(BLACK, 1)
            return VGroup(ring, innerRing)
       

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

    
        def createRect(ring : VGroup, extended, returnCorner):
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
            rectangle.set_fill(self.ringColor, self.ringOpacity)

            if returnCorner:
                return rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom
            return rectangle

        def unwrapRing(ring : VGroup):
            gap = ring[0].radius - ring[1].radius
            rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom = createRect(ring, False, True)
            self.add(rectangle)
            
            if ring[1].radius == 0:
                rect = createRect(ring,True, False)
                self.play(ring.animate.become(rect))
                return rect

            innerRadius = ring[1].radius


            def createConveringArc(angle,side):
                startAngle = 1.5 * PI
                arc = None
                if side == 'LEFT':
                    arc = Arc(innerRadius + gap,startAngle,-angle, arc_center= ring[0].get_center())
                else:
                    arc = Arc(innerRadius + gap,.5 * PI,-(angle - PI), arc_center= ring[0].get_center())
                triangle = Polygon(ring[0].get_center(), arc.get_start(), arc.get_end(),stroke_width = 0)
                arc.set_fill(BLACK, 1)
                triangle.set_fill(BLACK, 1)
                arc.set_stroke(width=0)
                triangle.set_stroke(width=0)
                arcGroup = VGroup(arc, triangle)

                return arcGroup

            initCenterX = ring[0].get_center()[0]
            angle = 0

            leftArcGroup = createConveringArc(0, 'LEFT')
            rightArcGroup = createConveringArc(PI, 'RIGHT')

            trAngle = 0
            tr1 = ring[0].point_at_angle(trAngle)
            tr2 = ring[1].point_at_angle(trAngle)
            angle2 = (angle / (2 * PI)) * (PI * ring[1].radius)
            angle2 = .05
            tr3 = ring[1].point_at_angle(min(2 * PI, angle + angle2))
            tr = Polygon(tr1, tr2, tr3)

            gr = VGroup(ring,leftArcGroup, rightArcGroup, tr)

            self.add(gr)


            

            x = ValueTracker(ring[0].get_arc_center()[0])
            

            def rectUpdater(rect):
                RLT = rectLeftTop.copy()
                RLT[0] += ((x.get_value() - initCenterX) /( (2 * PI * ring[0].radius) - PI * gap)) * PI * gap
                rectRightTop = rectLeftTop.copy()
                rectRightBottom = rectLeftBottom.copy()
                rectRightBottom[0] = rectRightTop[0] = x.get_value()
                # rectRightBottom
            
                rectangle = Polygon(rectLeftBottom, RLT, rectRightTop, rectRightBottom)
                rectangle.set_stroke(width=0)
                rectangle.set_fill(self.ringColor, self.ringOpacity)
                rect.become(rectangle)
                rect.set_z_index(10)

            def updater(r):
                center = ring[0].get_arc_center()
                
                center[0] = x.get_value()

                angle = max(0,(center[0] - initCenterX)) / ( (innerRadius + gap))

                trAngle = angle
                if angle > 1.5 * PI:
                    trAngle = 2 * PI - angle + 1.5 * PI
                    trAngle = min(trAngle, 2 * PI)
                else:
                    trAngle = 1.5 * PI - angle
                tr1 = ring[0].point_at_angle(trAngle)
                tr2 = ring[1].point_at_angle(trAngle)

                extra = ((x.get_value() - initCenterX) /( (2 * PI * ring[0].radius))) * PI * gap
                if ring[1].radius > 0:
                    extra /= ring[1].radius
                # else:
                #     extra = 0

                angle2 = (angle / (2 * PI)) * (PI * ring[1].radius)
                angle2 = extra
                tr3 = ring[1].point_at_angle(max(0, trAngle - angle2))
                nTr = Polygon(tr1, tr2, tr3)
                # nTr.set_stroke(width=0)
                # nTr.set_fill(BLACK, opacity=1)
                tr.become(nTr)
                # self.add(nTr)

                newArcGroup = None
                if angle <= PI :
                    newArcGroup = createConveringArc(angle, 'LEFT')
                    leftArcGroup.become(newArcGroup)
                else:
                    lc = createConveringArc(PI, 'LEFT')
                    leftArcGroup.become(lc)
                    newArcGroup = createConveringArc(angle, 'RIGHT')
                    rightArcGroup.become(newArcGroup)
                
            
                r.move_to(center)
            
                
            gr.add_updater(updater)
            rectangle.add_updater(rectUpdater)

            self.play(x.animate.set_value(ring[0].get_center()[0] + 2 * PI * (innerRadius + gap) ), run_time = 2)
            rectangle.remove_updater(rectUpdater)

            # rectRightTop = rectLeftTop.copy()
            # rectRightBottom = rectLeftBottom.copy()
            # rectLeftTop[0] += PI * gap
            # rectRightTop[0] -= PI * gap
            # rectRightTop[0] +=  + 2 * ring[0].radius * PI
            # rectRightBottom[0] += 2 * ring[0].radius * PI
            # p3 = rectRightTop.copy()
            # p3[1] -= gap
            # tr = Polygon(rectRightTop, rectRightBottom, p3)
            # rect2 = Polygon(rectLeftBottom, rectLeftTop, rectRightTop, rectRightBottom)
            # rect2.set_stroke(width=0)
            # rect2.set_fill(self.ringColor, self.ringOpacity)
            # tr.set_stroke(width=0)
            # tr.set_fill(self.ringColor, self.ringOpacity)
            # # self.play(gr.animate.become(tr), run_time = (gap) / (innerRadius + gap))
            # self.remove(ring)
            # self.play( FadeIn(tr), run_time = (gap) / (innerRadius + gap))
            # self.play(FadeOut(ring), rectangle.animate.become(rect2), run_time = (gap) / (innerRadius + gap))
            # rect2 = createRect(ring,True,False)
            # self.remove(ring)
            # self.play(FadeOut(ring), FadeIn(tr), run_time = (gap) / (innerRadius + gap))
            # self.play(rectangle.animate.become(rect2), run_time = (gap) / (innerRadius + gap))
            return rectangle


        prevCutCircularGroup = None
        prevRings = None
        prevRectangles = None


        def step(noOfRings, animate = True, showBrace = False):
            
            nonlocal prevRectangles, prevRings, prevCutCircularGroup

            circleRadius = self.circle.radius
            rings = VGroup()
            gap = circleRadius / noOfRings
            for i in range(noOfRings):
                rings.add(createRing(self.circle.get_center(), circleRadius - (i + 1) * gap, gap))
            
            if animate:
                self.circle.set_fill(opacity=0)
                self.add(rings)
            
            cutCirclesGroup = cutCircle(noOfRings)
            if animate:
                self.play(Create(cutCirclesGroup))
            

            if(animate):
                self.play(
                    self.circle.animate.move_to( 3 * LEFT), 
                    rings.animate.move_to(3 * LEFT),
                    cutCirclesGroup.animate.move_to(3 * LEFT)    
                )

            rectangles = VGroup()

            for i, item in enumerate(rings):
                if animate:
                    self.remove(cutCirclesGroup[noOfRings - i - 1])    
                    self.play(item.animate.move_to(ORIGIN))
                    rectangles.add(unwrapRing(item))
                else:
                    item.move_to(ORIGIN)
                    rectangles.add(createRect(item,True, False))
                # break
        
            if prevCutCircularGroup != None:
                gr1 = VGroup()
                gr2 = VGroup()
                self.play(prevCutCircularGroup.animate.become(cutCirclesGroup))
                nB = VGroup()
                for i in range(noOfRings):
                    if i < len(prevRectangles):
                        gr1.add(rectangles[i])
                        # self.play(prevRectangles[i].animate.become(rectangles[i]))
                        nB.add(prevRectangles[i])
                    else:
                        gr2.add(rectangles[i])
                        # self.play(Create(rectangles[i]))
                        nB.add(rectangles[i])

                self.play(prevRectangles.animate.become(gr1))
                self.play(FadeIn(gr2))
                rectangles = nB

            else:
                prevCutCircularGroup = cutCirclesGroup

            prevRectangles = rectangles
            
            if showBrace:
                bottomLeftBrace(prevRectangles)
            return rings


        def bottomLeftBrace(prevRectangles):
            brace = Brace(prevRectangles, DOWN)
            txt = brace.get_tex(r"2{\pi}r")
            brace2 = Brace(prevRectangles, LEFT)
            txt2 = brace2.get_tex(r"r")
            labelGroup = VGroup(brace, txt, brace2, txt2)
            self.play(FadeIn(labelGroup))
            self.wait(1)
            self.play(FadeOut(labelGroup))


        startSlice = 5
        incr = 4
        for i in range(1):
            step(startSlice, i == 0, i == 0)
            startSlice += incr
        
        # step(5)
        # step(9, False)
        # step(7, False)
        # step(9, False)
        # step(11, False)
        # # step(13, False)
        # rings = step(100, False)

        # rectangle, rectLeftTop, rectLeftBottom, rectRightTop, rectRightBottom = createRect(rings[0], True, True)
        # rectangle2, rectLeftTop2, rectLeftBottom2, rectRightTop2, rectRightBottom2 = createRect(rings[-1], True, True)
        # triangle = Polygon(rectLeftBottom, rectRightBottom, rectLeftTop2)
        # self.play(Create(triangle))
        # bottomLeftBrace(triangle)
        # self.areaTextSlice(True)

        

        
