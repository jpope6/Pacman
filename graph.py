import pygame as pg
from settings import *


class Node:
    def __init__(self, coordinates):
        self.coordinates = coordinates
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
        pg.draw.circle(screen, WHITE, self.coordinates, 20)


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
        node1 = Node((50, 50))
        node2 = Node((50, 170))
        node1.add_neighbor(node2, "DOWN")

        node3 = Node((200, 50))
        node1.add_neighbor(node3, "RIGHT")

        node4 = Node((200, 170))
        node2.add_neighbor(node4, "RIGHT")
        node3.add_neighbor(node4, "DOWN")

        self.nodes = [node1, node2, node3, node4]
