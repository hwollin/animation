from manimlib import *


# 视频地址 https://hwollin.github.io/2022/08/19/cas/
class TexTransformExample(Scene):
    def construct(self):
        # intro: value是内存中的一个变量，初始值为5，线程A和线程B都会去读写这个数据
        value = Text("value").set_color(RED_D)
        five = Text("5").set_color(RED_D)
        memory = Text("memory").set_color(BLUE_D)
        thread_a = Text("线程A").set_color(YELLOW)
        thread_b = Text("线程B").set_color(YELLOW)

        intro = VGroup(
            value,
            Text("是内存("),
            memory,
            Text(")中的一个变量，初始值为"),
            five,
            Text("，有两个线程("),
            thread_a,
            Text("和"),
            thread_b,
            Text(")都会去读写这个数据")
        ).arrange(buff=SMALL_BUFF).set_width(FRAME_WIDTH - 2).to_edge(UP)

        self.play(FadeIn(intro, DOWN))
        self.wait(3)

        # memory: value内存块
        mem_box = Rectangle(width=1.8, height=1.2).set_fill(BLUE_D, opacity=0.75).set_stroke(BLUE, width=4)
        mem_box.next_to(intro, DOWN).shift(5 * RIGHT + 1.2 * DOWN)
        five_cp = five.copy().scale(1.7)
        memory_cp = memory.copy()
        self.play(ShowCreation(mem_box))
        self.play(memory_cp.animate.shift(9 * RIGHT + 3.2 * DOWN))
        self.play(five_cp.animate.move_to(mem_box.get_center()))

        # 线程a部分
        thread_a_box = Rectangle(width=3.5, height=5).set_fill(GREY_D, opacity=0.75)
        thread_a_box.set_stroke(GREY, width=4).shift(3.5 * LEFT + 0.7 * DOWN)
        a_code_11 = Text("value = ", t2c={"value": RED_D})
        a_code_12 = Text("getValue()").next_to(a_code_11)
        a_code_1 = VGroup(
            a_code_11,
            a_code_12
        )

        a_code_21 = Text("updateValue = ", t2c={"updateValue": RED_D})
        a_code_22 = Text("value + 1", t2c={"value": RED_D}).next_to(a_code_21)
        a_code_2 = VGroup(
            a_code_21,
            a_code_22
        )
        a_code_3 = Text("cmpxchg(value, uv)", t2c={"value": RED_D, "uv": RED_D})
        a_code = VGroup(
            Text("..."),
            a_code_1,
            a_code_2,
            Text("..."),
            Text("..."),
            Text("..."),
            Text("//uv: updateValue").set_color(GREEN),
            a_code_3,
            Text("..."),
            Text("...")
        ).arrange(DOWN, buff=MED_LARGE_BUFF, center=False, aligned_edge=LEFT).scale(0.6).shift(5.9 * LEFT + 2.8 * UP)

        self.play(thread_a.copy().animate.shift(5.6 * LEFT + DOWN))
        self.play(ShowCreation(thread_a_box))
        self.play(Write(a_code))
        self.wait(2)

        # 线程b部分
        thread_b_cp = thread_b.copy()
        b_box = Rectangle(width=3.5, height=5).set_fill(GREY_D, opacity=0.75).set_stroke(GREY, width=4).shift(
            1.8 * RIGHT + 0.7 * DOWN)
        b_code_1 = Text("value = ", t2c={"value": RED_D})
        b_code_2 = Text("100").next_to(b_code_1, buff=SMALL_BUFF)
        b_code = VGroup(
            Text("..."),
            Text("..."),
            Text("..."),
            Text("..."),
            Text("..."),
            Text("//写value").set_color(GREEN),
            VGroup(
                b_code_1,
                b_code_2
            ),
            Text("..."),
            Text("..."),
            Text("..."),
            Text("..."),
            Text("...")
        ).arrange(DOWN, buff=MED_LARGE_BUFF, center=False, aligned_edge=LEFT).scale(0.6).shift(2.6 * UP)
        b_group = VGroup(b_box, b_code, thread_b_cp)
        self.play(thread_b_cp.animate.shift(1.4 * LEFT + DOWN))
        self.play(ShowCreation(b_box))
        self.play(Write(b_code))
        self.wait()

        # 模拟线程的执行过程
        arrow1_txt = Text("时刻t1 --->").set_color(PURPLE_A).scale(0.6).shift(6 * LEFT + 1.05 * UP)
        self.play(FadeIn(arrow1_txt))
        self.play(FadeOut(a_code_12))
        five_txt_cp2 = five_cp.copy().scale(0.66).set_color(BLUE)
        self.play(five_txt_cp2.animate.shift(8.8 * LEFT + 0.15 * DOWN))
        hint1 = Text("//").set_color(GREEN).scale(0.6).next_to(five_txt_cp2).shift(0.1 * LEFT)
        hint2 = Text("oldValue").set_color(GREEN).scale(0.6).next_to(hint1).shift(0.23 * LEFT)
        self.play(FadeIn(VGroup(hint1, hint2)))
        self.wait()

        arrow2_txt = Text("时刻t1.1 --->").set_color(PURPLE_A).scale(0.6).shift(6.13 * LEFT + 0.5 * UP)
        self.play(FadeIn(arrow2_txt))
        six = Text("6").set_color(BLUE).scale(0.6).shift(2.85 * LEFT + 0.45 * UP)
        self.play(FadeTransform(a_code_22, six))
        self.wait()

        arrow3_txt = Text("时刻t2 --->").set_color(PURPLE_A).scale(0.6).shift(6 * LEFT + 1.65 * DOWN)
        self.play(FadeIn(arrow3_txt))
        self.play(FadeOut(b_group))  # 隐藏线程b部分

        # 成功更新的情况
        case1 = Text("情况一：从时刻t1到时刻t2，内存中value\n的值未被其他线程改写", font_size=28).shift(
            2.1 * UP + 1.2 * RIGHT)
        case1.set_color(TEAL_B)
        self.play(Write(case1))
        self.wait(2)

        cas_step1 = Text("step1.将oldValue存入eax寄存器中", font_size=28).set_color(GREEN_B)
        cas_step1.next_to(case1, DOWN, aligned_edge=LEFT)
        self.play(Write(cas_step1))
        # draw eax
        eax = Rectangle(width=1.8, height=1.2).set_fill(GOLD_B, opacity=0.75).set_stroke(GOLD, width=4)
        eax.next_to(mem_box, DOWN).shift(1.5 * DOWN)
        eax_txt = Text("eax").next_to(eax, DOWN).scale(0.6).set_color(GOLD_B)
        self.play(ShowCreation(eax))
        self.play(FadeIn(eax_txt))
        five_txt_cp3 = five_txt_cp2.copy().scale(1.5).set_color(RED_D)
        self.play(five_txt_cp3.animate.move_to(eax.get_center()))

        cas_step21 = Text("step2.比较eax寄存器与value的", font_size=28).set_color(GREEN_B)
        cas_step21.next_to(cas_step1, DOWN, aligned_edge=LEFT)
        cas_step22 = Text("最新值", font_size=28).set_color(GREEN_B).next_to(cas_step21, buff=SMALL_BUFF / 2)
        self.play(Write(VGroup(cas_step21, cas_step22)))
        self.wait()
        five_txt_cp4 = five_cp.copy()  # memory 5
        hint2_cp = hint2.copy().scale(1.2)
        five_txt_cp5 = five_txt_cp3.copy()  # eax 5
        cas_step22_cp = cas_step22.copy()
        self.play(five_txt_cp5.animate.next_to(cas_step21, DOWN).shift(0.1 * DOWN + 1.5 * LEFT))
        self.play(hint2_cp.animate.next_to(five_txt_cp5, buff=SMALL_BUFF))
        self.play(five_txt_cp4.animate.next_to(hint2_cp, buff=LARGE_BUFF * 1.2))
        self.play(cas_step22_cp.animate.next_to(five_txt_cp4, buff=SMALL_BUFF))
        equal = Text("==", font_size=28).next_to(hint2_cp, buff=MED_LARGE_BUFF)
        self.play(FadeIn(equal))
        cas_step3 = Text("step3.若相等，则将updateValue写入内存", font_size=28).set_color(GREEN_B)
        cas_step3.next_to(cas_step21, 4 * DOWN, aligned_edge=LEFT)
        self.play(Write(cas_step3))
        self.wait()
        six_cp = six.copy().scale(1.5).set_color(RED)
        self.play(FadeOut(five_cp))
        self.play(six_cp.animate.move_to(mem_box.get_center()))
        cas_step3_info = Text("成功更新value的值", font_size=28)
        cas_step3_info.next_to(cas_step3, DOWN)
        self.play(Write(cas_step3_info))
        cas_step4 = Text("step4.将eax寄存器的值返回", font_size=28).set_color(GREEN_B)
        cas_step4.next_to(cas_step3, 3 * DOWN, aligned_edge=LEFT)
        self.play(Write(cas_step4))
        self.wait()
        return_on_success = five_txt_cp3.copy().scale(0.66)
        self.play(return_on_success.animate.next_to(a_code_3, buff=MED_SMALL_BUFF))
        cas_step4_info = Text("该返回值用于更新失败时自旋", font_size=28)
        cas_step4_info.next_to(cas_step4, DOWN).shift(0.9 * RIGHT)
        self.play(Write(cas_step4_info))
        cas_step4_info2 = Text("下面我们来看更新失败的情况", font_size=28).set_color(MAROON_A)
        cas_step4_info2.next_to(cas_step4, 4 * DOWN).shift(0.9 * RIGHT)
        self.play(Write(cas_step4_info2))
        self.wait()

        # 删除上述字幕
        success_info = VGroup(
            case1,
            cas_step1,
            cas_step21,
            cas_step22,
            cas_step22_cp,
            cas_step3,
            cas_step3_info,
            cas_step4,
            cas_step4_info,
            cas_step4_info2,
            return_on_success,
            six_cp,
            five_txt_cp4,
            five_txt_cp5,
            equal,
            hint2_cp,
            eax,
            eax_txt,
            five_txt_cp3,
            arrow3_txt
        )
        self.play(FadeOut(success_info))
        self.play(FadeIn(five_cp))
        self.play(FadeIn(b_group))

        # 更新失败的情况
        arrow4 = Text("时刻t1.5 --->").set_color(PURPLE_A).scale(0.6)
        arrow4.next_to(b_code_1, LEFT).shift(0.12 * LEFT)
        self.play(FadeIn(arrow4))
        new_value_cp = b_code_2.copy().set_color(RED).scale(1.5)
        self.play(FadeOut(five_cp))
        self.play(new_value_cp.animate.move_to(mem_box.get_center()))
        self.play(FadeIn(arrow3_txt))
        self.play(FadeOut(b_group.add(arrow4)))

        case_fail = Text("情况二：从时刻t1到时刻t2，内存中value\n的值被其他线程改写", font_size=28).shift(
            2.1 * UP + 1.2 * RIGHT)
        case_fail.set_color(TEAL_B)
        self.play(Write(case_fail))
        self.wait(2)
        self.play(Write(cas_step1))
        self.play(ShowCreation(eax))
        self.play(FadeIn(eax_txt))
        five_txt_cp6 = five_txt_cp2.copy().scale(1.5).set_color(RED_D)
        self.play(five_txt_cp6.animate.move_to(eax.get_center()))
        self.play(Write(VGroup(cas_step21, cas_step22)))
        self.wait()
        new_value_cp2 = new_value_cp.copy()  # memory 100
        hint2_cp2 = hint2.copy().scale(1.2)
        five_txt_cp7 = five_txt_cp6.copy()  # eax 5
        cas_step22_cp2 = cas_step22.copy()
        self.play(five_txt_cp7.animate.next_to(cas_step21, DOWN).shift(0.1 * DOWN + 1.5 * LEFT))
        self.play(hint2_cp2.animate.next_to(five_txt_cp7, buff=SMALL_BUFF))
        self.play(new_value_cp2.animate.next_to(hint2_cp, buff=LARGE_BUFF))
        self.play(cas_step22_cp2.animate.next_to(new_value_cp2, buff=SMALL_BUFF))
        not_equal = Text("! =", font_size=28).next_to(hint2_cp2, buff=MED_LARGE_BUFF * 0.8)
        self.play(FadeIn(not_equal))

        cas_step3_fail = Text("step3.若不等，则将updateValue写入eax", font_size=28).set_color(GREEN_B)
        cas_step3_fail.next_to(cas_step21, 4 * DOWN, aligned_edge=LEFT)
        self.play(Write(cas_step3_fail))
        self.wait()
        six_cp2 = six.copy().scale(1.5).set_color(RED)
        self.play(FadeOut(five_txt_cp6))
        self.play(six_cp2.animate.move_to(eax.get_center()))

        cas_step4.next_to(cas_step3_fail, DOWN, aligned_edge=LEFT)
        self.play(Write(cas_step4))
        self.wait()
        return_on_fail = six_cp2.copy().scale(0.66)
        self.play(return_on_fail.animate.next_to(a_code_3, buff=MED_SMALL_BUFF))
        self.wait()
        cas_step4_info_fail = Text("以上流程只是单次更新的过程", font_size=28)
        cas_step4_info2_fail = Text("下面我们来看一下失败是如何自旋的", font_size=28)
        cas_step4_info_fail.set_color(MAROON_A).next_to(cas_step4, 3 * DOWN).shift(RIGHT)
        cas_step4_info2_fail.set_color(MAROON_A).next_to(cas_step4_info_fail, DOWN)
        self.play(Write(cas_step4_info_fail))
        self.play(Write(cas_step4_info2_fail))
        self.wait()

        fail_info = VGroup(
            cas_step3_fail,
            cas_step4,
            cas_step4_info_fail,
            cas_step4_info2_fail,
            six_cp2,
            case_fail,
            cas_step1,
            eax,
            eax_txt,
            five_txt_cp6,
            five_txt_cp7,
            cas_step21,
            cas_step22,
            new_value_cp2,
            hint2_cp2,
            cas_step22_cp2,
            not_equal,
            mem_box,
            memory_cp,
            new_value_cp
        )

        self.clear()
        self.add(intro)
        # TODO 注意该路径修改为spin_code的真实路径
        spin_code = ImageMobject(filename="imgs/spin_code.png").shift(UP).scale(0.88)
        self.add(spin_code)

        spin_info = Text("在上述更新失败的场景中，oldValue=5，cmp的返回值为6，do-while会自旋重试，直到成功更新")
        spin_info.set_width(FRAME_WIDTH - 2).shift(2 * DOWN).set_color(BLUE)
        self.play(Write(spin_info))
