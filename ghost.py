import pygame as pg


class Ghost:
    def __init__(self, screen, graph):
        self.screen = screen
        self.graph = graph
        self.x = 0
        self.y = 0


class Blinky(Ghost):
    def __init__(self, screen, graph):
        super().__init__(screen, graph)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = self.node.x
        self.y = self.node.y

    def draw(self):
        pg.draw.rect(
            self.screen, (255, 0, 0), pg.Rect(self.x - 15, self.y - 15, 30, 30)
        )
