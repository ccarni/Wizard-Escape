import pygame
import runner
import title_runner

#this is needed since the game stops when you die
while True:
    #run title screen
    pygame.init()
    title_runner_instance = title_runner.TitleRunner()
    while title_runner_instance.running:
        title_runner_instance.update()
        title_runner_instance.draw()

    #run main game
    runner_instance = runner.Runner()
    while runner_instance.running:
        runner_instance.update()
        runner_instance.draw()
