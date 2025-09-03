import pygame as pg;
import moderngl as mgl;
import glm;
import json as js;
import os;
from engine import renderer as ren;
from engine import musicPlayer as mup;

pg.init();

real_res = (1280,720);
real_mouse = glm.vec2(0,0);

pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3);
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3);
pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE);
win = pg.display.set_mode(real_res,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE);
pg.display.set_caption("PyFunkin");
ctx = mgl.create_context(require=330);
#ctx.enable(flags=mgl.DEPTH_TEST);
clock = pg.time.Clock();
deltatime = 0;

ctx.enable(mgl.BLEND);
ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA);

texture = ctx.texture((1280,720), 4);
texture.filter = (mgl.LINEAR, mgl.LINEAR);
#drb = ctx.depth_renderbuffer((960,540));
screen_fbo = ctx.framebuffer(color_attachments=[texture]);
proj = glm.ortho(0.0, 1280.0, 720.0, 0.0, -1000.0, 1000.0);

texture3d = ctx.texture((1280,720), 3);
texture3d.filter = (mgl.LINEAR, mgl.LINEAR);
drb = ctx.depth_renderbuffer((1280,720));
screen3d_fbo = ctx.framebuffer(color_attachments=[texture3d],depth_attachment=drb);

render = ren.Renderer();

vcrTex = None;
vcrSpr = None;
state = None;

if os.path.exists(os.getenv('APPDATA')+"\\PyFunkin\\config.json"):
    with open(os.getenv('APPDATA')+"\\PyFunkin\\config.json","r") as json:
        config = js.load(json);
else:
    config = {
        "keys":{
            "leftA":pg.K_a,
            "downA":pg.K_s,
            "upA":pg.K_w,
            "rightA":pg.K_d,
            "leftB":pg.K_LEFT,
            "downB":pg.K_DOWN,
            "upB":pg.K_UP,
            "rightB":pg.K_RIGHT,
            "menu left":pg.K_LEFT,
            "menu down":pg.K_DOWN,
            "menu up":pg.K_UP,
            "menu right":pg.K_RIGHT,
            "vol-":pg.K_MINUS,
            "vol+":pg.K_PLUS,
            "accept":pg.K_RETURN,
            "back":pg.K_ESCAPE
        },
        "botplay":False,
        "downscroll":False,
        "volumen":1
    };

song = "TomachiP";
botplay = True;
trueVol = config["volumen"]*config["volumen"];
mp = mup.musicPlayer("assets/songs/menu.ogg",trueVol);

fulScr = False;

#pg.event.set_grab(True);

#font = pg.font.Font("assets/Moderniz.otf",12);

def save_data():
    path = os.getenv('APPDATA')+"\\PyFunkin";
    if not os.path.exists(path):
        os.makedirs(path);
    with open(path+"\\config.json","w") as json:
        json.write(js.dumps(config));