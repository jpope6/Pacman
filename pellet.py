import pygame as pg
from settings import *


class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 10

    def draw(self, screen):
        pg.draw.circle(screen, WHITE, (self.x, self.y), 5)


class Pellets:
    def __init__(self, graph, screen):
        self.graph = graph
        self.pellet_list = []
        self.node_x_done = []
        self.node_y_done = []
        self.x_list = [50, 475, 200, 287.5, 567.5, 650, 745]
        self.y_list = [50, 165, 255, 350, 620, 710, 800]
        self.screen = screen
        self.addPelletToList()

    # YOU CAN DO THIS BETTER
    def addPelletToList(self):
        for node in self.graph.nodes:
            if node.x in self.x_list:
                end = node
                while end.neighbors["RIGHT"] and end not in self.node_x_done:
                    if end.x == 650 and end.y == 435:
                        break

                    self.node_x_done.append(end)
                    end = end.neighbors["RIGHT"]

                x = node.x + 28
                y = node.y

                while x < end.x - 26:
                    self.pellet_list.append(Pellet(x, y))
                    x += 30

            if node.y in self.y_list:
                end = node
                while end.neighbors["DOWN"] and end not in self.node_y_done:
                    self.node_y_done.append(end)
                    end = end.neighbors["DOWN"]

                x = node.x
                y = node.y + 28

                while y < end.y - 26:
                    self.pellet_list.append(Pellet(x, y))
                    y += 30

        self.pellet_list.append(Pellet(627.5, 435))

    def drawPellets(self):
        for pellet in self.pellet_list:
            pellet.draw(self.screen)
