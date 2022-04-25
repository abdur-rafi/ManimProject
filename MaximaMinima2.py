from manim import *
from manim.mobject.mobject import T
import numpy as np


class Maxima(ZoomedScene):
    
    banglaFont =  'Li Shamim Cholontika UNICODE'
    engFont = 'Zuka Doodle'


    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.05,
            zoomed_display_height=3,
            zoomed_display_width=3,
            image_frame_stroke_width=1,
            zoomed_camera_config={
                "default_frame_stroke_width": 1,
                },
            
            **kwargs
        )

    
    def incrDecr(self):
        # tText = Text("Function", font_size=40).set_color_by_gradient(GREEN, BLUE)
        # tText.move_to(3.2 * UP)

        def createAxis():
            axis_config = {
                "tick_size" : .05,
                "include_numbers" : True,

            }
            axes = Axes(
                x_range=[-5, 5, 1],
                y_range =[-5, 5, 1],
                x_axis_config=axis_config,
                y_axis_config=axis_config,
                y_length=config.frame_height + 1

            ).set_color_by_gradient(RED, BLUE).scale(.8)
            self.play(Create(axes))
            
            self.axes = axes
        
        curveStrokeWidth = DEFAULT_STROKE_WIDTH / 3

        def curveCreate(func):
            
            
            curve = self.axes.plot(func, x_range=[-4, 4]).set_color(BLUE).set_stroke(width = curveStrokeWidth)
            # self.play(Create(curve))
            return curve

        # self.play(Write(tText))

        createAxis()


        # inc = Text("Increasing", font_size=30).set_color_by_gradient(BLUE, TEAL)
        # inc.move_to(4 * LEFT + UP)
        # self.play(Write(inc))
        curve = curveCreate(lambda x : np.exp(x / 3))
        self.play(Create(curve))

        # dec = Text("Decreasing", font_size=30).set_color_by_gradient(BLUE, TEAL)
        # dec.next_to(inc, DOWN).align_to(inc, LEFT)
        # self.play(Write(dec))
        curvePr = curve
        curve = curveCreate(lambda x : np.exp(-x / 3))
        self.play(curvePr.animate.become(curve))

        
        # const = Text("Constant", font_size=30).set_color_by_gradient(BLUE, TEAL)
        # const.next_to(dec, DOWN).align_to(dec, LEFT)
        # self.play(Write(const))
        curve = curveCreate(lambda x : 2)
        self.play(curvePr.animate.become(curve))

        def parabolaFunc(x):
            return -.3 * ( x ** 2 - 4)

        curve = curveCreate(parabolaFunc)
        self.play(curvePr.animate.become(curve))

        def highlightSide(side):
            axes : Axes = self.axes
            x = 5
            y = 5
            if side == "left":

                points = [[0, -y, 0], [-x, -y,0 ], [-x, y, 0], [0, y, 0]]
            else:
                points = [[0, -y, 0], [x, -y,0 ], [x, y, 0], [0, y, 0]]

            box = Polygon(*[axes.c2p(*i) for i in points]).set_stroke(width=0).reverse_direction()
            box.set_fill((TEAL, BLUE), .3)
            # box.set_
            return box
        
        axes : Axes = self.axes

        box = highlightSide("left")
        self.play(FadeIn(box))
        # incCopy = inc.copy()
        # incCopy.next_to(box, DOWN).scale(.7)
        # self.play(Write(incCopy))
        # boxPr = box
        self.remove(box)
        box = highlightSide("right")
        box.set_fill((BLUE, RED),.3)
        self.play(FadeIn(box))
        
        # decCopy = dec.copy()
        # decCopy.next_to(box, DOWN).scale(.7)
        # self.play(Write(decCopy))
        
        # self.play(FadeOut(incCopy, decCopy, box, boxPr, dec, const))
        self.play(FadeOut(box))
        # self.play(VGroup(axes, curvePr).animate.move_to(ORIGIN) ) #, inc.animate.shift(.5 * LEFT + UP))

        Dx = .00001
        x = ValueTracker(-4)
        def getTangentPoints(func):
            x1 = x.get_value()
            p1 = axes.c2p(x1, func(x1), 0)
            p2 = axes.c2p(x1 + Dx, func(x1 + Dx), 0)
            return p1, p2

        def getTangent(func):
            p1, p2 = getTangentPoints(func)
            line = Line(p1, p2).set_length(3).set_color((GRAY, BLUE)).set_stroke(width = curveStrokeWidth)
            return line

        tangentDot = Dot(axes.c2p(*[x.get_value(), parabolaFunc(x.get_value()), 0]), DEFAULT_DOT_RADIUS / 6).set_color(YELLOW).set_z_index(2)
        self.play(FadeIn(tangentDot))
        tangentDot.add_updater(lambda _: tangentDot.move_to(axes.c2p(*[x.get_value(), parabolaFunc(x.get_value()), 0])))
        tangentLine = getTangent(parabolaFunc)
        self.play(Create(tangentLine))
        
        def tangentTriangle(func, side):
            x1 = x.get_value()
            dx = .1
            p1 = axes.c2p(x1, func(x1), 0)
            p2 = axes.c2p(x1 + dx, func(x1 + dx), 0)
            p3 = p2.copy()
            p3[1] = p1[1]
            base = Line(p1,p3).set_stroke(width=curveStrokeWidth / 2).set_color((BLUE, PINK))
            s = DOWN
            if( side == 'right'):
                s = UP
            baseText = MathTex(r"dx(+)", font_size = 3).next_to(base, s, buff = .01)
            perpandicular = Line(p3, p2).set_stroke(width=curveStrokeWidth / 2).set_color((BLUE, PINK))
            sign = '(+)'
            if side == 'right':
                sign = '(-)'
            
            perpText = MathTex(r"dy" + sign, font_size = 3).next_to(perpandicular, RIGHT, buff = .01)

            return VGroup(base, perpandicular,baseText, perpText).set_z_index(3)
        
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        shiftCoeff = .04
        frame.move_to(tangentDot)
        frame.scale(1.5).align_to(tangentDot, DOWN + LEFT).shift(shiftCoeff * DOWN)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.scale(.8)
        # zoomed_display.shift(DOWN)

        self.play(Create(frame))
        self.play(self.get_zoomed_display_pop_out_animation())
        self.activate_zooming()
        self.wait(1)

        trGroup = tangentTriangle(parabolaFunc, 'left')
        self.play(Create(trGroup))
        trGroup.add_updater(lambda _ : trGroup.become(tangentTriangle(parabolaFunc, 'left')))
        frame.add_updater(lambda _ : frame.move_to(tangentDot).align_to(tangentDot, DOWN + LEFT).shift(shiftCoeff * DOWN))
        tangentLine.add_updater(lambda _ : tangentLine.become(getTangent(parabolaFunc)))
        slopeI = MathTex(r"{\frac{dy}{dx}} > 0", font_size = 30).set_color_by_gradient(RED, ORANGE).next_to(axes,LEFT ).shift(UP)
        self.play(Write(slopeI))
        self.play(x.animate.set_value(0), run_time = 3)

        frame.clear_updaters()
        trGroup.clear_updaters()
        self.remove(trGroup)

        # dec.next_to(axes).shift(DOWN)
        # self.play(Write(dec))
        slopeD = MathTex(r"{\frac{dy}{dx}} < 0", font_size = 30).set_color_by_gradient(RED, ORANGE).next_to(axes,RIGHT ).shift(DOWN)
        self.play(Write(slopeD))
        self.play(frame.animate.move_to(tangentDot).align_to(tangentDot, UP + LEFT).shift(shiftCoeff * UP))

        frame.add_updater(lambda _ : frame.move_to(tangentDot).align_to(tangentDot, UP + LEFT).shift(shiftCoeff * UP))
        trGroup.add_updater(lambda _ : trGroup.become(tangentTriangle(parabolaFunc, 'right')))
        
        self.add(trGroup)
        self.play(x.animate.set_value(4), run_time = 3)
        

        constCurve = curveCreate(lambda x : 2)
        constCurve.set_color(YELLOW)

        self.play(Create(constCurve))
        
        slopeC = MathTex(r"{\frac{dy}{dx}} = 0", font_size = 30).set_color_by_gradient(RED, ORANGE).next_to(constCurve, UP).align_to(constCurve, RIGHT)
        # const.next_to(slope, UP).align_to(slope, RIGHT)
        # self.play(Write(const))
        self.play(Write(slopeC))

        self.wait(1)

        self.play(FadeOut(constCurve), FadeOut(slopeC, slopeD, slopeI))

        def getSlope(func):
            x1 = x.get_value()
            p1 = [x1, func(x1), 0]
            p2 = [x1 + Dx, func(x1 + Dx), 0]
            slope = (p2[1] - p1[1]) / Dx
            return [x1, slope, 0]
        
        lastPoint = getSlope(parabolaFunc)
        lines = VGroup()
        def plotSlope(_):
            nonlocal lastPoint
            sl = getSlope(parabolaFunc)
            line = Line(axes.c2p(*lastPoint), axes.c2p(*sl)).set_stroke(width=curveStrokeWidth)
            lastPoint = sl;
            self.add(line)
            lines.add(line)
        self.add(lines)
        lines.add_updater(plotSlope)
        self.play(x.animate.set_value(0), run_time = 3)

        
        frame.clear_updaters()
        trGroup.clear_updaters()
        # self.remove(trGroup)

        self.play(frame.animate.align_to(tangentDot, DOWN + LEFT).shift(shiftCoeff * DOWN))

        trGroup.add_updater(lambda _ : trGroup.become(tangentTriangle(parabolaFunc, 'left')))
        frame.add_updater(lambda _ : frame.move_to(tangentDot).align_to(tangentDot, DOWN + LEFT).shift(shiftCoeff * DOWN))

        self.play(x.animate.set_value(-4), run_time = 3)


        fx = MathTex(r"f(x)", font_size = 25).set_color(BLUE).next_to(axes, RIGHT).shift(1.5 *DOWN)
        self.play(Write(fx))
        fpx = MathTex(r"f'(x)", font_size = 25).next_to(axes, LEFT).shift(UP)
        self.play(Write(fpx))
        posLine = Line(lines[-1].get_end(), axes.c2p(0, 0, 0)).set_stroke(color = YELLOW, width = 2 * curveStrokeWidth)
        self.play(Create(posLine))
        negLine = Line(axes.c2p(0, 0, 0), lines[0].get_start() ).set_stroke(color = ORANGE, width = 2 * curveStrokeWidth)
        self.play(Create(negLine))
        self.wait(1)
        # self.play(FadeOut(*self.mobjects))
        # axes.x_axis.set_
        # self.play(Uncreate(curve))

    def turningPoint(self):
        
        sW = DEFAULT_STROKE_WIDTH / 1.5

        axis_config = {
            "tick_size" : .05,
            "include_numbers" : False,

        }
        axes = Axes(
            x_range=[-4.5 * PI, 4.5 * PI, PI],
            y_range =[-3, 3, 1],
            x_axis_config=axis_config,
            y_axis_config=axis_config,
            y_length=config.frame_height - .5

        ).set_color_by_gradient(GREEN,RED, BLUE).scale(.9)
        self.play(Create(axes))
        def cosCurveFunc(x):
            return np.cos(x)
        cosCurve = axes.plot(cosCurveFunc, x_range= [-4.1 * PI, 4.1 * PI]).set_stroke(BLUE, sW)
        self.play(Create(cosCurve))
        extremaPoints = np.linspace(-4 * PI, 4 * PI, 9).tolist()
        # print(extremaPoints)
        dots = [Dot(axes.c2p(i, cosCurveFunc(i), 0), radius=DEFAULT_DOT_RADIUS / 1.5, color= YELLOW) for i in extremaPoints]
        posEx = dots[4].copy()
        negEx = dots[5].copy()

        self.play(*[Create(i) for i in dots])
        self.add(posEx, negEx)
        self.play(FadeOut(*dots))     


        
        Dx = .00001
        x = ValueTracker(-.5 * PI)
        def getTangentPoints(func):
            x1 = x.get_value()
            p1 = axes.c2p(x1, func(x1), 0)
            p2 = axes.c2p(x1 + Dx, func(x1 + Dx), 0)
            return p1, p2

        def getTangent(func):
            p1, p2 = getTangentPoints(func)
            line = Line(p1, p2).set_length(3.5).set_color((RED,GRAY, BLUE)).set_stroke(width = sW)
            return line

        tangentDot = Dot(axes.c2p(*[x.get_value(), cosCurveFunc(x.get_value()), 0]), DEFAULT_DOT_RADIUS / 1.5).set_color(ORANGE).set_z_index(2)
        self.play(FadeIn(tangentDot))
        tangentDot.add_updater(lambda _: tangentDot.move_to(axes.c2p(*[x.get_value(), cosCurveFunc(x.get_value()), 0])))
        tangentLine = getTangent(cosCurveFunc)
        tangentLine.add_updater(lambda _ : tangentLine.become(getTangent(cosCurveFunc)))

        

        self.play(Create(tangentLine))

        
        def getSlope(func):
            x1 = x.get_value()
            p1 = [x1, func(x1), 0]
            p2 = [x1 + Dx, func(x1 + Dx), 0]
            slope = (p2[1] - p1[1]) / Dx
            return [x1, slope, 0]
        
        lastPoint = getSlope(cosCurveFunc)
        lines = VGroup()
        def plotSlope(_):
            nonlocal lastPoint
            sl = getSlope(cosCurveFunc)
            line = Line(axes.c2p(*lastPoint), axes.c2p(*sl)).set_stroke(color = tangentDot.color, width=sW)
            lastPoint = sl
            lines.add(line)
            
        lines.add_updater(plotSlope)        
        self.add(lines)



        self.play(x.animate.set_value(0))
        # lines.clear_updaters()

        self.wait()
        self.play(x.animate.set_value(.5 * PI))
        self.wait(1)
        self.play(x.animate.set_value(PI))
        self.wait(1)
        self.play(x.animate.set_value(1.5 * PI))

   
        pass

    def graph2(self):
        
        sW = DEFAULT_STROKE_WIDTH / 1.5

        axis_config = {
            "tick_size" : .05,
            "include_numbers" : False,

        }
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range =[-10, 10, 2],
            x_axis_config=axis_config,
            y_axis_config=axis_config,
            y_length=config.frame_height - .5

        ).set_color_by_gradient(RED,PURPLE,GRAY).scale(.9).set_stroke(width = sW)
        def curveFunc(x):
            return x ** 7 - 6 * x ** 5 + 9 * x ** 3 - 4 * x

        self.play(Create(axes))
        curve = axes.plot(curveFunc).set_stroke(YELLOW, sW)
        self.play(Create(curve), run_time = 2)

        
        Dx = .00001
        x = ValueTracker(-2)
        def getTangentPoints(func):
            x1 = x.get_value()
            p1 = axes.c2p(x1, func(x1), 0)
            p2 = axes.c2p(x1 + Dx, func(x1 + Dx), 0)
            return p1, p2

        def getTangent(func):
            p1, p2 = getTangentPoints(func)
            line = Line(p1, p2).set_length(3.5).set_color(WHITE).set_stroke(width = sW)
            return line

        tangentDot = Dot(axes.c2p(*[x.get_value(), curveFunc(x.get_value()), 0]), DEFAULT_DOT_RADIUS / 1.5).set_color(WHITE).set_z_index(2)
        self.play(FadeIn(tangentDot))
        tangentDot.add_updater(lambda _: tangentDot.move_to(axes.c2p(*[x.get_value(), curveFunc(x.get_value()), 0])))
        tangentLine = getTangent(curveFunc)
        tangentLine.add_updater(lambda _ : tangentLine.become(getTangent(curveFunc)))

        

        self.play(Create(tangentLine))

        
        def getSlope(func):
            x1 = x.get_value()
            p1 = [x1, func(x1), 0]
            p2 = [x1 + Dx, func(x1 + Dx), 0]
            slope = (p2[1] - p1[1]) / Dx
            return [x1, slope, 0]
        
        lastPoint = getSlope(curveFunc)
        lines = VGroup()
        def plotSlope(_):
            nonlocal lastPoint
            sl = getSlope(curveFunc)
            line = Line(axes.c2p(*lastPoint), axes.c2p(*sl)).set_stroke(color = tangentDot.color, width=sW)
            lastPoint = sl
            lines.add(line)
            
        lines.add_updater(plotSlope)        
        self.add(lines)

        self.play(x.animate.set_value(2), run_time = 10)

    

    def construct(self):
        # self.incrDecr()
        # self.turningPoint()
        self.graph2()
        pass