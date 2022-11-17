import pygame as pg
from settings import *


class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 10
        self.color = WHITE

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), 5)


class Pellets:
    def __init__(self, graph, screen):
        self.graph = graph
        self.pellet_list = []
        self.node_x_done = []
        self.node_y_done = []
        self.x_list = [50, 475, 200, 287.5, 650, 745]
        self.y_list = [50, 165, 620, 710, 800]
        self.screen = screen
        self.addPelletToList()

    def pelletEaten(self, pacman):
        for pellet in self.pellet_list:
            if (
                pellet.x > pacman.x - pacman.radius
                and pellet.x < pacman.x + pacman.radius
            ) and (
                pellet.y > pacman.y - pacman.radius
                and pellet.y < pacman.y + pacman.radius
            ):
                self.pellet_list.remove(pellet)

    def addPelletToList(self):
        for node in self.graph.nodes:
            if node.x in self.x_list:
                end = node
                while end.neighbors["RIGHT"] and end not in self.node_x_done:
                    if (
                        end.x == 287.5
                        and end.y == 350
                        or end.x == 287.5
                        and end.y == 530
                    ):
                        break

                    if end.x == 200 and end.y == 435 or end.x == 650 and end.y == 435:
                        break

                    if end.x == 475 and end.y == 350:
                        break

                    self.node_x_done.append(end)
                    end = end.neighbors["RIGHT"]

                    if end.x == 375 and end.y == 710:
                        break

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

        # special case pellets
        self.pellet_list.append(Pellet(50, 50))
        self.pellet_list.append(Pellet(800, 50))
        self.pellet_list.append(Pellet(50, 255))
        self.pellet_list.append(Pellet(800, 255))
        self.pellet_list.append(Pellet(287.5, 255))
        self.pellet_list.append(Pellet(375, 255))
        self.pellet_list.append(Pellet(475, 255))
        self.pellet_list.append(Pellet(562.5, 255))
        self.pellet_list.append(Pellet(375, 50))
        self.pellet_list.append(Pellet(475, 50))
        self.pellet_list.append(Pellet(50, 620))
        self.pellet_list.append(Pellet(800, 620))
        self.pellet_list.append(Pellet(287.5, 620))
        self.pellet_list.append(Pellet(375, 620))
        self.pellet_list.append(Pellet(475, 620))
        self.pellet_list.append(Pellet(375, 710))
        self.pellet_list.append(Pellet(475, 710))
        self.pellet_list.append(Pellet(50, 710))
        self.pellet_list.append(Pellet(105, 710))
        self.pellet_list.append(Pellet(745, 710))
        self.pellet_list.append(Pellet(800, 710))
        self.pellet_list.append(Pellet(50, 800))
        self.pellet_list.append(Pellet(200, 800))
        self.pellet_list.append(Pellet(287.5, 800))
        self.pellet_list.append(Pellet(375, 800))
        self.pellet_list.append(Pellet(475, 800))
        self.pellet_list.append(Pellet(567.5, 800))
        self.pellet_list.append(Pellet(650, 800))
        self.pellet_list.append(Pellet(50, 890))
        self.pellet_list.append(Pellet(800, 890))
        self.pellet_list.append(Pellet(800, 800))

    def drawPellets(self):
        for pellet in self.pellet_list:
            if (
                pellet.x == 650
                and pellet.y == 168
                or pellet.x == 200
                and pellet.y == 168
            ):
                self.pellet_list.remove(pellet)

            pellet.draw(self.screen)
