from manimlib import *


# REAEME video
class Introduce(Scene):
    def construct(self):
        title = Text("Learn programming by Animation").set_width(FRAME_WIDTH - 4)
        title.shift(2.2 * UP).set_submobject_colors_by_gradient(YELLOW, RED)  # 颜色渐变
        self.play(Write(title, run_time=3))

        logo = ImageMobject("imgs/github.png").scale(0.7).shift(0.3 * DOWN)
        self.play(FadeIn(logo))

        author = Text("hwollin").set_submobject_colors_by_gradient(BLUE_C, TEAL_C)
        author.next_to(logo, DOWN, buff=MED_LARGE_BUFF)
        self.play(FadeIn(author))
