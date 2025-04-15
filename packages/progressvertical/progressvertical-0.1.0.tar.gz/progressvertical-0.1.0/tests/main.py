from progressvertical  import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()

renderer = VerticalProgressRenderer(height=10)
manager = ProgressManager(renderer)

manager.add_stage(
    label="Download",
    duration=2.0,
    fore_color="LIGHTBLUE_EX",
    style="BRIGHT",
)

manager.add_stage(
    label="Processamento",
    duration=3.0,
)

manager.add_stage(
    label="Finalizado",
    duration=1.0,
    fore_color="GREEN",
    style="BRIGHT",
)
manager.start_animation()
