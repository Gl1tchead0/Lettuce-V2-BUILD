import pygame
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading

# === CONFIG ===
AUDIO_FILE = "assets/songs/jit/Inst.ogg"
WINDOW_SIZE = (600, 200)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# === LOAD AUDIO ===
data, samplerate = sf.read(AUDIO_FILE)
lastPos = 0;
position = 0
speed = 1.0
lock = threading.Lock()

# === AUDIO CALLBACK ===
def audio_callback(outdata, frames, time, status):
    global position, speed
    with lock:
        end = int(position + frames * speed)
        if end >= len(data):
            outdata[:] = np.zeros((frames, data.shape[1]))
            raise sd.CallbackStop
        indices = np.linspace(position, end, frames, endpoint=False).astype(int)
        outdata[:] = data[indices]
        position += frames * speed

# === AUDIO THREAD ===
def audio_thread():
    stream = sd.OutputStream(channels=data.shape[1], callback=audio_callback, samplerate=samplerate)
    stream.start()
    while stream.active:
        pygame.time.wait(100)

threading.Thread(target=audio_thread, daemon=True).start()

# === INIT PYGAME ===
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Reproductor OGG en Pygame")
font = pygame.font.SysFont(None, 24)

# === BUTTONS ===
buttons = {
    "Rebobinar": pygame.Rect(20, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Adelantar": pygame.Rect(140, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Ralentizar": pygame.Rect(260, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Normal": pygame.Rect(380, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Salir": pygame.Rect(500, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
}

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
            position = min(len(data), position + samplerate * 5)
        elif buttons["Ralentizar"].collidepoint(pos):
            speed = 0.5
        elif buttons["Normal"].collidepoint(pos):
            speed = 1.0
        elif buttons["Salir"].collidepoint(pos):
            pygame.quit()
            exit()

# === MAIN LOOP ===
running = True
while running:
    screen.fill((30, 30, 30))
    draw_buttons()

    #speed = (pygame.mouse.get_pos()[0]-300)/150;
    position = (pygame.mouse.get_pos()[0]/600)*len(data);
    if position != lastPos:speed = 1;
    else:speed = 0;
    lastPos = position;

    # Mostrar progreso
    with lock:
        progress = int((position / len(data)) * (WINDOW_SIZE[0] - 40))
    pygame.draw.rect(screen, (0, 255, 0), (20, 150, progress, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass#handle_button_click(event.pos)

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
