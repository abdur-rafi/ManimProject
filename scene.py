from math import cos, sin
from os import remove
from manim import *

class createCircle(Scene):
    def construct(self):
        circle = Circle();
        circle.set_fill(PINK, opacity=.4)

        # square = Square()
        # square.rotate(PI / 4)
        
        # self.play(Create(square))
        # # self.play(Create(circle))
        # self.play(Transform(square, circle))
        # self.wait()
        ax = Axes(
            [-10, 10, 1],
            [-5, 5, 1],
            10,
            5
        )
        # self.play(Create(circle))
        # self.play(circle.animate.add_background_rectangle(ORANGE))
        # ax.animate.
        self.play(Create(ax))
        
        # self.play(ax.animate.rotate(PI / 4))

        curve = ax.get_graph(lambda x : x ** 2)
        curve.set_fill(ORANGE)
        self.play(Create(curve))
        self.play(curve.animate.set_color(ORANGE))

class Logo(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        
        
        
       
        triangle = Triangle(color=logo_red, fill_opacity=1)
        self.play(Create(triangle))
        self.play(triangle.animate.shift(RIGHT))

        circle = Circle(color=logo_green, fill_opacity=1)
        self.play(Create(circle))
        self.play(circle.animate.shift(LEFT))

        square = Square(color=logo_blue, fill_opacity=1)
        self.play(Create(square))
        self.play(square.animate.shift(UP))

        ds_m = MathTex(r"\mathbb{M}", fill_color=logo_black)
        self.play(Create(ds_m))
        self.play(ds_m.animate.scale(7))
        self.play(ds_m.animate.shift(2.25 * LEFT + 1.5 * UP))

        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.move_to(ORIGIN)
        # self.add(logo)

class Logo2(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        ds_m = MathTex(r"\mathbb{M}", fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.move_to(ORIGIN)
        self.play(Create(logo), run_time = 4)

class brace2(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center())
        self.play(Create(line))
        self.play(line.animate.set_color(ORANGE))
        b1 = Brace(line)
        self.play(Create(b1))
        b1text = b1.get_text("Horizontal distance")
        self.play(Create(b1text));
        # print(line.copy().rotate(PI / 2).get_unit_vector())
        b2 = Brace(line,direction=line.copy().rotate(PI / 2).get_unit_vector())
        self.play(Create(b2))
        # self.play(b2.get_direction())
        b2text = b2.get_tex("x-x_1")
        self.play(Create(b2text));
        group = VGroup(line, dot, dot2, b1, b2, b1text, b2text)
        # self.play(Create(group), run_time = 4)
        # self.add(line, dot, dot2, b1, b2, b1text, b2text)


class Mine(Scene):
    def construct(self):
        x = ValueTracker(.01)
        dot = Dot(ORIGIN)
        r = 1
        self.play(Create(dot))
        self.play(dot.animate.move_to([r, 0, 0]))

        line = Line([r, 0, 0], [r, 0, 0])
        s = r
        vg = VGroup()
        prevPoint = [r, 0 , 0]
        self.add(line)

        def getPoint():
            y1 = r * sin(x.get_value())
            x1 = r * cos(x.get_value())
            return [x1, y1, 0]

        def moveDot(dot : Dot):
            dot.move_to(getPoint())
            
        
        def moveLine(l : Line):
            delta = .5 / 60
            nonlocal prevPoint
            nonlocal s
            x1 = getPoint()
            x2 = x1.copy()
            x2[0] = s + delta
            s += delta
            line2 = Line(x1, x2)
            l.become(line2)
            vg.add(Line(prevPoint, x2))
            prevPoint = x2

        line.add_updater(moveLine)

        dot.add_updater(moveDot)
        self.add(vg);
        self.play(x.animate.set_value(PI * 2.5), run_time = 6, rate_func = linear)

class Diff(Scene):
    def construct(self):
        axes = Axes([-10, 10, 1], [-10, 10, 1],x_length=12, y_length=10, tips=False, axis_config={
            'tick_size' : .05
        })

        def func(x : float):
            return .1 * (.7 * x**3 - 3 * x**2  + 30)

        self.play(Create(axes))
        cube_graph = axes.get_graph(func, x_range=(-10,10,.01), color=BLUE)
        label_x = -1
        label = axes.get_graph_label(cube_graph,'f(x)', x_val=label_x,direction=UP)
        self.play(Create(cube_graph))
        self.play(Create(label))
        self.play(label.animate.set_color(ORANGE))

        x_fixed = 1
        x_changing = 6
        
        x_end = ValueTracker(x_changing)
        
        f_dot = Dot(axes.i2gp(x_fixed,cube_graph), color=ORANGE)
        moving_dot = Dot(axes.i2gp(x_end.get_value(),cube_graph), color=ORANGE)

        self.play(Create(f_dot))
        self.play(Create(moving_dot))

        line = Line(f_dot, moving_dot, color=ORANGE).scale(100)

        vBottomPoint = moving_dot.get_center().copy()
        vBottomPoint[1] = f_dot.get_center()[1]

        vLine = Line(moving_dot.get_center(), vBottomPoint);
        hLine = Line(f_dot.get_center(),vBottomPoint)

        self.play(Create(line))
        self.play(Create(vLine))
        self.play(Create(hLine))
        

        brRight = Brace(vLine, RIGHT)
        self.play(Create(brRight));
        brRightText =  brRight.get_text('dy')
        self.play(Create(brRightText));



        brBottom = Brace(hLine, DOWN)
        self.play(Create(brBottom))
        brBottomText = brBottom.get_text('dx')
        self.play(Create(brBottomText))


        def dot_updater(dot:Dot):
            nonlocal x_end
            nDot = Dot(axes.i2gp(x_end.get_value(),cube_graph), color=ORANGE)
            dot.become(nDot)

            vBottomPoint = nDot.get_center().copy()
            vBottomPoint[1] = f_dot.get_center()[1]

            vLine.become(Line(nDot.get_center(), vBottomPoint))
            hLine.become(Line(f_dot.get_center(),vBottomPoint))

            brLeftNew = Brace(vLine, RIGHT)

            brBottomNew = Brace(hLine, DOWN)

            brRight.become(brLeftNew)
            brBottom.become(brBottomNew)

            brRightText.become(brRight.get_text('dy'))
            brBottomText.become(brBottom.get_text('dx'))

            line.become(Line(f_dot.get_center(),nDot.get_center(),color = ORANGE).scale(100))
            

        moving_dot.add_updater(dot_updater)

        self.play(x_end.animate.set_value(x_fixed + .5), run_time = 4)


        