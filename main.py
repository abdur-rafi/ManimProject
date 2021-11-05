from math import cos, exp, log, sin
from os import remove
from manim import *

class diff(Scene):
    
    def construct(self):
        self.group = None
        self.createAxis()
        self.createLine(False)
        self.stairMovementForOneFunc(False)
        self.createLine(True)
        self.stairMovementForOneFunc(True)
        
    def stairMovementForOneFunc(self, transform):
        self.createMovingStair(transform)
        self.play(self.xMiddleTracker.animate.set_value(20), run_time = 1)
        self.play(self.xMiddleTracker.animate.set_value(10), run_time = 2)
        self.play(self.xMiddleTracker.animate.set_value(15))
        self.group.remove_updater(self.stairUpdater1)
        self.expandStair()
        self.play(self.expandXTracker.animate.set_value(20))
        self.play(self.expandXTracker.animate.set_value(10))
        # self.play(self.expandXTracker.animate.set_value(self.expandXTrackerInit))
        self.group.remove_updater(self.stairUpdater2)

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

        self.line = self.axis.get_graph(self.lineEquation)
        self.line.set_color(BLUE)
        self.prGroup = self.group 
        self.group = VGroup()
        self.group.add(self.line)  

    def createMovingStair(self , transform):
        
        self.xMiddleTracker = ValueTracker(15)

        xMiddle = self.xMiddleTracker.get_value()
        yMiddle = self.lineEquation(xMiddle)
        distance = 2.5

        xMidDot = xMiddle + distance
        yMidDot = yMiddle - distance
        leftX = self.lineEquationInverse(yMidDot)
        topY = self.lineEquation(xMidDot)

        stair = self.axis.get_line_graph([leftX, xMidDot, xMidDot], [yMidDot, yMidDot, topY])
        rightBrace = Brace(stair,RIGHT)
        rightBraceText = rightBrace.get_tex(r"{\Delta}y")
        # self.rightBraceText = MathTex(r"\Delta")
        bottomBrace = Brace(stair, DOWN)
        bottomBraceText = bottomBrace.get_tex(r"{\Delta}x")
        
        # self.group = VGroup();
        self.group.add(stair, rightBrace, rightBraceText, bottomBrace, bottomBraceText)
        if(transform):
            t = self.group
            self.group = self.prGroup
            self.play(self.group.animate.become(t))
            # self.prGroup.become(self.group)
        else:
            self.play(Create(self.group))

        # self.t = MathTex(r"\frac{{{{\Delta}}y}}{{{{\Delta}}x}} = \frac{{{:.2f} - {:.2f}}}{{{:.2f} - {:.2f}}} = {:.2f}".
        # format(topY, yMidDot, xMidDot, leftX,(topY - yMidDot) / (xMidDot - leftX)))
        # self.t.move_to(self.axis, 2 * UP)   

        # self.play(Create(self.t))
        

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
            ngroup = VGroup(self.line,stair, rightBrace, rightBraceText, bottomBrace, bottomBraceText)
            self.group.become(ngroup)

        self.stairUpdater1 = stairUpdater

        self.group.add_updater(stairUpdater)


    def expandStair(self):
        
        xMiddle = self.xMiddleTracker.get_value()
        yMiddle = self.lineEquation(xMiddle)
        distance = 2.5

        xMidDot = xMiddle + distance
        yMidDot = yMiddle - distance
        leftX = self.lineEquationInverse(yMidDot)
        topY = self.lineEquation(xMidDot)

        leftY = yMidDot

        self.expandXTrackerInit = xMidDot

        self.expandXTracker = ValueTracker(xMidDot)
        def updater(_):
            xMidDot = self.expandXTracker.get_value()
            stair = self.axis.get_line_graph([leftX,xMidDot, xMidDot], [leftY, leftY, self.lineEquation(xMidDot)])
            rightBrace = Brace(stair, RIGHT)
            rightBraceText = rightBrace.get_tex(r"{\Delta}y")
            bottomBrace = Brace(stair, DOWN)
            bottomBraceText = bottomBrace.get_tex(r"{\Delta}x")
            ngroup = VGroup(self.line,stair, rightBrace, rightBraceText, bottomBrace, bottomBraceText)
            self.group.become(ngroup)

            
        self.stairUpdater2 = updater;
            
        self.group.add_updater(updater)
