import pygame
import title_runner
import runner

fps = 30 # more than 60 fps is not recommended as pygame starts to break

while True:
    pygame.init()
    # run title screen
    title_runner_instance = title_runner.TitleRunner()
    while title_runner_instance.running:
        title_runner_instance.update()
        title_runner_instance.draw()

    # run main game
    taskbar_padding = 35  # extra pixels for the taskbar | increase this if the game clips through the taskbar
    fullscreen_height = pygame.display.set_mode(flags=pygame.FULLSCREEN).get_height()
    window_size = (fullscreen_height - taskbar_padding, fullscreen_height - taskbar_padding)

    runner_instance = runner.Runner(fps, window_size, random_game=title_runner_instance.is_random_game)
    while runner_instance.running: 
        runner_instance.update()
        runner_instance.draw()
