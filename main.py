import pygame
import sys
import random
import json
from gates import MyGate, MySwitch, MyLight, MyWire
# main.py
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 1000, 600
SIDEBAR_WIDTH = 200
COMPONENT_BUTTON_HEIGHT = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LogicPy")  # Proje ismi

WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

font = pygame.font.SysFont("Arial", 18)

# Sidebar komponentleri
COMPONENTS = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR", "Switch", "LED"]

# Eleman listeleri
gates = []
switches = []
leds = []
wires = []

selected_component = None
dragging_component = None
current_wire = None

# -----------------------------
# Sidebar çizimi
# -----------------------------
def draw_sidebar():
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SIDEBAR_WIDTH, HEIGHT), border_radius=0)
    for i, name in enumerate(COMPONENTS):
        rect = pygame.Rect(10, 10 + i*(COMPONENT_BUTTON_HEIGHT+10), SIDEBAR_WIDTH-20, COMPONENT_BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x+10, rect.y+10))

        # Seçilen elemanı vurgula
        if name == selected_component:
            pygame.draw.rect(screen, BLUE, rect, 3, border_radius=8)  # Mavi çerçeve ile göster

def save_circuit(filename="circuit.json"):
    data = {
        "gates": [{"x": g.x, "y": g.y, "type": g.gate_type, "state": g.state} for g in gates],
        "switches": [{"x": s.x, "y": s.y, "state": s.state} for s in switches],
        "leds": [{"x": l.x, "y": l.y, "state": l.state} for l in leds],
        "wires": [{
            "start_idx": (gates + switches).index(w.start_comp),
            "start_slot": w.start_slot,
            "end_idx": (gates + leds).index(w.end_comp),
            "end_slot": w.end_slot,
            "color": w.color
        } for w in wires]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Circuit saved!")

def load_circuit(filename="circuit.json"):
    global gates, switches, leds, wires
    with open(filename, "r") as f:
        data = json.load(f)

    gates = [MyGate(g["x"], g["y"], g["type"]) for g in data["gates"]]
    for g, g_data in zip(gates, data["gates"]):
        g.state = g_data["state"]

    switches = [MySwitch(s["x"], s["y"]) for s in data["switches"]]
    for s, s_data in zip(switches, data["switches"]):
        s.state = s_data["state"]

    leds = [MyLight(l["x"], l["y"]) for l in data["leds"]]
    for l, l_data in zip(leds, data["leds"]):
        l.state = l_data["state"]

    wires = []
    for w_data in data["wires"]:
        start_list = gates + switches
        end_list = gates + leds
        start_comp = start_list[w_data["start_idx"]]
        end_comp = end_list[w_data["end_idx"]]
        wires.append(MyWire(start_comp, w_data["start_slot"], end_comp, w_data["end_slot"], w_data["color"]))
    print("Circuit loaded!")

# -----------------------------
# Ana döngü
# -----------------------------
running = True
while running:
    screen.fill(WHITE)
    draw_sidebar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_circuit()
            elif event.key == pygame.K_l:
                load_circuit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol tık
                # Sidebardan seçim
                if event.pos[0] < SIDEBAR_WIDTH:
                    for i, name in enumerate(COMPONENTS):
                        rect = pygame.Rect(10, 10 + i*(COMPONENT_BUTTON_HEIGHT+10), SIDEBAR_WIDTH-20, COMPONENT_BUTTON_HEIGHT)
                        if rect.collidepoint(event.pos):
                            selected_component = name
                            break

                # Switch tıklama
                for s in switches:
                    if s.is_clicked(event.pos):
                        s.toggle()

                # Eleman sürükleme
                for c in gates + switches + leds:
                    if c.is_clicked(event.pos):
                        dragging_component = c

                # Slot tıklama (kablo başlatma/bağlama)
                for c in gates + switches + leds:
                    slot = c.get_slot_clicked(event.pos) if hasattr(c, "get_slot_clicked") else None
                    if slot:
                        if current_wire is None:
                            current_wire = MyWire(c, slot)  # MyWire nesnesi olarak başlat
                        else:
                            current_wire.start_comp
                            current_wire.start_slot
                            current_wire.end_comp = c
                            current_wire.end_slot = slot
                            wires.append(current_wire)
                            current_wire = None

                # Sidebardan seçilen elemanı yerleştirme
                if selected_component and event.pos[0] > SIDEBAR_WIDTH:
                    if selected_component in ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]:
                        gates.append(MyGate(event.pos[0], event.pos[1], selected_component))
                    elif selected_component == "Switch":
                        switches.append(MySwitch(event.pos[0], event.pos[1]))
                    elif selected_component == "LED":
                        leds.append(MyLight(event.pos[0], event.pos[1]))
                    selected_component = None

                # Oluşturulmakta olan kabloyu çiz ve bükme noktası ekleme
                if current_wire and event.button == 1:
                    # Sol tık ile yeni bükme noktası ekleme
                    if pygame.mouse.get_pressed()[0]:  # Sol fare tuşu basılıysa
                        mouse_pos = pygame.mouse.get_pos()
                        # Son noktadan çok uzaksa yeni nokta ekle (gereksiz çoklu eklemeyi önler)
                        if (mouse_pos[0]-current_wire.points[-1][0])**2 + (mouse_pos[1]-current_wire.points[-1][1])**2 > 25:
                            current_wire.add_point(mouse_pos)

                    # Mevcut noktaları çiz + fare pozisyonu (kablo bitmeden)
                    pts = current_wire.points + [pygame.mouse.get_pos()]
                    if len(pts) > 1:
                        pygame.draw.lines(screen, BLACK, False, pts, 3)
                    # Öncelikle kablo silme
            elif event.button == 3:  # Sağ tık
                # Kablo sil
                for w in wires:
                    if w.is_clicked(event.pos):
                        wires.remove(w)
                        break
                else:
                    # Eleman sil
                    for comp_list in [gates, switches, leds]:
                        for c in comp_list:
                            if c.is_clicked(event.pos):
                                wires[:] = [w for w in wires if w.start_comp != c and w.end_comp != c]
                                comp_list.remove(c)
                                break

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_component = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_component:
                dragging_component.x, dragging_component.y = event.pos
                if hasattr(dragging_component, "_update_slots"):
                    dragging_component._update_slots()

    # Mantık kapısı hesaplamaları
    for gate in gates:
        inputs = []
        for w in wires:
            if w.end_comp == gate:
                if hasattr(w.start_comp, "state"):
                    inputs.append(w.start_comp.state)
        gate.calculate(inputs)

    # LED durum güncellemesi
    for led in leds:
        for w in wires:
            if w.end_comp == led:
                led.state = w.start_comp.state

    # Elemanları çiz
    for gate in gates:
        gate.draw(screen)
    for s in switches:
        s.draw(screen)
    for led in leds:
        led.draw(screen)

    # Kabloları çiz
    for w in wires:
        w.draw(screen)
        w.transfer_signal()

    # Oluşturulmakta olan kabloyu çiz
# Oluşturulmakta olan kabloyu çiz (bükme noktaları ile)
    if current_wire:
        pts = current_wire.points + [pygame.mouse.get_pos()]
        if len(pts) > 1:
            pygame.draw.lines(screen, BLACK, False, pts, 3)

    pygame.display.flip()

pygame.quit()
sys.exit()
