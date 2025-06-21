import moderngl as mgl;
import pygame as pg;
from engine import sprites as spr;
from engine import screen as sc;

textures = {};
sprites = {};
sounds = {};

def load_backgrounds(files):
    #files = glob.glob('assets/backgrounds/*.png');
    for file in files:
        image = pg.image.load(file[1]).convert_alpha();
        textures[file[0]] = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
        textures[file[0]].filter = (mgl.LINEAR, mgl.LINEAR);
        print("el fondo: "+file[0]+"; se cargo correctamente we.");

def load_sprites(files):
    #files = glob.glob('assets/sprites/*.png');
    for file in files:
        image = pg.image.load(file[1]+'.png').convert_alpha();
        textures[file[0]] = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
        textures[file[0]].filter = (mgl.LINEAR, mgl.LINEAR);
        sprites[file[0]] = spr.Sprite(file[1]+'.xml',textures[file[0]].size);
        print("el sprite: "+file[0]+"; se cargo correctamente we.");
        
def load_sounds(files):
    #files = glob.glob('assets/sounds/*.ogg');
    for file in files:
        sounds[file[0]] = pg.mixer.Sound(file[1]);
        print("el sonido: "+file[0]+"; se cargo correctamente we.");