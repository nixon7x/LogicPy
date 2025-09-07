import pygame
import random
# gates.py
# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GRAY = (180, 180, 180)
YELLOW = (255, 255, 100)
WIRE_COLORS = [(0, 0, 0), (50, 50, 200), (200, 50, 50)]
BLUE = (0, 100, 255)

# -----------------------------
# Mantık Kapıları Sınıfı
# -----------------------------
class MyGate:
    def __init__(self, x, y, gate_type):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 50
        self.type = gate_type
        self.state = False
        self.color = BLUE
        self._update_slots()

    def _update_slots(self):
        # Giriş slotları
        if self.type == "NOT":
            self.inputs = [(self.x - 10, self.y + self.height // 2)]
        else:
            self.inputs = [(self.x - 10, self.y + 15), (self.x - 10, self.y + self.height - 15)]
        # Çıkış slotu
        self.output = (self.x + self.width + 10, self.y + self.height // 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=12)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2, border_radius=12)
        font = pygame.font.SysFont("Arial", 18)
        text = font.render(self.type, True, WHITE)
        surface.blit(text, (self.x + 10, self.y + 15))

        for slot in self.inputs:
            pygame.draw.circle(surface, BLACK, slot, 5)
        pygame.draw.circle(surface, BLACK, self.output, 5)

    def calculate(self, input_states):
        if self.type == "AND":
            self.state = all(input_states)
        elif self.type == "OR":
            self.state = any(input_states)
        elif self.type == "NOT":
            self.state = not input_states[0] if input_states else False
        elif self.type == "NAND":
            self.state = not all(input_states)
        elif self.type == "NOR":
            self.state = not any(input_states)
        elif self.type == "XOR":
            if len(input_states) == 2:
                self.state = input_states[0] != input_states[1]
            else:
                self.state = False
        elif self.type == "XNOR":
            if len(input_states) == 2:
                self.state = input_states[0] == input_states[1]
            else:
                self.state = False
        return self.state

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height



    def get_slot_clicked(self, pos):
        for slot in self.inputs:
            if (pos[0]-slot[0])**2 + (pos[1]-slot[1])**2 < 25:
                return slot
        if (pos[0]-self.output[0])**2 + (pos[1]-self.output[1])**2 < 25:
            return self.output
        return None

# -----------------------------
# Anahtar Sınıfı
# -----------------------------
class MySwitch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.state = False
        self._update_slot()

    def _update_slot(self):
        self.output = (self.x + self.width + 10, self.y + self.height // 2)

    def toggle(self):
        self.state = not self.state

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height), border_radius=10)
        color = GREEN if self.state else RED
        pygame.draw.circle(surface, color, (self.x + (self.width - 10 if self.state else 10), self.y + self.height // 2), 8)
        pygame.draw.circle(surface, BLACK, self.output, 5)

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def get_slot_clicked(self, pos):
        if (pos[0]-self.output[0])**2 + (pos[1]-self.output[1])**2 < 25:
            return self.output
        return None

# -----------------------------
# LED Sınıfı
# -----------------------------
class MyLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.state = False
        self._update_slot()

    def _update_slot(self):
        self.inputs = [(self.x - 10, self.y + self.height // 2)]

    def draw(self, surface):
        color = GREEN if self.state else GRAY
        pygame.draw.ellipse(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, BLACK, self.inputs[0], 5)

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def get_slot_clicked(self, pos):
        if (pos[0]-self.inputs[0][0])**2 + (pos[1]-self.inputs[0][1])**2 < 25:
            return self.inputs[0]
        return None

# -----------------------------
# Kablo Sınıfı
# -----------------------------
class MyWire:
    def __init__(self, start_comp, start_slot, end_comp=None, end_slot=None):
        self.start_comp = start_comp
        self.start_slot = start_slot
        self.end_comp = end_comp
        self.end_slot = end_slot
        self.color = random.choice(WIRE_COLORS)
        # Noktalar listesi: başta sadece start noktası var
        self.points = [start_slot]

    def add_point(self, pos):
        self.points.append(pos)

    def draw(self, surface):
        # Eğer end_slot mevcutsa onu da ekle
        pts = self.points[:]
        if self.end_slot:
            pts.append(self.end_slot)
        if len(pts) > 1:
            pygame.draw.lines(surface, self.color, False, pts, 3)

    def transfer_signal(self):
        if self.end_comp and hasattr(self.end_comp, 'state'):
            self.end_comp.state = self.start_comp.state

    def is_clicked(self, pos):
        # Basit yakınlık kontrolü: her segment için kontrol et
        for i in range(len(self.points)-1):
            start = self.points[i]
            end = self.points[i+1]
            dist = abs((end[1]-start[1])*pos[0] - (end[0]-start[0])*pos[1] + end[0]*start[1] - end[1]*start[0]) / ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5
            if dist < 5:
                return True
        return False
