from game import *
from grid import *
from snake import *
from AI_game import *
import neat
import os

def eval_genomes(genomes, config):
    for genomeid, genome in genomes:
        ai_game = AI_Game()

        ai_game.train_ai(genome, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-199')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 200)
   


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)