import pygame as pg
from timer import Timer


class Portal:
    def __init__(self, pacman):
        self.portal1_images = [
            pg.transform.scale(
                pg.image.load(f"./assets/images/orange-{n}.png"), (32, 32)
            )
            for n in range(1, 5)
        ]

        self.portal2_images = [
            pg.transform.scale(pg.image.load(f"./assets/images/blue-{n}.png"), (32, 32))
            for n in range(1, 5)
        ]

        self.portal1_timer = Timer(self.portal1_images)
        self.portal2_timer = Timer(self.portal2_images)

        self.pacman = pacman
        self.portal1 = False
        self.portal2 = False
        self.portal1_node = None
        self.portal2_node = None
        self.portal_frame = 0
        self.canTele = True

    def teleport(self, framerate):
        if self.portal1 and self.portal2:
            if (
                self.pacman.onNode
                and self.pacman.node.neighbors["PORTAL"] is not None
                and self.canTele
            ):
                self.portal_frame = framerate
                self.canTele = False
                self.pacman.x = self.pacman.node.neighbors["PORTAL"].x
                self.pacman.y = self.pacman.node.neighbors["PORTAL"].y
                self.pacman.node = self.pacman.node.neighbors["PORTAL"]

            if not self.canTele:
                if self.portal_frame + 200 == framerate:
                    self.canTele = True

    def createPortalPair(self, portal1, portal2):
        portal1.neighbors["PORTAL"] = portal2
        portal2.neighbors["PORTAL"] = portal1

    def deletePortalPair(self, portal1, portal2):
        if portal1:
            portal1.neighbors["PORTAL"] = None

        if portal2:
            portal2.neighbors["PORTAL"] = None

    def createPortal1(self):
        temp = self.pacman.node
        while temp.neighbors[self.pacman.direction]:
            temp = temp.neighbors[self.pacman.direction]

        temp.teleport = True
        self.portal1_node = temp
        self.portal1_x = temp.x
        self.portal1_y = temp.y
        self.portal1_pos = (temp.x - 16, temp.y - 16)
        self.portal1 = True

        self.deletePortalPair(temp, self.portal2_node)

        if self.portal2:
            self.createPortalPair(temp, self.portal2_node)

    def createPortal2(self):
        temp = self.pacman.node
        while temp.neighbors[self.pacman.direction]:
            temp = temp.neighbors[self.pacman.direction]

        temp.teleport = True
        self.portal2_node = temp
        self.portal2_x = temp.x
        self.portal2_y = temp.y
        self.portal2_pos = (temp.x - 16, temp.y - 16)
        self.portal2 = True

        self.deletePortalPair(temp, self.portal1_node)

        if self.portal1:
            self.createPortalPair(temp, self.portal1_node)

    def drawPortal(self, screen, framerate):
        if self.portal1:
            image = self.portal1_timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.portal1_pos
            screen.blit(image, rect)
        if self.portal2:
            image = self.portal2_timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.portal2_pos
            screen.blit(image, rect)

        self.teleport(framerate)
