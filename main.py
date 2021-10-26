from math import cos, exp, log, sin
from os import remove
from manim import *

class diff(Scene):
    
    def construct(self):
        self.createAxis()
        self.createLine(False)
        # self.createMovingStair()
        # self.createRatioText()
        # self.play(self.rightAngleDotXVal.animate.set_value(25))
        # self.play(self.rightAngleDotXVal.animate.set_value(-5))
        # self.play(self.xMiddleTracker.animate.set_value(20), run_time = 1)
        # self.play(self.xMiddleTracker.animate.set_value(10), run_time = 2)
        # self.play(self.xMiddleTracker.animate.set_value(15))
        # self.remove_updater(self.stairUpdater1)
        # self.expandStair()
        # self.play(self.expandXTracker.animate.set_value(25))
        # self.play(self.expandXTracker.animate.set_value(5))

        self.stairMovementForOneFunc()
        self.play(FadeOut(self.group))
        # self.play(FadeOut(self.stair))
        # self.play(FadeOut(self.line))
        self.createLine(True)
        self.stairMovementForOneFunc()
        




    def stairMovementForOneFunc(self):
        self.createMovingStair()
        self.play(self.xMiddleTracker.animate.set_value(20), run_time = 1)
        self.play(self.xMiddleTracker.animate.set_value(10), run_time = 2)
        self.play(self.xMiddleTracker.animate.set_value(15))
        self.expandStair()
        self.play(self.expandXTracker.animate.set_value(25))
        self.play(self.expandXTracker.animate.set_value(5))


    def createAxis(self):
        self.xAxis = [-10, 30, 5]
        self.yAxis = [-10, 30, 10]
        self.axis = Axes(self.xAxis,self.yAxis,tips=False, x_axis_config={
            'include_numbers' : True
        },y_axis_config={
            'include_numbers' : True
        });
        self.play(Create(self.axis));
    
    def createLine(self, expo):
        def eqn(x):
            return x
        
        def eqn2(y):
            return y

        
        def expoEqn(x):
            return (x / 7) ** 3

        def expoEqnInverse(y):
            return pow(y, 1/3) * 7

        if expo:
            self.lineEquation = expoEqn
            self.lineEquationInverse = expoEqnInverse
        else:
            self.lineEquation = eqn
            self.lineEquationInverse = eqn2



        startX = self.xAxis[0]
        startY = self.lineEquation(startX)
        endX = self.xAxis[1]
        endY = self.lineEquation(endX)
        # self.line = Line(self.axis.coords_to_point(startX, startY, 0), self.axis.coords_to_point(endX, endY, 0))
        # self.line = Line()
        self.line = self.axis.get_graph(self.lineEquation)
        self.line.set_color(BLUE)
        self.play(Create(self.line)); 
    


    def createMovingStair(self):
        

        self.xMiddleTracker = ValueTracker(15)

        xMiddle = self.xMiddleTracker.get_value()
        yMiddle = self.lineEquation(xMiddle)
        distance = 2.5

        xMidDot = xMiddle + distance
        yMidDot = yMiddle - distance
        leftX = self.lineEquationInverse(yMidDot)
        topY = self.lineEquation(xMidDot)

        
        self.stair = self.axis.get_line_graph([leftX, xMidDot, xMidDot], [yMidDot, yMidDot, topY])
        self.rightBrace = Brace(self.stair,RIGHT)
        self.rightBraceText = self.rightBrace.get_tex(r"{\Delta}y")
        # self.rightBraceText = MathTex(r"\Delta")
        self.bottomBrace = Brace(self.stair, DOWN)
        self.bottomBraceText = self.bottomBrace.get_tex(r"{\Delta}x")
        
        self.group = VGroup();
        self.group.add(self.stair)
        self.group.add(self.rightBrace)
        self.group.add(self.rightBraceText)
        self.group.add(self.bottomBrace)
        self.group.add(self.bottomBraceText)

        self.play(Create(self.group))

        # self.play(Create(self.stair))
        # self.play(Create(self.rightBrace))
        # self.play(Create(self.rightBraceText))
        # self.play(Create(self.bottomBrace))
        # self.play(Create(self.bottomBraceText))

        

        # self.t = MathTex(r"\frac{{{{\Delta}}y}}{{{{\Delta}}x}} = \frac{{{:.2f} - {:.2f}}}{{{:.2f} - {:.2f}}} = {:.2f}".
        # format(topY, yMidDot, xMidDot, leftX,(topY - yMidDot) / (xMidDot - leftX)))
        # self.t.move_to(self.axis, 2 * UP)   

        # self.play(Create(self.t))
        


        # self.yMiddle = self.lineEquation()

        def stairUpdater(_):

            xMiddle = self.xMiddleTracker.get_value()
            yMiddle = self.lineEquation(xMiddle)

            xMidDot = xMiddle + distance
            yMidDot = yMiddle - distance
            leftX = self.lineEquationInverse(yMidDot)
            topY = self.lineEquation(xMidDot)

            stair = self.axis.get_line_graph([leftX, xMidDot, xMidDot], [yMidDot, yMidDot, topY])
            rightBrace = Brace(stair, RIGHT)
            rightBraceText = rightBrace.get_tex(r"{\Delta}y")
            bottomBrace = Brace(stair, DOWN)
            bottomBraceText = bottomBrace.get_tex(r"{\Delta}x")
            # t = MathTex(r"\frac{{{{\Delta}}x}}{{{{\Delta}}y}} = \frac{{{:.2f} - {:.2f}}}{{{:.2f} - {:.2f}}} = {:.2f}".
            # format(topY, yMidDot, xMidDot, leftX, (topY - yMidDot) / (xMidDot - leftX)))
            # t.move_to(self.axis, 2 * UP)
            # self.t.become(t)

            self.stair.become(stair)
            self.rightBrace.become(rightBrace)
            self.rightBraceText.become(rightBraceText)
            self.bottomBrace.become(bottomBrace)
            self.bottomBraceText.become(bottomBraceText)

        self.stairUpdater1 = stairUpdater

        self.stair.add_updater(stairUpdater)


    def expandStair(self):
        
        xMiddle = self.xMiddleTracker.get_value()
        yMiddle = self.lineEquation(xMiddle)
        distance = 2.5

        xMidDot = xMiddle + distance
        yMidDot = yMiddle - distance
        leftX = self.lineEquationInverse(yMidDot)
        topY = self.lineEquation(xMidDot)

        leftY = yMidDot

        self.expandXTracker = ValueTracker(xMidDot)
        def updater(_):
            xMidDot = self.expandXTracker.get_value()
            stair = self.axis.get_line_graph([leftX,xMidDot, xMidDot], [leftY, leftY, self.lineEquation(xMidDot)])
            self.stair.become(stair)
            rightBrace = Brace(stair, RIGHT)
            rightBraceText = rightBrace.get_tex(r"{\Delta}y")
            bottomBrace = Brace(stair, DOWN)
            bottomBraceText = bottomBrace.get_tex(r"{\Delta}x")
            self.rightBrace.become(rightBrace)
            self.rightBraceText.become(rightBraceText)
            self.bottomBrace.become(bottomBrace)
            self.bottomBraceText.become(bottomBraceText)
            
            
        self.stair.add_updater(updater)

