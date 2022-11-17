import pygame as pg


class Pacman:
    def __init__(self, screen, graph):
        self.node = None
        self.screen = screen
        self.graph = graph
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.target = None
        self.x = self.node.x
        self.y = self.node.y
        self.move_speed = 0.5
        self.direction = "STOP"
        self.target_direction = "STOP"
        self.onNode = True
        self.radius = 20

    def move(self):
        self.change_direction()
        self.update_node()
        self.teleport_node()

        if self.direction == "UP" and self.node.neighbors["UP"] is not None:
            self.y += self.move_speed * -1
            self.target = self.node.neighbors["UP"]
        if self.direction == "DOWN" and self.node.neighbors["DOWN"] is not None:
            self.y += self.move_speed * 1
            self.target = self.node.neighbors["DOWN"]
        if self.direction == "LEFT" and self.node.neighbors["LEFT"] is not None:
            self.x += self.move_speed * -1
            self.target = self.node.neighbors["LEFT"]
        if self.direction == "RIGHT" and self.node.neighbors["RIGHT"] is not None:
            self.x += self.move_speed * 1
            self.target = self.node.neighbors["RIGHT"]

        # print(self.x, ", ", self.y)

    def update_node(self):
        for node in self.graph.nodes:
            if node.circle.collidepoint(self.x, self.y):
                self.node = node
                self.onNode = True
                break
            else:
                self.onNode = False

    def change_direction(self):
        if self.onNode:
            self.direction = self.target_direction

        # allows you to turn around
        if self.target and self.target.neighbors[self.target_direction] == self.node:
            self.direction = self.target_direction
            temp = self.node
            self.node = self.target
            self.target = temp

    def teleport_node(self):
        if self.x < 1 and self.direction == "LEFT":
            self.x = self.graph.node_right.x
            self.node = self.graph.node_right

        if self.x > 845 and self.direction == "RIGHT":
            self.x = self.graph.node_left.x
            self.node = self.graph.node_left

    def draw(self):
        pg.draw.circle(self.screen, (255, 255, 0), (self.x, self.y), self.radius)
