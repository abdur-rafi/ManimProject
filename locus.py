from math import cos, sin, sqrt, tan
from manim import *
from random import *

class Locus(Scene):


    font =  'Li Shamim Cholontika UNICODE'
    engFont = 'Zuka Doodle'
    dotColor = GOLD
    circleRadius = 1.5
    fixedPointColor = TEAL
    a = 1
    dashC = 100

    def locusLine(self):

        plane = NumberPlane(
            x_range=[-5, 10, 1],
            y_range=[-4, 6, 1],
            axis_config = {"include_numbers" : True}
        )
        self.play(FadeIn(plane))

        fDot = Dot(plane.c2p(2, 1, 0)).set_stroke(YELLOW)
        sDot = Dot(plane.c2p(7, 1, 0)).set_stroke(YELLOW)

        fDotLabel = MathTex(r"A(2, 1)").scale(.7)
        sDotLabel = MathTex(r"B(7, 1)").scale(.7)
        
        fDotLabel.next_to(fDot, LEFT)
        sDotLabel.next_to(sDot, RIGHT)

        VGroup( fDot, sDot).set_color(self.fixedPointColor)


        self.play(Create(fDot), Create(sDot))
        self.play(Write(VGroup(sDotLabel, fDotLabel)))

        self.play(FadeOut(plane))
        shift = 2 * LEFT
        plane = plane.shift(shift)
        self.play(VGroup(fDot, sDot, sDotLabel, fDotLabel).animate.shift(shift))

        startPoint = plane.c2p(4.5, 4, 0) 
        endPoint = plane.c2p(4.5, -2, 0)

        movingDot = Dot(startPoint).set_z_index(10).set_color(self.dotColor)
        self.play(Create(movingDot))
        movingDotLabel = MathTex(r"P(x, y)").scale(.7).next_to(movingDot,RIGHT)
        self.play(Write(movingDotLabel))
        movingDotLabel.add_updater(lambda x : movingDotLabel.next_to(movingDot, RIGHT))

        line = Line(startPoint, endPoint).set_stroke(self.dotColor)

        dottedLine = DashedVMobject(Line(startPoint, endPoint).set_stroke(BLACK, 5, opacity=1), self.dashC).set_z_index(2)
        
        self.add(dottedLine)

        
        

        l1 = Line()
        l2 = Line()

        

        # self.play(VGroup(movingDot, fDot,sDot).animate.move_to(ORIGIN))

        def dotUpdater(mob):
            movingDot.move_to(line.get_corner(DOWN))
        movingDot.add_updater(dotUpdater)
        self.add(movingDot)

        def l1Updater(mob):
            l1.become(Line(fDot.get_center(), movingDot.get_center()))
        
        def l2Updater(mob):
            l2.become(Line(sDot.get_center(), movingDot.get_center()))
            
            
        l1.add_updater(l1Updater)
        l2.add_updater(l2Updater)

        self.add(fDot, sDot,  l1, l2)
        self.play(Create(line), run_time = 1.5)

        line2 = line.copy().set_z_index(6).set_color(YELLOW)
        movingDot.remove_updater(dotUpdater)
        l1.remove_updater(l1Updater)
        l2.remove_updater(l2Updater)

        self.play(Create(line2))

        dots = VGroup(sDot, fDot, sDotLabel, fDotLabel, movingDot, movingDotLabel)
        lines = VGroup(l1, l2, line, line2, dottedLine)
        
        # allObj = VGroup(dots.copy(), lines.copy())
        dotsCopy = dots.copy()

        # copy = [i.copy() for i in self.mobjects]
        self.play(VGroup(dots, lines).animate.scale(.8).shift(3 * LEFT))


        # movingDot.add_updater(dotUpdater)
        l1.add_updater(l1Updater)
        l2.add_updater(l2Updater)

        self.play(movingDot.animate.shift(4 * UP))
        # self.play(FadeOut(VGroup(movingDot, line, line2, dottedLine, l1, l2 )))

        eqnText = r"""
            &{\Rightarrow}{\sqrt{(x - 2)^2 + (y - 1)^2}} = {\sqrt{(x - 7)^2 + (y - 1)^2}} 
            \\&{\Rightarrow} (x - 2)^2 = (x - 7)^2
            \\&{\Rightarrow} x^2 - 4x + 4 = x^2 - 14x + 49
            \\&{\Rightarrow} x^2 - 4x + 4 - x^2 + 14x - 49 = 0
            \\&{\Rightarrow} 10x - 45 = 0
            \\&{\Rightarrow} x - 4.5 = 0
             
        """

        l11 = l1.copy().set_color(ORANGE).reverse_direction()

        l22 = l2.copy().set_color(ORANGE).reverse_direction()
        self.play(Create(l11))
        PA = MathTex(r"PA").scale(.6).move_to( .5 * RIGHT + 2.5 * UP)
        self.play(l11.animate.become(PA))
        eq = MathTex(r" = ").scale(.6).next_to(PA, RIGHT)
        self.play(Write(eq))
        self.play(Create(l22))
        PB = MathTex(r"PB").scale(.6).next_to(eq, RIGHT)
        self.play(l22.animate.become(PB))


        l1.clear_updaters()
        l2.clear_updaters()

        eqn = MathTex(eqnText).scale(.6).next_to(PA, DOWN).align_to(PA, LEFT)
        self.play(Write(eqn), run_time = 5, rate_func = linear)

        gr = VGroup(eqn, l11, l22, eq)


        self.play(FadeOut(lines), FadeOut(gr))
        self.play(dots.animate.become(dotsCopy))


        self.fDot = fDot
        self.sDot = sDot
        self.fDotLabel = fDotLabel
        self.sDotLabel = sDotLabel
        self.plane = plane
        self.movingDot = movingDot
        self.movingDotLabel = movingDotLabel

        pass
    

    def ellips(self):

        self.play(self.fDotLabel.animate.next_to(self.fDot, DOWN), self.sDotLabel.animate.next_to(self.sDot, DOWN))
        
        self.movingDot.set_z_index(120)
        first = self.fDot.get_center()
        second = self.sDot.get_center()
        e = .7
        ae = (second[0] - first[0]) / 2
        a = ae / e
        midPoint = (first + second) / 2
        b = a * sqrt(1 - e ** 2)
        ellips = Ellipse(width= 2 * a, height= 2 * b).move_to(midPoint).set_color(self.dotColor)

        obj = DashedVMobject(ellips, 2 * self.dashC).set_stroke(BLACK, width = 5).set_z_index(6)

        self.add(obj)

        dot : Dot = self.movingDot
        self.play(dot.animate.move_to(ellips.point_at_angle(0)))

        l1 = Line()
        l2 = Line()
        def l1Updater(mob):
            mob.become(Line(self.fDot.get_center(), dot.get_center()))
        def l2Updater(mob):
            mob.become(Line(dot.get_center(), self.sDot.get_center()))
        
        l1.add_updater(l1Updater)
        l2.add_updater(l2Updater)
        self.add(l1, l2)

        def updater(mob):
            c = ellips.get_end()
            mob.move_to(c)

        dot.add_updater(updater)

        self.play( Create(ellips),
         run_time = 3)
        
        ellips2 = ellips.copy().set_z_index(100).set_color(YELLOW)
        self.play(Create(ellips2))

        dot.clear_updaters()

        x = ValueTracker(0)
        dot.add_updater(lambda y : dot.move_to(ellips.point_at_angle(x.get_value())))
        self.play(x.animate.set_value(PI / 4))
        dot.clear_updaters()


        # eqnText = r""

        # x = ValueTracker()

        # dots = VGroup()
        


        l1.remove_updater(l1Updater)
        l2.remove_updater(l2Updater)


        group = VGroup(self.fDot, self.fDotLabel, self.sDot, self.sDotLabel, self.movingDot, self.movingDotLabel, ellips, ellips2, obj, l1, l2)

        self.play(group.animate.scale(.7).shift(4 * LEFT))

        l1c = l1.copy().set_color(ORANGE).reverse_direction()
        l2c = l2.copy().set_color(ORANGE)
        
        self.play(Create(l1c))
        fText = MathTex(r"PA").scale(.6).move_to( 1 * UP)
        self.play(l1c.animate.become(fText))
        
        plus = MathTex(r" + ").scale(.6).next_to(fText)
        self.play(Write(plus))
        self.play(Create(l2c))
        sText = MathTex(r"PB").scale(.6).next_to(plus)
        self.play(l2c.animate.become(sText))
        eqa = MathTex(r" =  c").scale(.6).next_to(sText)
        self.play(Write(eqa))
        eqnText = r"""
        &{\Rightarrow}{\sqrt{(x - 2)^2 + (y - 1)^2}} + {\sqrt{(x - 7)^2 + (y - 1)^2}} = c 
        """    
        eqn = MathTex(eqnText).scale(.6).next_to(fText, DOWN).align_to(fText, LEFT)
        self.play(Write(eqn), run_time = 3)

        group.add(eqn, l1c, l2c, plus, eqa)

        self.play(FadeOut(group))
        self.remove(eqn, l1c, l2c, plus, eqa)


    def parabolaEqn(t):
        return [Locus.a * t **2 , Locus.a * 2 * t, 0]
   
    def parabola(self):
        plane = NumberPlane(
            # x_range=[-5, 10, 1],
            # y_range=[-20, 30, 5],
            # y_length=12,
            axis_config = {"include_numbers" : True}
        )
        self.play(FadeIn(plane))

        a = Locus.a
        fontScale = .7
        centerDot = Dot([a, 0, 0]).set_color(self.fixedPointColor)
        centerDotLabel = MathTex(r"S(1, 0)").next_to(centerDot, UP).scale(fontScale)


        movingDot : Dot = Dot(Locus.parabolaEqn(1.5)).set_color(self.dotColor).set_z_index(140)
        movingDotLabel = MathTex(r"P(x, y)").next_to(movingDot, RIGHT).scale(fontScale)


        line = Line([-1, -20, 0], [-1, 20, 0]).set_color(self.fixedPointColor)
        lineEqn = MathTex(r"x = -1").next_to(line , LEFT).scale(fontScale).shift(UP)

        self.play(Create(VGroup(centerDot,line)))
        self.play(Write(VGroup(centerDotLabel, lineEqn)))
        

        axes = plane.get_axes()
        self.add(axes)


        self.play(FadeIn(movingDot))
        self.play(Write(movingDotLabel))




        self.graph = ParametricFunction(Locus.parabolaEqn, [-1.5,1.5]).reverse_direction().set_color(self.dotColor)
        
        l1 = Line(centerDot.get_center(), movingDot.get_center())
        l1.add_updater(lambda y : l1.become(Line(centerDot.get_center(), movingDot.get_center())))
        self.play(Create(l1))
        
        center = movingDot.get_center()
        end = center.copy()
        end[0] = -1
        l2 = Line(center, end)
        def l2Updater(mob):
            center = movingDot.get_center()
            end = center.copy()
            end[0] = -1
            l2.become(Line(end, center))    

        self.play(Create(l2))
        l2.add_updater(l2Updater)
        l2Label = MathTex(r"A(-1, y)").scale(fontScale).next_to(l2, LEFT)
        l2Label.add_updater(lambda y : l2Label.next_to(l2, LEFT))
        self.play(Write(l2Label))
        self.play(FadeOut(plane))

        movingDot.add_updater(lambda y : movingDot.move_to(self.graph.get_end()))
        movingDotLabel.add_updater(lambda y : movingDotLabel.next_to(movingDot.get_center(), RIGHT))

        dottedGraph = DashedVMobject(self.graph,self.dashC).set_stroke(BLACK, 5, 1).set_z_index(121)
        self.add(dottedGraph)

        self.play(Create(self.graph))

        graph2 = self.graph.copy().set_color(YELLOW).set_z_index(130)
        self.play(Create(graph2))


        movingDot.clear_updaters()
        
        x = ValueTracker(-1.5)
        movingDot.add_updater(lambda y : movingDot.move_to(Locus.parabolaEqn(x.get_value())))

        self.play(x.animate.set_value(1))      

        movingDot.clear_updaters()
        l1.clear_updaters()
        l2.clear_updaters()
        l2Label.clear_updaters()

        self.play(centerDotLabel.animate.next_to(centerDot, RIGHT))

        dots = VGroup(movingDot, movingDotLabel, centerDot, centerDotLabel)
        dotsCopy = dots.copy()
        lines = VGroup(line, lineEqn, l1, l2, l2Label)
        curves = VGroup(self.graph, graph2, dottedGraph)
        self.play(VGroup(dots, lines, curves).animate.scale(.7).shift(3 * LEFT))  

        l1c = l1.copy().set_color(ORANGE).reverse_direction()
        l2c = l2.copy().set_color(ORANGE).reverse_direction()
        PS = MathTex(r"PS").scale(.6).move_to(UP)
        eq = MathTex(r" = ").scale(.6).next_to(PS, RIGHT)
        PA = MathTex(r"PA").scale(.6).next_to(eq, RIGHT)
        self.play(Create(l1c))
        self.play(l1c.animate.become(PS))
        self.play(Write(eq))
        self.play(Create(l2c))
        self.play(l2c.animate.become(PA))

        eqnText = r"""
                    &{\Rightarrow}{\sqrt{(x - 1)^2 + (y - 0)^2}} = {\sqrt{(x + 1)^2 + (y - y)^2}} 
        """
        
        eqn = MathTex(eqnText).scale(.6).next_to(PS, DOWN).align_to(PS, LEFT)
        self.play(Write(eqn), run_time = 3, rate_func = linear)

        self.play(FadeOut(VGroup(eqn, lines, curves, dots, l1c, l2c, eq)))
        self.remove(eq, eqn, l1c, l2c)

        # self.play(dots.animate.become(dotsCopy))

        pass


    def introText(self):
        banglaText = Text("সঞ্চারপথ", font = self.font ).set_color_by_gradient(BLUE, GREEN, GOLD).scale(1.2).shift(.5 * UP)
        englishText = Text("Locus", font = self.engFont).set_color_by_gradient(BLUE, GREEN, GOLD).scale(1.2).shift(.5 * DOWN)
        textGroup = VGroup(banglaText, englishText)

        self.play(Write(banglaText), run_time = 1.5)
        self.play(Write(englishText), run_time = 1.5)

        self.wait(1)
        self.play(textGroup.animate.shift(3 * UP + 3.5 * LEFT).scale(.7))
        self.introTextGroup = textGroup
        # self.play(FadeOut(textGroup, shift = 2 * UP))
        return textGroup

    def createAxis(self):
        plane = NumberPlane(

        )
        self.axes = plane.get_axes()
        self.play(FadeIn(self.axes), run_time = 1)
        pass


    def roseCurveFunction(t):
        a = 3
        b = 3
        return [a * cos(b * t) * cos(t) ,a * cos(b * t) * sin(t), 0 ]

    def roseCurve(self):
        self.curve = ParametricFunction(Locus.roseCurveFunction, t_range=[0, PI]).set_color(self.dotColor)
        self.circle = Circle(self.dot.get_center()[0]).set_color(YELLOW)
        dotCopy = self.dot.copy().set_color(YELLOW)
        dotLabelCopy = self.dotLabel.copy()
        self.dot.set_z_index(5)

        dotCopy.add_updater(lambda _ : dotCopy.move_to(self.circle.get_end()))
        dotLabelCopy.add_updater(lambda _ : dotLabelCopy.next_to(dotCopy, UP))
        self.add(dotCopy, dotLabelCopy)
        self.dot.add_updater(lambda x : self.dot.move_to(self.curve.get_end()))
        self.play(Create(self.curve), Create(self.circle), run_time = 3)
        self.dot.clear_updaters()
        dotCopy.clear_updaters()
        dotLabelCopy.clear_updaters()
        self.remove(dotCopy, dotLabelCopy)

    def createDot(self):
        self.dot = Dot(Locus.roseCurveFunction(0)).set_color(self.dotColor)
        self.dotLabel = MathTex(r"P").scale(.7).next_to(self.dot, UP)
        self.dotLabel.add_updater(lambda x : self.dotLabel.next_to(self.dot, UP))
        self.play(Create(self.dot), FadeIn(self.dotLabel))
        # self.play(Create(self.dotLabel))


    def cleanUpRoseCurve(self):
        self.dotLabel.clear_updaters()
        self.play(FadeOut(VGroup(self.curve, self.dot, self.axes, self.dotLabel, self.circle, self.introTextGroup)))


    def createDotOnNumberPlane(self):
        coord = [2, 2, 0]
        p = self.plane.c2p(*coord)
        dot = Dot(p).set_fill(self.dotColor)
        
        pointLabel = MathTex(r'P(x, y)').scale(.7).next_to(dot, RIGHT)
        pointLabel.add_updater(lambda y : pointLabel.next_to(dot, RIGHT))
        self.play(Create(dot))
        self.play(FadeIn(pointLabel))
        # self.play(FadeOut(pointLabel))
        self.dot = dot
        self.dotLabel = pointLabel

    def createNumberPlane(self):
        plane = NumberPlane(
            # x_range=[-2, 13, 1],
            # y_range=[-2, 6, 1]
        )
        self.play(Create(plane), run_time = 2)

        axes = plane.get_axes().copy()
        self.add(axes)
        self.plane = plane
        self.axes = axes
        
    def RemoveNumberPlane(self):
        self.play(Uncreate(self.plane), run_time = 1.5)
        
    
    def transitionToCircleByBezier(self):
        self.circleStartPoint = Circle(radius=self.circleRadius).point_at_angle(PI / 4)
        end = self.circleStartPoint
        start = self.dot.get_center()
        m1 = start + (1.5 * LEFT + .5 * DOWN)
        m2 = m1 + (LEFT)
        self.bezier = CubicBezier(start, m1, m2, end).set_stroke(self.dotColor)
        self.bezierDashed = DashedVMobject(self.bezier, self.dashC).set_color(BLACK).set_z_index(2)
        self.add(self.bezierDashed)
        self.dot.set_z_index(5)
        self.dot.add_updater(lambda x : self.dot.move_to(self.bezier.get_end()))
        self.play(Create(self.bezier), run_time = 1.5, rate_func = linear)
        # self.wait(1)
        # self.play(FadeOut(VGroup(self.bezierDashed,self.bezier)))
    
    def circleLocus(self):
        rotationAngle = .25 * PI
        radius = self.circleRadius

        origin = Dot().set_color(self.fixedPointColor)
        originLabel = MathTex(r"O(0, 0)").scale(.7).next_to(origin, RIGHT + .5 * DOWN)
        self.play(Create(origin), FadeOut(VGroup(self.bezierDashed,self.bezier)))
        self.play(Write(originLabel))
        self.play(Uncreate(self.plane), run_time = 1.5)

        circle = Circle(radius).rotate(rotationAngle).set_stroke(self.dotColor, opacity=1)
        point = circle.point_at_angle(rotationAngle)

        vector = Vector(point)
        
        self.dot.add_updater(lambda x : self.dot.move_to(circle.get_end()))
        vector.add_updater(lambda x : vector.become(Vector(circle.get_end())))

        self.play(Create(vector))


        dottedCircle = DashedVMobject(circle.copy().set_stroke(BLACK, opacity = 1), self.dashC).set_z_index(2)
        self.axes.set_z_index(3)
        self.dot.set_z_index(15)
        self.add(dottedCircle)

        self.play(Create(circle), run_time = 2)
        nCircle = circle.copy().set_z_index(10).set_stroke(YELLOW, opacity = 1)
        self.play(Create(nCircle))
        self.remove(circle)
        circle = nCircle
        self.remove(dottedCircle)
        
        brace = Brace(vector, direction=vector.copy().rotate(PI/2).get_unit_vector(), buff=.05, sharpness=1)

        brText = brace.get_tex(r"a")
        
        self.play(Write(VGroup( brace, brText)), run_time = 3)


        circleGroup = VGroup(nCircle)
        braceGroup = VGroup(brace, brText)
        points = VGroup(self.dot, self.dotLabel, origin, originLabel)
        axis = self.axes
        xLine = Line([-39, 0, 0], [49, 0, 0]).set_stroke(color = self.axes.get_stroke_color(), width=self.axes.get_stroke_width()).set_z_index(-1)
        self.add(xLine)
        # brace.clear_updaters()
        vector.clear_updaters()

        allGroup = VGroup(circleGroup, braceGroup, points, axis, vector)
        self.play(allGroup.animate.shift(LEFT))

        firstText = MathTex(r"PO").scale(.6).shift(4 * RIGHT + 3 * UP)
        v2 = vector.copy()
        self.add(v2)
        self.play(v2.animate.become(firstText))
        secondText = MathTex(r" = a").next_to(firstText, RIGHT).scale(.6).shift(.2 * LEFT)
        self.play(Write(secondText))


        eqnText = r"""
                &{\Rightarrow}{\sqrt{(x - 0)^2 + (y - 0)^2}} = a
                \\&{\Rightarrow}x^2 + y^2 = a^2
        """
        

        eqn = MathTex(eqnText).align_to(firstText, LEFT).next_to(firstText, DOWN).scale(.6)
        self.play(Write(eqn), run_time = 4, rate_func = linear)

        allGroup.add(eqn, v2, xLine, secondText)
        self.play(FadeOut(allGroup))
        self.remove(eqn, v2, secondText, xLine)
        self.wait(1)

        pass


    def hyperbola(self):
        plane = NumberPlane(
            # x_range=[-5, 10, 1],
            # y_range=[-20, 30, 5],
            # y_length=12,
            axis_config = {"include_numbers" : True}
        )
        self.play(FadeIn(plane))
        axisLine = Line([0, -30, 0], [0, 30, 0]).set_color(self.fixedPointColor)
        a = 2
        e = 1.5
        b = a * sqrt((e ** 2) - 1)

        def hyperbolaeqn(t):
            return [a * (1 / cos(t)) ,  b * tan(t), 0]

        
        

        graphL = ParametricFunction(hyperbolaeqn, [2.18, PI + PI - 2.18]).reverse_direction().set_color(self.dotColor)
        graphR = ParametricFunction(hyperbolaeqn, [-.96, .96]).reverse_direction().set_color(self.dotColor)
        # graphR = graphL.apply_function(lambda p : p + 2)

        fDot = Dot( [- a * e, 0, 0]).set_color(self.fixedPointColor)
        fDotLabel = MathTex(r"S'(-3, 0)").scale(.7).next_to(fDot, DOWN)
        sDot = Dot([a * e, 0, 0]).set_color(self.fixedPointColor)
        sDotLabel = MathTex(r"S(3, 0)").scale(.7).next_to(sDot, DOWN)

        self.play(Create(VGroup(fDot, sDot)))
        self.play(Write(VGroup(fDotLabel, sDotLabel)))

        self.play(Create(axisLine))

        axes = plane.get_axes()
        self.add(axes)
        axisLine.set_z_index(1000)
        axisLine.set_z_index(1)

        mDot = Dot(hyperbolaeqn(2 * PI - 2.18)).set_color(self.dotColor).set_z_index(150)
        mDotLabel = MathTex(r"P(x, y)").scale(.7).next_to(mDot, RIGHT)
        self.play(Create(mDot))
        self.play(Write(mDotLabel))

        l1 = Line(fDot.get_center(), mDot.get_center()).set_z_index(11)
        l2 = Line(mDot.get_center(), sDot.get_center()).set_z_index(11)
        self.play(Create(l1))
        self.play(Create(l2))
        self.play(FadeOut(plane))

        l1.add_updater(lambda _ : l1.become(Line(fDot.get_center(), mDot.get_center())))
        l2.add_updater(lambda _ : l2.become(Line(mDot.get_center(), sDot.get_center())))


        mDot.add_updater(lambda y : mDot.move_to(graphL.get_end()))
        mDotLabel.add_updater(lambda y : mDotLabel.next_to(mDot, RIGHT))

        lDashed = DashedVMobject(graphL, self.dashC).set_color(BLACK).set_z_index(10)
        rDashed = DashedVMobject(graphR, self.dashC).set_color(BLACK).set_z_index(10)
        self.add(lDashed, rDashed)
        
    
        self.play(Create(graphL), Create(graphR))
        graphLC = graphL.copy().set_color(YELLOW).set_z_index(100)
        graphRC = graphR.copy().set_color(YELLOW).set_z_index(100)

        self.play(Create(graphLC), Create(graphRC))

        mDot.clear_updaters()
        x = ValueTracker(2.18)
        mDot.add_updater(lambda _ : mDot.move_to(hyperbolaeqn(x.get_value())))
        self.play(x.animate.set_value(2 * PI - 2.18 - .4 ))
        mDot.clear_updaters()
        l1.clear_updaters()
        l2.clear_updaters()
        
        group = VGroup(mDot, fDotLabel, fDot, sDot, sDotLabel, mDotLabel, l1, l2, graphR, graphL,
        graphLC, graphRC, lDashed, rDashed, axisLine)
        self.play(group.animate.scale(.7).shift(3 * LEFT))

        l1c = l2.copy().set_color(ORANGE)
        l2c = l1.copy().set_color(ORANGE).reverse_direction()
        PS = MathTex(r"PS").scale(.6).move_to(UP)
        minus = MathTex(r" - ").scale(.6).next_to(PS, RIGHT)
        PSP = MathTex(r"PS'").scale(.6).next_to(minus, RIGHT)
        eqc = MathTex(r" = c").scale(.6).next_to(PSP, RIGHT)
        self.play(Create(l1c))
        self.play(l1c.animate.become(PS))
        self.play(Write(minus))
        self.play(Create(l2c))
        self.play(l2c.animate.become(PSP))
        self.play(Write(eqc))

        
        eqnText = r"""
            {\Rightarrow}{\sqrt{(x - 3)^2 + (y - 0)^2}} - {\sqrt{(x + 3)^2 + (y - 0)^2}} = c 
             
        """
        
        eqn = MathTex(eqnText).scale(.6).next_to(PS, DOWN).align_to(PS, LEFT)
        self.play(Write(eqn), run_time = 3, rate_func = linear)
        group.add(eqn, l1c, l2c, minus, eqc)
        self.play(FadeOut(group))
        self.remove(eqn, l1c, l2c, minus, eqc)

        # self.remove(l1, l2)
        # self.play(mDot.animate.move_to(hyperbolaeqn(.96)))
        # self.add(l1, l2)
        # mDot.add_updater(lambda y : mDot.move_to(graphR.get_end()))

        # self.play(Create(graphR))

        

    def endText(self):
        cya = Text("Thank you for watching", font=self.engFont, font_size=40).set_color_by_gradient(BLUE, GREEN, GOLD).move_to(ORIGIN + 2 * UP)
        ins = Text("Instructor",font=self.engFont, font_size=30).set_color_by_gradient(GOLD, ORANGE).next_to(cya,2.5 * DOWN)
        insName = Text("Kazi Rakibul Hasan",font=self.engFont, font_size=30).set_color_by_gradient(GOLD, ORANGE).next_to(ins, DOWN)

        anim = Text("Animator",font=self.engFont, font_size=30).set_color_by_gradient(GOLD, ORANGE).next_to(insName,2.5 * DOWN)
        animName = Text("Abdur Rafi",font=self.engFont, font_size=30).set_color_by_gradient(GOLD, ORANGE).next_to(anim,  DOWN)
        self.play(Write(VGroup(cya, ins, insName, anim, animName)))



    def construct(self):
        self.introText()
        self.createAxis()
        self.createDot()
        self.roseCurve()
        self.cleanUpRoseCurve()
        self.createNumberPlane()
        self.createDotOnNumberPlane()
        # self.RemoveNumberPlane()
        self.transitionToCircleByBezier()
        self.circleLocus()


        self.locusLine()
        self.ellips()

        self.parabola()
        self.hyperbola()
        self.endText()

        # dots = path
        # path = VMobject()


        # def dotUpdaters(neg):
        #     def updater(mob, dt):
        #         cord = [0,0,0]
        #         scale = 2
        #         cord[0] += ((random() * dt * scale))
        #         cord[1] += ((random())* dt * scale / 2)
        #         if neg:
        #             cord[1] = -1 * cord[1]
        #         dot.shift(cord)
        #     return updater

        # posUpdater = dotUpdaters(False)
        # dot.add_updater(posUpdater)
        # # dot.remo
        # self.wait(1.5)
        # dot.remove_updater(posUpdater)

        # negUpdater = dotUpdaters(True)
        # dot.add_updater(negUpdater)
        # self.wait(1.5)
        # dot.remove_updater(negUpdater)


        pass