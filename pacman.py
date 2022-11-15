import pygame as pg


class Pacman:
    def __init__(self, screen, graph):
        self.node = 0
        self.screen = screen
        self.graph = graph
        self.node = self.graph.nodes[0]
        self.x = self.node.x
        self.y = self.node.y
        self.move_speed = 0.5
        self.direction = "STOP"

    def move(self):
        if self.direction == "UP" and self.node.neighbors["UP"] is not None:
            self.y += self.move_speed * -1
        if self.direction == "DOWN" and self.node.neighbors["DOWN"] is not None:
            self.y += self.move_speed * 1
        if self.direction == "LEFT" and self.node.neighbors["LEFT"] is not None:
            self.x += self.move_speed * -1
        if self.direction == "RIGHT" and self.node.neighbors["RIGHT"] is not None:
            self.x += self.move_speed * 1

        self.update_node()

    def update_node(self):
        for node in self.graph.nodes:
            if (self.x, self.y) == (node.coordinates):
                self.node = node

    def draw(self):
        pg.draw.circle(self.screen, (255, 255, 0), (self.x, self.y), 20)
