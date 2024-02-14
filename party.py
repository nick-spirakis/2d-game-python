import pygame

class Party:
    def __init__(self, main_player):
        self.members = []
        self.main_player = main_player

    def add_member(self, character):
        self.members.append(character)

    def remove_member(self, character):
        self.members.remove(character)

    def update(self, dt):
        for member in self.members:
            member.update(dt)
