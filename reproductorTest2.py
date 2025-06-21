import pygame
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading

# === CONFIG ===
AUDIO_FILES = ["assets/songs/jit/Inst.ogg", "assets/songs/jit/Voices.ogg"]
WINDOW_SIZE = (800, 300)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# === LOAD AUDIO ===
data1, sr1 = sf.read(AUDIO_FILES[0])
data2, sr2 = sf.read(AUDIO_FILES[1])

assert sr1 == sr2, "Los audios deben tener la misma frecuencia de muestreo"

samplerate = sr1
position = 0
lastPos = 0;
speed = 1.0
volume1 = 1.0
volume2 = 1.0
lock = threading.Lock()

# === AUDIO CALLBACK ===
def audio_callback(outdata, frames, time, status):
    global position, speed, volume1, volume2
    with lock:
        end = int(position + frames * speed)
        #if end >= len(data1) or end >= len(data2):
        #    outdata[:] = np.zeros((frames, 2))  # silencio
        #    raise sd.CallbackStop

        indices = np.linspace(position, end, frames, endpoint=False).astype(int)

        # Mezclar las dos pistas
        mix = (
            volume1 * data1[indices] +
            volume2 * data2[indices]
        )

        # Evitar saturación
        mix = np.clip(mix, -1.0, 1.0)

        outdata[:] = mix
        position += frames * speed

# === AUDIO THREAD ===
def audio_thread():
    stream = sd.OutputStream(channels=2, callback=audio_callback, samplerate=samplerate)
    stream.start()
    while stream.active:
        pygame.time.wait(100)

threading.Thread(target=audio_thread, daemon=True).start()

# === INIT PYGAME ===
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Reproductor Dual de Audio")
font = pygame.font.SysFont(None, 24)

# === BUTTONS ===
buttons = {
    "Rebobinar": pygame.Rect(20, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Adelantar": pygame.Rect(140, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Ralentizar": pygame.Rect(260, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Normal": pygame.Rect(380, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Salir": pygame.Rect(500, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
}

# === SLIDERS ===
slider1 = pygame.Rect(150, 150, 200, 10)
slider2 = pygame.Rect(150, 200, 200, 10)
knob1 = pygame.Rect(150 + int(volume1 * 200) - 5, 145, 10, 20)
knob2 = pygame.Rect(150 + int(volume2 * 200) - 5, 195, 10, 20)

dragging1 = dragging2 = False

# === FUNCTIONS ===
def draw_buttons():
    for text, rect in buttons.items():
        pygame.draw.rect(screen, (180, 180, 180), rect)
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (rect.x + 10, rect.y + 10))

def handle_button_click(pos):
    global position, speed
    with lock:
        if buttons["Rebobinar"].collidepoint(pos):
            position = max(0, position - samplerate * 5)
        elif buttons["Adelantar"].collidepoint(pos):
            position = min(len(data1), position + samplerate * 5)
        elif buttons["Ralentizar"].collidepoint(pos):
            speed = 0.5
        elif buttons["Normal"].collidepoint(pos):
            speed = 1.0
        elif buttons["Salir"].collidepoint(pos):
            pygame.quit()
            exit()

def draw_slider(rect, knob, label):
    pygame.draw.rect(screen, (100, 100, 100), rect)
    pygame.draw.rect(screen, (255, 0, 0), knob)
    txt = font.render(label, True, (255, 255, 255))
    screen.blit(txt, (rect.x - 120, rect.y - 5))

# === MAIN LOOP ===
running = True
while running:
    screen.fill((30, 30, 30))
    draw_buttons()

    draw_slider(slider1, knob1, "Volumen Pista 1")
    draw_slider(slider2, knob2, "Volumen Pista 2")

    speed = (pygame.mouse.get_pos()[0]-400)/200;
    #position = (pygame.mouse.get_pos()[0]/WINDOW_SIZE[0])*len(data1);
    #if position != lastPos:speed = 1;
    #else:speed = 0;
    #lastPos = position;


    # Barra de progreso
    with lock:
        progress = int((position / len(data1)) * (WINDOW_SIZE[0] - 40))
    pygame.draw.rect(screen, (0, 255, 0), (20, 250, progress, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if knob1.collidepoint(event.pos):
                dragging1 = True
            elif knob2.collidepoint(event.pos):
                dragging2 = True
            else:
                handle_button_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging1 = dragging2 = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging1:
                knob1.x = max(slider1.x, min(slider1.x + slider1.width - 10, event.pos[0] - 5))
                volume1 = (knob1.x - slider1.x) / slider1.width
            elif dragging2:
                knob2.x = max(slider2.x, min(slider2.x + slider2.width - 10, event.pos[0] - 5))
                volume2 = (knob2.x - slider2.x) / slider2.width

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
