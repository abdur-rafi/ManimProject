from manim import *
import numpy as np

class MaximaMinima(ZoomedScene):

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

    def construct(self):
        axis_config = {
             "include_ticks" : False,
            # "include_tip" : False
        }
        axes = Axes(
            x_axis_config=axis_config,
            y_axis_config=axis_config
        ).set_color(BLUE)
        self.play(Create(axes))
        
        
        # incrGraph = plane.plot(lambda x : .1 * (x ** 3 - x ** 2 + x + 2) )
        # incrGraph.set_color(ORANGE)
        # self.play(Create(incrGraph))
        # decrGraph = plane.plot(lambda x : -1 * .1 * (x ** 3 - x ** 2 + x + 2)).set_color(YELLOW)
        # self.play(incrGraph.animate.become(decrGraph))    
        # constGraph = plane.plot(lambda x : 1).set_color(GREEN)
        # self.play(incrGraph.animate.become(constGraph))
        
        # self.remove(incrGraph)
        def parabolaFunc(x):
            return -.2 * ( x ** 2 - 4)

        funcLabel = MathTex(r"y = f(x)",font_size = 30).move_to(axes.c2p(-4, 4, 0)).set_color(ORANGE)
        parabola = axes.plot(parabolaFunc,x_range=[-5, 5]).set_color(ORANGE).set_stroke(width=DEFAULT_STROKE_WIDTH / 2)
        self.play(Create(parabola), Write(funcLabel))
        
        graphPlaneGroup = VGroup(axes, parabola)
        self.play(graphPlaneGroup.animate.scale(.5).shift(2 * UP), funcLabel.animate.shift(LEFT))
        self.play(funcLabel.animate.next_to(axes, LEFT))

        axesBottom = axes.copy()
        self.play(axesBottom.animate.shift(4 * DOWN))
        slopeLabel = MathTex(r"y = f'(x)", font_size = 30)
        self.play(slopeLabel.animate.next_to(axesBottom, LEFT))
        # self.play(Write(slopeLabel))

        lineGroup = VGroup()
        last = None

        x = ValueTracker(-4)

        dotColor = YELLOW

        dot = Dot(radius=DEFAULT_DOT_RADIUS / 2).set_color(dotColor)\
            .move_to(axes.c2p(x.get_value(), parabolaFunc(x.get_value()), 0))


        # parabola.cordi
        def getTangent(x, func, dx)->Line:
            nonlocal last, dot
            dx = max(dx, .000001)
            coord1 = axes.c2p(x, func(x), 0)
            coord2 = axes.c2p(x + dx, func(x + dx), 0)
            slope = (func(x + dx) - func(x)) / dx
            
            point = axesBottom.c2p(x, slope, 0)

            if last is not None:
                l = Line(last, point).set_color(dot.get_color())
                lineGroup.add(l)
                self.add(l)
            last = point
            
            line = Line(coord1, coord2)\
                .set_stroke(width=DEFAULT_STROKE_WIDTH / 2).set_length(3).\
                    set_color(WHITE)
            
            return line


        tan = getTangent(x.get_value(), parabolaFunc, .0001)


        self.add(dot)

        self.play(Create(tan))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.scale(3)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        self.play(Create(frame))
        self.activate_zooming()
        self.wait(1)


        frame.add_updater(lambda _ : frame.move_to(dot))

        tan.add_updater(
            lambda _, dt : tan.become(getTangent(x.get_value(), parabolaFunc, dt))
            )
        dot.add_updater(
                lambda _ : dot.move_to(axes.c2p(x.get_value(), parabolaFunc(x.get_value()), 0))
            )

        


        
        self.play(x.animate.set_value(0), run_time = 3)

        dotColor = WHITE
        dot.set_color(dotColor)
        
        
        self.play(x.animate.set_value(4), run_time = 3)
    

        # self.play(lineGroup.animate.set_color(YELLOW))
        
        # self.play(Create(points))