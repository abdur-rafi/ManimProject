from manim import *

class MovingZoomedSceneAround(ZoomedScene):
# contributed by TheoremofBeethoven, www.youtube.com/c/TheoremofBeethoven
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
        dot = Dot().shift(UL * 2)
        self.add(dot)
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)


        # unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))


        self.play(Create(frame))
        self.activate_zooming()

        # self.play(self.get_zoomed_display_pop_out_animation())
        # Scale in        x   y  z
        # scale_factor = [0.5, 1.5, 0]
        # self.play(
        #     frame.animate.scale(scale_factor),
        #     zoomed_display.animate.scale(scale_factor),
        # )
        # self.wait()
        # self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()