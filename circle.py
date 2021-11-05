from math import floor
from manim import *

class CircleArea(Scene):
    
    def construct(self):

        circleRadius = 1
        circleBuff = .1
        circle = Circle(circleRadius, color = BLUE)
        # self.play(FadeIn(circle))
        # self.play(Create(circle))
        radiusLine = Line(circle.get_center(),RIGHT)
        # self.play(Create(radiusLine))
        brace = Brace(radiusLine,DOWN, buff=circleBuff)
        braceText = brace.get_tex(r"r" , buff = circleBuff)
        
        self.circleGroup = VGroup(circle, radiusLine,brace,braceText)
        self.play(Create(self.circleGroup), run_time = 1)


        self.play(FadeOut(braceText, brace, radiusLine))
        self.play(circle.animate.set_fill(BLUE, .4))


        slices = 6
        angleDelta = (PI * 2) / slices

        arcLineGroup = []
        rotationAngles = []
        startAngle = 0
        lines = VGroup()
        arcs = VGroup()
        triangles = VGroup()

        circleAndSectionGroup = VGroup(circle)
        
        sliceStrokeWidth = 2
        arcStrokeWidth = 2

        def getArc(center, startAngle,angleDelta,fill_color):
            arc = Arc(circle.radius, startAngle,angleDelta,
            arc_center=center, stroke_width = sliceStrokeWidth)
            arc.set_fill(BLUE, .4)
            fLine = Line(center,arc.get_start(),stroke_width = sliceStrokeWidth)
            sLine = Line(center,arc.get_end(),stroke_width = sliceStrokeWidth)
            triangle = Polygon(center, arc.get_start(), arc.get_end(),stroke_width = 0)
            triangle.set_fill(BLUE, .4)
            # self.add(triangle)
            return arc, fLine, sLine, triangle

        for i in range(slices):
            arc, sLine, fLine, triangle = getArc(circle.get_center(),startAngle,angleDelta,'')
            group = VGroup(arc, sLine, fLine, triangle)
            arcLineGroup.append(group)
            triangles.add(triangle)
            # group.set_fill(BLUE)
            lines.add( fLine, sLine)
            lines.set_fill(BLUE, .4)
            # self.play(Create(group))
            rotationAngles.append(PI / 2 - startAngle - angleDelta / 2)
            startAngle += angleDelta
            arcs.add(arc)

            circleAndSectionGroup.add(group)

        self.play(GrowFromCenter(lines))
        
        self.add(arcs)
        self.add(triangles)
        
        circle.set_fill(BLUE, 0)

        self.play(
            circleAndSectionGroup.animate.move_to(5 * LEFT)
        )

        def createSlices(n):
            center = .5 * DOWN
            angleDelta = (PI * 2) / n
            slices = []
            arcs = []
            for i in range(floor(n / 2)):   
                arc, sLine, fLine, triangle = getArc(center,.5 * PI - angleDelta / 2,angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                slices.append(group)

                center = arc.get_start()
                
                arc, sLine, fLine, triangle = getArc(center,1.5 * PI - angleDelta / 2, angleDelta,'')
                group = VGroup(arc, sLine, fLine, triangle)
                slices.append(group)

                center = arc.get_end()
            return slices


        newArcLineGroup = createSlices(slices)
        for i in range(slices):
            gr : VGroup = arcLineGroup[i]
            self.play(gr.animate.become(newArcLineGroup[i]), run_time = .5)
        

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
                line = Line(fPoint, ePoint, stroke_width = arcStrokeWidth, color = ORANGE)
                self.play(Create(line))
                arcGroups.add(line)
                # self.play(FadeIn(arcGroups))

            topBrace = Brace(arcGroups, UP)
            topBraceText = topBrace.get_tex(r"{\pi}r")
            self.play(Create(topBrace), Create(topBraceText))
            # self.play(arcGroups.animate.move_to(2 * DOWN))


            nArcs.reverse()

            fLine = slices[0][2].copy()
            fLine.set_stroke(ORANGE, width = 2 * sliceStrokeWidth)
            self.play(Create(fLine))

            leftBrace = Brace(fLine,  direction=fLine.copy().rotate(PI / 2).get_unit_vector())
            leftBraceText = leftBrace.get_tex(r"r")
            self.play(Create(leftBrace), Create(leftBraceText))
            
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
                

        gr = highlightSlices(newArcLineGroup)

        self.play(FadeOut(gr))

        def divideCircle(n):
            angleDelta = (PI * 2) / n
            angle = 0
            lines = VGroup()
            for i in range(n):
                line = Line(circle.get_center(),circle.point_at_angle(angle), stroke_width = sliceStrokeWidth)
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

        pLines = None

        

        def increaseSlice(n, incr,pSlices, animateNewSlice = True):
            nonlocal pLines
            noOfSlices = n + incr
            # if(pLines != None):
            #     self.remove(pLines)
            nLines = divideCircle(noOfSlices)
            # pLines = nLines
            if(pLines != None):
                self.play(pLines.animate.become(nLines))
            else:
                self.play(GrowFromCenter(nLines))
                pLines = nLines
            nSlices = createSlices(noOfSlices)
            nSlices = transition(pSlices, nSlices, animateNewSlice)
            # gr = highlightSlices(nSlices)
            # self.play(FadeOut(gr))
            # self.play(nSlices[0][0].animate.set_stroke(ORANGE))


            return nSlices

        pSlices = arcLineGroup

        for i in range(4):
            incr = 2
            pSlices = increaseSlice(slices,incr,pSlices, True)
            slices += incr

        pSlices = increaseSlice(slices, 200, pSlices, False)

        
        gr = highlightSlices(pSlices, False)
        # self.play(FadeOut(gr))

        # sliceGroup = VGroup()
        # for i in pSlices:
        #     sliceGroup.add(i)
        
        # brace = Brace(sliceGroup, UP);
        # # brace.move_to(sliceGroup, UP)
        # self.play(Create(brace))
        
