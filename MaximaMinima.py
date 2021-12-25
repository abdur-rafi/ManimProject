from types import FrameType
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
        slopeLabel = MathTex(r"y = f'(x) = {\frac{df}{dx}}", font_size = 30)
        self.play(slopeLabel.animate.next_to(axesBottom, LEFT))
        # self.play(Write(slopeLabel))

        lineGroup = VGroup()
        last = None

        x = ValueTracker(-4)

        dotColor = YELLOW

        dot = Dot(radius=DEFAULT_DOT_RADIUS / 3).set_color(dotColor)\
            .move_to(axes.c2p(x.get_value(), parabolaFunc(x.get_value()), 0)).set_z_index(2)

        DX = .0001

        # parabola.cordi
        def getTangent(x, func)->Line:
            nonlocal last, dot
            dx = DX
            # dx = max(dx, .000001)
            coord1 = axes.c2p(x, func(x), 0)
            coord2 = axes.c2p(x + dx, func(x + dx), 0)
            slope = (func(x + dx) - func(x)) / dx
            
            line = Line(coord1, coord2)\
                .set_stroke(width=DEFAULT_STROKE_WIDTH / 2).set_length(3).\
                    set_color(WHITE)
            
            return line, (x,slope)

        def createBasePerp(dirx=DOWN):
            dx = .3
            x1 = x.get_value()
            x2 = x.get_value() + dx
            c1 = axes.c2p(x1, parabolaFunc(x1), 0)
            c2 = axes.c2p(x2, parabolaFunc(x1), 0)

            c3 = axes.c2p(x2, parabolaFunc(x2), 0)
            strokeWidth = DEFAULT_STROKE_WIDTH / 4
            lx = Line(c1, c2).set_stroke(width=strokeWidth)
            ly = Line(c2, c3).set_stroke(width=strokeWidth)
            lxT = MathTex(r"dx(+)", font_size = 5).next_to(lx, dirx, buff=0.03)
            rstr = "df" +( "(+)" if c3[1] - c2[1] > 0 else "(-)") 
            lyT = MathTex(rstr, font_size = 5).next_to(ly, RIGHT, buff=0.03)
            
            
            return VGroup(lx,ly, lxT, lyT)


        tan, prevSlopePointPair = getTangent(x.get_value(), parabolaFunc)
        

        self.play(Create(dot))
        # self.add(slopeVis)
        self.play(Create(tan))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.scale(3).shift(.1 * RIGHT)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.scale(.8)
        # zoomed_display.shift(DOWN)

        self.play(Create(frame))
        self.play(self.get_zoomed_display_pop_out_animation())
        self.activate_zooming()
        self.wait(1)
        bottomDot = dot.copy()

    

        self.play(bottomDot.animate.move_to(axesBottom.c2p(*prevSlopePointPair, 0)))
        dashCount = 30
        dashedLine = DashedVMobject(
            Line(dot.get_center(), bottomDot.get_center())\
                .set_stroke(width= DEFAULT_STROKE_WIDTH / 2)\
                    .set_color(TEAL),
            dashCount)
        self.play(Create(dashedLine))
        lineGroup  = []


        frame.add_updater(lambda _ : frame.move_to(dot).shift(.1 * RIGHT))
        
        def tanAndSlopeUpdater(_, dt):
            nonlocal prevSlopePointPair
            nTan, slopePointPair = getTangent(x.get_value(), parabolaFunc)
            tan.become(nTan)
            p2 = axesBottom.c2p(*slopePointPair, 0)
            line = Line(axesBottom.c2p(*prevSlopePointPair, 0),
                       p2).set_color(dotColor)
            lineGroup.append(line)
            bottomDot.move_to(p2)
            dashedLine.become(DashedVMobject(Line(dot.get_center(), p2), dashCount).set_stroke(width= DEFAULT_STROKE_WIDTH / 2).set_color(TEAL))
            
            prevSlopePointPair = slopePointPair
            self.add(line)
            

        tan.add_updater(tanAndSlopeUpdater)
        dot.add_updater(
                lambda _ : dot.move_to(axes.c2p(x.get_value(), parabolaFunc(x.get_value()), 0))
            )
        

        
        slopeVis = createBasePerp()
        slopeVis.add_updater(lambda _, dt : slopeVis.become(createBasePerp()))    
        self.play(Create(slopeVis))

        self.play(x.animate.set_value(0), run_time = 3)

        
        # tan.clear_updaters()
        # # dot.clear_updaters()
        
        slopeVis.clear_updaters()
        self.play(Uncreate(slopeVis))
        self.wait(1)
        
        lu = lineGroup[0].start
        rd = lineGroup[-1].end
        ld = lu.copy()
        ld[1] = rd[1]
        ru = rd.copy()
        ru[1] = lu[1]
        rect = Polygon(lu, ru, rd, ld).set_color(RED)
        self.play(Create(rect))
        txt = MathTex(r"{\frac{df}{dx}} > 0\, {\Rightarrow}\, increasing", font_size = 30).next_to(axesBottom).align_to(axesBottom, UP)
        self.play(Write(txt))
        self.play(Uncreate(rect))
        self.play(FadeOut(txt))
        # self.play(Circumscribe(VGroup(Dot(lineGroup[0].start), Dot(lineGroup[-1].end))))

        # self.wait(1)
        dotColor = WHITE
        dot.set_color(dotColor)
        # x.set_value(.0001)
        slopeVis.add_updater(
            lambda _, dt : slopeVis.become(createBasePerp(UP))
        )
        self.play(Create(slopeVis))
        lineGroup = []
        # tan.add_updater(tanAndSlopeUpdater)
        
        self.play(x.animate.set_value(4), run_time = 3)


        self.wait(1)

        
        lu = lineGroup[0].start
        rd = lineGroup[-1].end
        ld = lu.copy()
        ld[1] = rd[1]
        ru = rd.copy()
        ru[1] = lu[1]
        rect = Polygon(lu, ru, rd, ld).set_color(RED)
        self.play(Create(rect))
        txt = MathTex(r"{\frac{df}{dx}} < 0\, {\Rightarrow}\, decreasing", font_size = 30).next_to(axesBottom).align_to(axesBottom, UP)
        self.play(Write(txt))
        self.play(Uncreate(rect))
        self.play(FadeOut(txt))
        

        # self.play(lineGroup.animate.set_color(YELLOW))
        
        # self.play(Create(points))