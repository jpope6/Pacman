import pygame as pg
from settings import *


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = (self.x, self.y)
        self.neighbors = {"LEFT": None, "RIGHT": None, "UP": None, "DOWN": None}

    def add_neighbor(self, neighbor, direction):
        other_direction = None

        if direction == "LEFT":
            other_direction = "RIGHT"
        if direction == "RIGHT":
            other_direction = "LEFT"
        if direction == "UP":
            other_direction = "DOWN"
        if direction == "DOWN":
            other_direction = "UP"

        self.neighbors[direction] = neighbor
        neighbor.neighbors[other_direction] = self

    def draw(self, screen):
        self.circle = pg.draw.rect(screen, WHITE, pg.Rect(self.x, self.y, 1, 1))


class Graph:
    def __init__(self, screen):
        self.nodes = []
        self.add_nodes()
        self.screen = screen

    def add_node(self, node):
        self.nodes[node] = node.neighbors

    def draw_edge(self):
        for node in self.nodes:
            if node.neighbors["DOWN"] is not None:
                pg.draw.line(
                    self.screen,
                    WHITE,
                    node.coordinates,
                    node.neighbors["DOWN"].coordinates,
                )
            if node.neighbors["UP"] is not None:
                pg.draw.line(
                    self.screen,
                    WHITE,
                    node.coordinates,
                    node.neighbors["UP"].coordinates,
                )
            if node.neighbors["LEFT"] is not None:
                pg.draw.line(
                    self.screen,
                    WHITE,
                    node.coordinates,
                    node.neighbors["LEFT"].coordinates,
                )
            if node.neighbors["RIGHT"] is not None:
                pg.draw.line(
                    self.screen,
                    WHITE,
                    node.coordinates,
                    node.neighbors["RIGHT"].coordinates,
                )

    def add_edge(self, node_from, node_to):
        node_from.add_neighbor(node_to)
        self.nodes[node_from] = node_from.neighbors
        self.nodes[node_to] = node_to.neighbors

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1])

    def draw(self):
        for node in self.nodes:
            node.draw(self.screen)

    def add_nodes(self):
        node1 = Node(50, 50)
        node2 = Node(50, 165)
        node1.add_neighbor(node2, "DOWN")

        node3 = Node(200, 50)
        node1.add_neighbor(node3, "RIGHT")

        node4 = Node(200, 165)
        node2.add_neighbor(node4, "RIGHT")
        node3.add_neighbor(node4, "DOWN")

        node5 = Node(375, 50)
        node3.add_neighbor(node5, "RIGHT")

        node6 = Node(375, 165)
        node5.add_neighbor(node6, "DOWN")

        node7 = Node(50, 255)
        node7.add_neighbor(node2, "UP")

        node8 = Node(200, 255)
        node8.add_neighbor(node4, "UP")
        node8.add_neighbor(node7, "LEFT")

        node9 = Node(287.5, 165)
        node9.add_neighbor(node4, "LEFT")
        node9.add_neighbor(node6, "RIGHT")

        node10 = Node(287.5, 255)
        node9.add_neighbor(node10, "DOWN")

        node11 = Node(375, 255)
        node11.add_neighbor(node10, "LEFT")

        node12 = Node(375, 350)
        node12.add_neighbor(node11, "UP")

        node13 = Node(287.5, 350)
        node13.add_neighbor(node12, "RIGHT")

        node14 = Node(287.5, 435)
        node14.add_neighbor(node13, "UP")

        node15 = Node(200, 435)
        node15.add_neighbor(node14, "RIGHT")
        node15.add_neighbor(node8, "UP")

        node16 = Node(287.5, 530)
        node16.add_neighbor(node14, "UP")

        node17 = Node(287.5, 620)
        node17.add_neighbor(node16, "UP")

        node18 = Node(200, 620)
        node18.add_neighbor(node15, "UP")
        node18.add_neighbor(node17, "RIGHT")

        self.nodes = [
            node1,
            node2,
            node3,
            node4,
            node5,
            node6,
            node7,
            node8,
            node9,
            node10,
            node11,
            node12,
            node13,
            node14,
            node15,
            node16,
            node17,
            node18,
        ]
