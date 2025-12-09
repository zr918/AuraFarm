# objects that move across the screen

class PhysicalEntities:
    def __init__(self, screen, e_type, pos, size):
        self.screen = screen
        self.type = e_type
        self.pos = pos
        self.size = size

    def pos(self):   # returns position
        return self.pos

    def size(self):  #returns size
        return self.size
