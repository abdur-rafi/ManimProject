from math import floor
from manim import *

class CircleArea(Scene):
    

    ringColor = BLUE
    ringOpacity = .4
    font =  'Li Shamim Cholontika UNICODE'

    def highlightSlices(self,slices, sliceStrokeWidth, animateEach = True):
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

        topBrace = Brace(arcGroups, UP)
        topBraceText = topBrace.get_tex(r"{\pi}r")
        self.play(FadeIn(topBrace), FadeIn(topBraceText))


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


    def slicesAnimation(self, slices, moveCircleTo, sliceStartPoint, animateEach = False):

        colors = [[BLUE, GREEN, GOLD], [ORANGE, PURPLE]]
        opacity = .3

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

        def createSlices(n, thinSlices, startPoint):
            center = startPoint
            angleDelta = (PI * 2) / n
            slices = VGroup()
            thinSliceWidth = 1
            arcs = []
            for i in range(floor(n / 2)):   
                arc, sLine, fLine, triangle = getArc(center,.5 * PI - angleDelta / 2,angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                if thinSlices:
                    for i in group:
                        i.set_stroke(width = thinSliceWidth)
                slices.add(group)

                group.set_fill(colors[0], opacity)

                center = arc.get_start()
                
                arc, sLine, fLine, triangle = getArc(center,1.5 * PI - angleDelta / 2, angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                
                group.set_fill(colors[1], opacity)

                if thinSlices:
                    for i in group:
                        i.set_stroke(width = thinSliceWidth)
                slices.add(group)

                center = arc.get_end()
            return slices

       
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

        angleDelta = (PI * 2) / slices
        startAngle = 0
        slicesGroup = VGroup()
        sliceStrokeWidth = 2
        # arcStrokeWidth = 2
        # colors = color_gradient([ORANGE, PURPLE] , 2)

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
            triangle.set_stroke(width=0)
            group.set_fill(colors[i % 2], opacity)
            slicesGroup.add(group)
            startAngle += angleDelta
        
        cuts = divideCircle(slices)

        self.play(GrowFromCenter(cuts))
        self.circle.set_fill(opacity=0)
        self.play(FadeIn(slicesGroup))
        self.wait(1)
        self.play(self.circle.animate.move_to(moveCircleTo), cuts.animate.move_to(moveCircleTo), slicesGroup.animate.move_to(moveCircleTo))

        movedSlicesGroup = createSlices(slices, False, sliceStartPoint)

        if animateEach:
            for i in range(slices):
                self.play(slicesGroup[i].animate.become(movedSlicesGroup[i]), run_time = 2 / slices)
        else:
            self.play(slicesGroup.animate.become(movedSlicesGroup))


        return slicesGroup, cuts
        
    
    def areaTextSlice(self, textPos, scale, triangle = False):
        
        text = MathTex(r"Area").scale(scale)
        text.move_to(textPos)
        self.play(FadeIn(text))

        nText = MathTex(r"Height * Width").scale(scale)
        if triangle:
            nText = MathTex(r".5 * Base * Height").scale(scale)
        nText.move_to(textPos)
        self.play(text.animate.become(nText))

        nText = MathTex(r"r * {\pi}r").scale(scale)
        if triangle:
            nText = MathTex(r".5 * r * 2{\pi}r").scale(scale)
        nText.move_to(textPos)
        self.play(text.animate.become(nText))

        nText = MathTex(r"{\pi}r^2")
        nText.move_to(textPos).scale(scale)
        self.play(text.animate.become(nText))
        return text

    def areaTextSlice2(self, textPos, scale, triangle = False):
        
        text = MathTex(r"Area = ").scale(scale)
        text.move_to(textPos)
        # self.play(FadeIn(text))
        

        nText = MathTex(r"Height * Width")
        if triangle:
            nText = MathTex(r"{\frac{1}{2}} * Base * Height")
        nText.scale(scale).move_to(textPos).shift((2.9 * scale) * RIGHT + (.05 * scale) * DOWN)
        self.play(FadeIn(text), FadeIn(nText))

        oText = nText
        nText = MathTex(r"r * {\pi}r")
        if triangle:
            nText = MathTex(r"{\frac{1}{2}} * 2{\pi}r * r")
        
        nText.scale(scale).move_to(textPos).shift((2.1 * scale) * RIGHT + (.05 * scale) * DOWN)
        self.play(oText.animate.become(nText))


        nText = MathTex(r"{\pi}r^2")
        nText.scale(scale).move_to(textPos).shift((1.75 * scale) * RIGHT + (.05 * scale) * UP)

        self.play(oText.animate.become(nText))

        return VGroup(text, oText)
        


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
        # self.play(self.circle.animate.set_fill(self.ringColor, self.ringOpacity))


    def sliceAnimationComplete(self):
        slices = 6
        moveCircleTo = 2 * LEFT
        startPoint = RIGHT + .5 * DOWN
        
        allElelms = VGroup()

        slicesGroup, cuts = self.slicesAnimation(slices, moveCircleTo, startPoint, True)
        highlightGroup = self.highlightSlices(slicesGroup, 2, True)
        self.play(FadeOut(highlightGroup))
        
        allElelms.add(slicesGroup, cuts, self.circle)

        circles = []

        deltaY = 3 * UP

        self.play(
            self.circle.animate.shift( deltaY),
            cuts.animate.shift( deltaY), 
            slicesGroup.animate.shift(deltaY)
        )

        self.circle = Circle(color = WHITE)
        self.play(Create(self.circle))
        # self.play(self.circle.animate.set_fill(self.ringColor, self.ringOpacity))
        
        slices += slices

        slicesGroup, cuts = self.slicesAnimation(slices, moveCircleTo, startPoint)

        allElelms.add(slicesGroup, cuts, self.circle)


        deltaY = 3 * DOWN

        self.play(
            self.circle.animate.shift( deltaY),
            cuts.animate.shift( deltaY), 
            slicesGroup.animate.shift(deltaY)
        )

        self.circle = Circle(color = WHITE)
        self.play(Create(self.circle))
        # self.play(self.circle.animate.set_fill(self.ringColor, self.ringOpacity))

        slices = 100

        slicesGroup, cuts = self.slicesAnimation(slices, moveCircleTo, startPoint)
        highlightGroup = self.highlightSlices(slicesGroup, 2, False)
        
        

        allElelms.add(slicesGroup, cuts, self.circle, highlightGroup)

        self.play(allElelms.animate.shift(3 * LEFT).scale(.6))

        areaText = self.areaTextSlice2(2 * RIGHT, .6)

        self.play(FadeOut(areaText))


        self.play(FadeOut(allElelms))


    def rectLabels(self, rectangles):
        brace = Brace(rectangles, DOWN)
        txt = brace.get_tex(r"2{\pi}r")
        braceL = Brace(rectangles, LEFT)
        txtL = braceL.get_tex(r"r")
        self.play(FadeIn(brace, txt))
        self.play(FadeIn(braceL, txtL))
        return VGroup(brace, txt, braceL, txtL)
    

    def ringAnimationAll(self):
        allRingGroups = VGroup()

        self.circle = Circle(1, WHITE)
        # self.circle.set_fill(self.ringColor, self.ringOpacity)
        self.play(FadeIn(self.circle))

        rings = 5
        rectangles, cutGr = self.ringAnimation(rings)
        # rectangles.set_z_index(30)
        # cutGr.set_z_index(30)
        # self.circle.set_z_index(30)
        deltaY = 3 * UP
        self.play(
            self.circle.animate.shift(deltaY),
            rectangles.animate.shift(deltaY),
            cutGr.animate.shift(deltaY)
        
        )
        rings += rings
        allRingGroups.add(self.circle, rectangles, cutGr)


        self.circle = Circle(1, WHITE)
        # self.circle.set_fill(self.ringColor, self.ringOpacity)
        self.play(FadeIn(self.circle))

        rectangles, cutGr = self.ringAnimation(rings)
        deltaY = 3 * DOWN
        self.play(
            self.circle.animate.shift(deltaY),
            rectangles.animate.shift(deltaY),
            cutGr.animate.shift(deltaY)
        
        )
        rings += rings
        allRingGroups.add(self.circle, rectangles, cutGr)


        self.circle = Circle(1, WHITE)
        # self.circle.set_fill(self.ringColor, self.ringOpacity)
        self.play(FadeIn(self.circle))

        rectangles, cutGr = self.ringAnimation(rings)
        allRingGroups.add(self.circle, rectangles, cutGr)
        labels = self.rectLabels(rectangles)
        allRingGroups.add(labels)

        self.play(allRingGroups.animate.shift(3 * LEFT).scale(.6))

        areaText = self.areaTextSlice2(2 * RIGHT, .8, True)

        self.play(FadeOut(areaText))

        # allRingGroups.add(areaText)

        self.play(FadeOut(allRingGroups))
        
    
    def circleToRect(self):
        grad = [GREEN, BLUE]
        opacity = .6
        self.circle = Circle(color = WHITE).set_fill(grad, opacity)
        # circle2 = self.circle.copy().move_to(3 * RIGHT)
        self.play(FadeIn(self.circle))
        rectangle = Rectangle(WHITE, height=self.circle.radius, width=self.circle.radius * PI).set_fill(grad, opacity)
        self.play(self.circle.animate.become(rectangle))
        self.play(FadeOut(self.circle))

    def circleToTriangle(self):
        grad = [GREEN, BLUE]
        opacity = .6
        self.circle = Circle(color = WHITE).set_fill(grad, opacity)
        self.play(FadeIn(self.circle))
        self.ringAnimation2nd(5)


    def introText(self):
        banglaText = Text("বৃত্তের ক্ষেত্রফল ", font = self.font ).set_color_by_gradient(BLUE, GREEN, GOLD).scale(1.2).shift(.5 * UP)
        englishText = Text("Area of a circle", font = self.font).set_color_by_gradient(BLUE, GREEN, GOLD).scale(1.2).shift(.5 * DOWN)
        textGroup = VGroup(banglaText, englishText)

        self.play(Write(banglaText), run_time = 1.5)
        self.play(Write(englishText), run_time = 1.5)

        self.wait(1)
        self.play(FadeOut(textGroup))
        return textGroup

    def rectangleArea(self):
        colors = [BLUE, GREEN, GOLD]
        rectangle = Rectangle().set_fill(colors, .5)
        areaText = MathTex(r"Area = height * width").next_to(rectangle, DOWN).scale(.6)
        rectGroup = VGroup(rectangle, areaText)
        # self.play(Create(rectGroup))
        return rectGroup
    
    def triangleArea(self):
        colors = [BLUE, GREEN, GOLD]
        triangle = Triangle().scale(1.5).set_fill(colors, .5)
        areaText = MathTex(r"Area = {\frac{1}{2}} * height * base").next_to(triangle, DOWN).scale(.6)
        trGroup = VGroup(triangle, areaText)
        # self.play(Create(trGroup))
        return trGroup

    def rectTrArea(self):
        rectArea = self.rectangleArea()
        trArea = self.triangleArea()
        rectArea = rectArea.shift(3 * LEFT)
        trArea = trArea.shift(3 * RIGHT)
        self.play(FadeIn(rectArea[0]), FadeIn(trArea[0]), run_time = 1.5)
        self.play(Write(rectArea[1]), Write(trArea[1]), run_time = 1.5)

        self.wait(1)
        self.play(FadeOut(rectArea, trArea))
    
    def circleArea(self):
        circle = Circle(1, WHITE)
        circle2 = Circle(1).set_fill([PURPLE, ORANGE], .5).set_stroke(width=0)
        self.play(FadeIn(VGroup(circle, circle2)))
        

        line = Line(ORIGIN, circle.point_at_angle(0)).set_stroke(ORANGE, 2)
        self.play(Create(line))
        
        brace = Brace(line, DOWN, buff = .1)
        braceTxt = brace.get_tex(r"r", buff = .1)
        # areaText = Text("ক্ষেত্রফল = ", font = self.font ).scale(.6)
        self.play(FadeIn(brace), FadeIn(braceTxt))

        areaText = MathTex(r"Area").next_to(circle, DOWN, buff=.2).shift(.75 * LEFT)
        self.play(circle2.animate.become(areaText))
        eqText = MathTex(r" = ").next_to(circle2, RIGHT)
        self.play(Write(eqText))
        piText = MathTex(r"{\pi}").next_to(eqText, RIGHT)
        self.play(Write(piText))
        braceTxt2 = braceTxt.copy()
        self.play(braceTxt2.animate.become(MathTex(r"r").next_to(piText, .5 *RIGHT)))
        self.play(braceTxt2.animate.become(MathTex(r"r^2").next_to(piText, .5 * RIGHT)).shift(.1 * UP))
        # self.play(braceTxt)

        # areaText2 = MathTex(r"Area = {\pi}r^2")
        # txtGroup = VGroup(areaText2)
        # txtGroup.next_to(circle, DOWN)
        # self.play(Write(areaText2))
        # gr = VGroup(circle, line, brace, braceTxt,txtGroup)
        # # self.play(Create(gr), run_time = 2)
        # self.wait(1)
        # txt = Text("")
        # self.play(FadeOut(gr))


    def endText(self):
        cya = Text("Thank you for watching!", font_size=35).set_color_by_gradient(BLUE, GREEN, GOLD).move_to(ORIGIN)
        cya1 = Text("Instructor: Kazi Rakibul Hasan", font_size=21).set_color_by_gradient(GOLD, ORANGE).next_to(cya,
                                                                                                                3 * DOWN)
        cya2 = Text("Animation: Abdur Rafi", font_size=21).set_color_by_gradient(ORANGE, PURPLE).next_to(
            cya1, DOWN)
        self.play(Write(VGroup(cya, cya1, cya2)))

    def construct(self):

        # self.introText()
        self.circleArea()
        # self.rectTrArea()
        # self.intro()

        # txt = self.introText()
        # self.play(FadeOut(txt))
        # self.rectangleArea()
        
        moveCircleTo = 2 * LEFT
        startPoint = RIGHT + .5 * DOWN
        # self.intro()
        # self.slicesAnimation(6,moveCircleTo, startPoint, True)
        # self.sliceAnimationComplete()
        # self.ringAnimationAll()
        
        # self.circleToRect()
        # self.circleToTriangle()
        # self.endText()

        

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
            # strokeColor = BLACK
            # strokeWidth = 1
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
                arc.set_stroke(strokeColor, width=strokeWidth + 1)
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

    def ringAnimation2nd(self, count):
        strokeColor = BLACK
        strokeWidth = .5

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
            return VGroup(ring, leftCoveringArc, rightCoveringArc,leftTr, rightTr)

        
        colors = color_gradient([BLUE, GREEN], length_of_output=count)
        gap = 1 / count
        ringGr = VGroup()
        for i in range(count):
            r = setRing(1 - (i + 1) * gap, i + 1, gap, colors[i] , 1 / count)
            ringGr.add(r)

        # self.play(Create(ringGr))
        self.remove(self.circle)
        # self.play(x.animate.set_value(mid), run_time = 2)
        self.play(x.animate.set_value(end), run_time = 2, rate_func = rate_functions.ease_in_cubic)
        
        self.wait(1)
        self.play(FadeOut(ringGr))

        
