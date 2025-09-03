import pygame as pg;
import sys;
import glm;
import moderngl as mgl;
from engine import sprites as spr;
from engine import screen as sc;
from engine import assets as ass;
import importlib as il;

volAnim = -60;

def refresh():
    #draw
    sc.screen3d_fbo.use();
    sc.proj = glm.perspective(1.5707963267948966192313216916398,1.7777777777777777777777777777778,1,100000);

    look = glm.vec3(0,0,0);
    up = glm.vec3(0,0,0);
    sinX = glm.sin(sc.render.camR.x);cosX = glm.cos(sc.render.camR.x);
    sinY = glm.sin(sc.render.camR.y);cosY = glm.cos(sc.render.camR.y);
    sinZ = glm.sin(sc.render.camR.z);cosZ = glm.cos(sc.render.camR.z);
    look.z = cosX * cosY;
    look.x = cosX * sinY;
    look.y = sinX;

    up.x = sinZ * cosY;
    up.z = sinZ * sinY;
    up.y = -cosZ;

    sc.render.camT = glm.lookAt(sc.render.camP,sc.render.camP+look,up);

    sc.state.draw();
    sc.screen_fbo.use();
    sc.ctx.clear(0,0,0,0)
    sc.proj = glm.ortho(0.0, 1280.0, 720.0, 0.0, -1000.0, 1000.0);
    sc.render.camT = glm.mat4x4();
    sc.state.drawHUD();
    #dibujar weas del hud
    sc.render.s_rect(glm.vec2(10+min(0,volAnim),20),glm.vec2(50,80),glm.vec4(0,0,0,0.5));
    sc.render.draw_simple_poly(((20+min(0,volAnim),30,0),(50+min(0,volAnim),30,0),(20+min(0,volAnim),90,0)),(0.25,0.25,0.25))
    sc.render.draw_simple_poly(((20+min(0,volAnim),90-60*sc.config["volumen"],0),(20+min(0,volAnim)+30*sc.config["volumen"],90-60*sc.config["volumen"],0),(20+min(0,volAnim),90,0)),(1,1,1))
    sc.render.draw_text(None,"FPS:"+str(int(glm.floor(sc.clock.get_fps()))),glm.vec2(0,0),glm.vec3(0.7,0.7,0.7),10,16);
    
def refresh_screen():
    #draw screen
    sc.ctx.screen.use();
    #sc.ctx.clear();
    sc.ctx.clear(color=(0,0,0));
    sc.render.draw_screen(sc.texture3d);
    sc.render.draw_screen(sc.texture);

def loadState(state):
    sc.state = None;
    sc.state = il.import_module("states."+state).State();
    fondo2load, sprites2load, sounds2load, models2load = sc.state.load();
    ass.load_backgrounds(fondo2load)
    ass.load_sprites(sprites2load)
    ass.load_sounds(sounds2load)
    ass.load_models(models2load);
    sc.deltatime = 0;

if __name__ == '__main__':
    #loadState("playState");
    loadState("menuState");
    
    image = pg.image.load('assets/images/vcr.png').convert_alpha();
    sc.vcrTex = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
    sc.vcrTex.filter = (mgl.LINEAR, mgl.LINEAR);
    sc.vcrSpr = spr.Sprite('assets/images/vcr.xml',sc.vcrTex.size);
    del image;
    
    while True:
        keypress = None;
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sc.save_data();
                sys.exit();
            if event.type == pg.KEYDOWN:
                keypress = event.key;
                if event.key == pg.K_F11:
                    if sc.fulScr:
                        sc.win = pg.display.set_mode((1280,720),flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE);
                        sc.fulScr = False;
                    else:
                        sc.win = pg.display.set_mode((0,0),flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE | pg.FULLSCREEN);
                        sc.fulScr = True;
                    sc.real_res = sc.win.get_size();
                    sc.ctx.screen.viewport = (0,0,sc.real_res[0],sc.real_res[1]);
        
                if event.key == sc.config["keys"]["vol-"]:
                    sc.config["volumen"] = max(0,sc.config["volumen"]-0.1);
                    sc.trueVol = sc.config["volumen"]*sc.config["volumen"];
                    ass.update_sounds_vol();
                    ass.sounds["beep"].play();
                    volAnim = 150;
                if event.key == sc.config["keys"]["vol+"]:
                    sc.config["volumen"] = min(1,sc.config["volumen"]+0.1);
                    sc.trueVol = sc.config["volumen"]*sc.config["volumen"];
                    ass.update_sounds_vol();
                    ass.sounds["beep"].play();
                    volAnim = 150;
            if event.type == pg.VIDEORESIZE:
                width, height = event.size;
                sc.real_res = event.size;
                sc.ctx.screen.viewport = (0,0,width,height);
        sc.render.ajust_screen();
        #update
        volAnim = max(-60,volAnim-sc.deltatime*100);
        if sc.state.update(keypress):
            refresh();
            refresh_screen();
            pg.display.flip(); 
            sc.clock.tick(60)
            sc.deltatime = 0;
            continue;
        #draw
        refresh();
        refresh_screen();
        pg.display.flip(); 
        sc.deltatime = sc.clock.tick(60) * 0.001;