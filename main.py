import pygame
import neat
import os
import pickle

from classes.player import Player
from classes.game import Game

pygame.font.init()

WIN_WIDTH = 640
WIN_HEIGHT = 640

def gameRun(in_genomes, config):
    nets = []
    genomes = []
    players = []
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    if not in_genomes == 0:
        for _, g in in_genomes:
            network = neat.nn.FeedForwardNetwork.create(g, config)
            g.fitness = 0

            nets.append(network)
            players.append(Player())
            genomes.append(g)
    else:
        players.append(Player())

    bestPlayer = None
    bestFitness = 0

    for x, player in enumerate(players):

        game = Game()
        while game.IsRunning():
            clock.tick(7680)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            genomes[x].fitness += game.update(player=player, network=nets[x])
            game.draw(win=win, player=player)

        if genomes[x].fitness > bestFitness:
            bestPlayer = genomes[x]
            bestFitness = genomes[x].fitness

        players.pop(x)
        nets.pop(x)
        genomes.pop(x)

    fileOpen = open('model/bestPlayer', 'rb')
    lastGenome = pickle.load(fileOpen)
    fileOpen.close()

    if lastGenome.fitness < bestFitness:
        file = open('model/bestPlayer', 'wb')
        pickle.dump(bestPlayer, file)
        file.close()


def gameRunSingleNet(in_net):
    players = []
    fitness = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    players.append(Player())

    for x, player in enumerate(players):
        game = Game()
        while game.IsRunning():
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            fitness += game.update(player=player, network=in_net)
            game.draw(win=win, player=player)

    print(fitness)



def setup(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(gameRun)

    file = open('model/winnerModel', 'xb')
    pickle.dump(winner, file)
    file.close()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    #setup(config_path)

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    file = open('model/bestPlayer', 'rb')
    genome = pickle.load(file)
    network = neat.nn.FeedForwardNetwork.create(genome, config)
    gameRunSingleNet(network)


