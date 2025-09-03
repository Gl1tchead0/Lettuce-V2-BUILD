import moderngl as mgl;
import pygame as pg;
import pywavefront as pw;
import numpy as np;
from engine import sprites as spr;
from engine import screen as sc;

textures = {};
sprites = {};
sounds = {};
models = {};

def load_backgrounds(files):
    #files = glob.glob('assets/backgrounds/*.png');
    textures.clear();
    for file in files:
        image = pg.image.load(file[1]).convert_alpha();
        textures[file[0]] = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
        textures[file[0]].filter = (mgl.LINEAR, mgl.LINEAR);
        print("el fondo: "+file[0]+"; se cargo correctamente we.");

def load_sprites(files):
    #files = glob.glob('assets/sprites/*.png');
    sprites.clear();
    for file in files:
        image = pg.image.load(file[1]+'.png').convert_alpha();
        textures[file[0]] = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
        textures[file[0]].filter = (mgl.LINEAR, mgl.LINEAR);
        sprites[file[0]] = spr.Sprite(file[1]+'.xml',textures[file[0]].size);
        print("el sprite: "+file[0]+"; se cargo correctamente we.");
        
def load_sounds(files):
    #files = glob.glob('assets/sounds/*.ogg');
    sounds.clear();
    for file in files:
        sounds[file[0]] = pg.mixer.Sound(file[1]);
        sounds[file[0]].set_volume(sc.trueVol);
        print("el sonido: "+file[0]+"; se cargo correctamente we.");

def load_models(files):
    models.clear();
    for file in files:
        #cargar vertices
        obj = pw.Wavefront(file[1]+".obj",create_materials=True,parse=True);
        vertex_data = obj.materials.popitem()[1].vertices;
        vertex_data = np.array(vertex_data,dtype='f4');
        vbo = sc.ctx.buffer(vertex_data);
        #cargar datos
        data = open(file[1]+".mdf").readlines();
        vert_shad = "";
        frag_shad = "";
        data_type = "";
        data_name = [];
        for dat in data:
            if dat[:-(len(dat)-4)] == "v_s ":
                vert_shad = dat[4:-1];
            elif dat[:-(len(dat)-4)] == "f_s ":
                frag_shad = dat[4:-1];
            elif dat[:-(len(dat)-4)] == "d_t ":
                data_type = dat[4:-1];
            elif dat[:-(len(dat)-4)] == "d_n ":
                data_name.append(dat[4:-1]);
        #cargar shader
        vert = open(f'assets/shaders3D/{vert_shad}.vert').read()
        frag = open(f'assets/shaders3D/{frag_shad}.frag').read()
        program = sc.ctx.program(vertex_shader=vert, fragment_shader=frag);
        #crear el vao de mierd
        vbod = [vbo,data_type];
        for na in data_name:
            vbod.append(na);
        models[file[0]] = sc.ctx.vertex_array(program,[tuple(vbod)]);
        
def update_sounds_vol():
    for sound in sounds.values():
        sound.set_volume(sc.trueVol);