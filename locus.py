from math import sqrt
from manim import *
from random import *

class Locus(Scene):

    def locusLine(self):
        plane = NumberPlane(
            x_range=[-5, 10, 1],
            y_range=[-4, 6, 1],
            axis_config = {"include_numbers" : True}
        )
        self.play(Create(plane))
        fDot = Dot(plane.c2p(2, 1, 0)).set_stroke(YELLOW)
        sDot = Dot(plane.c2p(7, 1, 0)).set_stroke(YELLOW)

        self.play(Create(fDot), Create(sDot))

        self.play(FadeOut(plane))
        shift = 2 * LEFT
        plane = plane.shift(shift)
        self.play(VGroup(fDot, sDot).animate.shift(shift))

        startPoint = plane.c2p(4.5, 4, 0) 
        endPoint = plane.c2p(4.5, -2, 0)

        movingDot = Dot(startPoint).set_z_index(4)
        self.play(Create(movingDot))

        line = Line(startPoint, endPoint).set_stroke(ORANGE)

        dottedLine = DashedVMobject(Line(startPoint, endPoint).set_stroke(BLACK, 5, opacity=1)).set_z_index(2)
        
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
        self.play(Create(line))

        line2 = line.copy().set_z_index(6)
        movingDot.remove_updater(dotUpdater)
        self.play(Create(line2))
        l1.remove_updater(l1Updater)
        l2.remove_updater(l2Updater)

        self.play(FadeOut(VGroup(movingDot, line, line2, dottedLine, l1, l2 )))
        self.fDot = fDot
        self.sDot = sDot
        self.plane = plane
        pass
    
    def ellips(self):
        dot = Dot().set_fill(ORANGE, opacity=1).set_z_index(5)
        self.add(dot)

        ellips = Ellipse(5, 2)

        obj = (DashedVMobject(ellips,dashed_ratio=.5, num_dashes=60).set_stroke(BLACK).set_z_index(6))
        self.add(obj)

        
        fDot = Dot(LEFT)
        sDot = Dot(RIGHT)
        self.add(fDot, sDot)

        l1 = Line()
        l2 = Line()
        def l1Updater(mob):
            mob.become(Line(fDot.get_center(), dot.get_center()))
        def l2Updater(mob):
            mob.become(Line(dot.get_center(), sDot.get_center()))
        
        l1.add_updater(l1Updater)
        l2.add_updater(l2Updater)
        self.add(l1, l2)

        # dot1 = Dot()

        def updater(mob):
            c = ellips.get_end()
            mob.move_to(c)
        # self.add(dot1)
        # dot1.add_updater(updater)
        
        dot.add_updater(updater)

        self.play( Create(ellips),
         run_time = 3)
    

    def ellips2(self):
        first = self.fDot.get_center()
        second = self.sDot.get_center()
        e = .7
        ae = (second[0] - first[0]) / 2

        a = ae / e

        midPoint = (first + second) / 2
        b = a * sqrt(1 - e ** 2)
        print(a, b)
        ellips = Ellipse(width= 2 * a, height= 2 * b).move_to(midPoint)
        # self.play(Create(ellips))

        obj = (DashedVMobject(ellips,dashed_ratio=.5, num_dashes=60).set_stroke(BLACK).set_z_index(6))
        self.add(obj)

        dot = Dot(ellips.point_at_angle(0))
        self.add(dot)

        l1 = Line()
        l2 = Line()
        def l1Updater(mob):
            mob.become(Line(self.fDot.get_center(), dot.get_center()))
        def l2Updater(mob):
            mob.become(Line(dot.get_center(), self.sDot.get_center()))
        
        l1.add_updater(l1Updater)
        l2.add_updater(l2Updater)
        self.add(l1, l2)

        # dot1 = Dot()

        def updater(mob):
            c = ellips.get_end()
            mob.move_to(c)
        # self.add(dot1)
        # dot1.add_updater(updater)
        
        dot.add_updater(updater)

        self.play( Create(ellips),
         run_time = 3)
        
        ellips2 = ellips.copy().set_z_index(100)
        self.play(Create(ellips2))
        l1.remove_updater(l1Updater)
        l2.remove_updater(l2Updater)
    


    def circleLocus(self):
        rotationAngle = .25 * PI
        radius = 1.5
        circle = Circle(radius).rotate(rotationAngle)
        point = circle.point_at_angle(rotationAngle)
        self.play(self.dot.animate.move_to(point))

        vgroups = VGroup()

        vector = Vector(point)
        
        def dotUpdater(mob):
            self.dot.move_to(circle.get_end())
        self.dot.add_updater(dotUpdater)

        def vectorUpdater(mob):
            vector.become(Vector(circle.get_end()))
        vector.add_updater(vectorUpdater)
        self.add(vector)

        # brace = Brace(vector, direction=vector.copy().rotate(PI/2).get_unit_vector())
        
        # def braceUpdater(mob):
        #     brace.become(Brace(vector, direction=vector.copy().rotate(PI/2).get_unit_vector()))
        
        # brace.add_updater(braceUpdater)
        # txt = brace
        # self.add(brace)


        dottedCircle = DashedVMobject(circle.copy().set_stroke(BLACK, width=4)).set_z_index(2)
        self.axes.set_z_index(3)
        self.dot.set_z_index(15)
        self.add(dottedCircle)

        self.play(Create(circle))
        # self.play(Uncreate(dottedCircle))
        nCircle = circle.copy().set_z_index(10)
        self.play(Create(nCircle))

        circle = nCircle

        self.remove(dottedCircle)

        pointLabelScale = .6
        gap = .2

        dotLabel = MathTex(r"P(x, y)").scale(pointLabelScale).move_to(point).align_to(self.dot,LEFT).shift(gap * RIGHT)
        originLabel = MathTex(r"O(0, 0)").scale(pointLabelScale).move_to(ORIGIN).align_to(Dot(ORIGIN),LEFT).shift(gap * (RIGHT + DOWN))


        brace = Brace(vector, direction=vector.copy().rotate(PI/2).get_unit_vector(), buff=.05, sharpness=1)

        brText = brace.get_tex(r"a")
        
        self.play(Create(VGroup(dotLabel, originLabel, brace, brText)))

        
        eqn = MathTex(r"&PO = a\\&{\Rightarrow}{\sqrt{(x - 0)^2 + (y - 0)^2}} = a\\&{\Rightarrow}x^2 + y^2 = a^2").scale(1.15 * pointLabelScale).shift(5 * RIGHT + 2 * UP)
        self.play(Create(eqn))

        # self.play(FadeOut(VGroup(eqn, brace, brText, dotLabel, originLabel,circle, vector, circle, self.dot)))
        # eqn2 = MathTex(r"")

        pass
    

    def parabola(self):
        plane = NumberPlane(
            x_range=[-5, 10, 1],
            y_range=[-20, 30, 5],
            y_length=12,
            axis_config = {"include_numbers" : True}
        )
        self.play(Create(plane))
        sx = 7
        point = plane.c2p(sx, 5, 0)
        dot = Dot(point)
        line = Line(plane.c2p(*[1, 50, 0]), plane.c2p(*[1, -50, 0]))
        self.play(Create(dot), Create(line))
        self.play(FadeOut(plane))
        shift = 3 * LEFT
        plane.shift(shift)
        self.play(VGroup(dot, line).animate.shift(shift))

        def createF(neg):
            def par(x):
                sign = 1
                if neg:
                    sign = -1
                return sign * sqrt(4 * 3 *(x - 4)) + 5
            return par
        grP = plane.plot(createF(False), [4, 12]).reverse_direction().set_stroke(ORANGE, opacity=1)
        dot = Dot(plane.c2p(12, createF(False)(12), 0)).set_z_index(20)
        self.add(dot)
        grPDashed = DashedVMobject(grP, 30,.2)
        grPDashed.set_stroke(BLACK, opacity=1).set_z_index(5)
        self.add(grPDashed)
        dot.add_updater(lambda x : dot.move_to(grP.get_end()))
        self.play(Create(grP))
        dot.clear_updaters()
        grN = plane.plot(createF(True), [4, 12]).set_stroke(ORANGE, opacity=1)
        grNDashed = DashedVMobject(grN, 30, .2)
        grNDashed.set_stroke(BLACK, opacity=1).set_z_index(5)
        self.add(grNDashed)
        dot.add_updater(lambda x: dot.move_to(grN.get_end()))
        self.play(Create(grN))
        grPC = grP.copy().set_z_index(30)
        self.play(Create(grPC))
        grNC = grN.copy().set_z_index(40)
        self.play(Create(grNC))
        pass


    def construct(self):
        # self.ellips()
        # self.locusLine()

        # circle Locus
        plane = NumberPlane(
            # x_range=[-2, 13, 1],
            # y_range=[-2, 6, 1]
        )
        self.play(Create(plane))

        axes = plane.get_axes().copy()
        self.add(axes)
        
        coord = [2, 2, 0]
        p = plane.c2p(*coord)
        dot = Dot(p).set_fill(YELLOW)
        
        pointLabel = MathTex(r'P(x, y)').move_to(dot).align_to(dot, LEFT).shift(.2 * RIGHT)


        self.play(Create(dot))
        self.play(FadeIn(pointLabel))
        self.play(FadeOut(pointLabel))

        self.play(Uncreate(plane))

        self.axes = axes
        self.dot = dot
        self.circleLocus()

        # self.play(self.axes.animate.shift(2 * LEFT))
        self.play(*[FadeOut(i) for i in self.mobjects])

        self.locusLine()
        self.ellips2()

        self.play(*[FadeOut(i) for i in self.mobjects])
        self.parabola()
        
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