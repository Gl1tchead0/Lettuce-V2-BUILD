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
    #sc.ctx.clear();
    sc.screen_fbo.use();
    #sc.ctx.clear(color=(0,0,0));
    sc.state.draw();
    #dibujar weas del hud
    sc.render.s_rect(glm.vec2(10+min(0,volAnim),20),glm.vec2(50,80),glm.vec4(0,0,0,0.5));
    sc.render.draw_simple_poly(((20+min(0,volAnim),30),(50+min(0,volAnim),30),(20+min(0,volAnim),90)),(0.25,0.25,0.25))
    sc.render.draw_simple_poly(((20+min(0,volAnim),90-60*sc.config["volumen"]),(20+min(0,volAnim)+30*sc.config["volumen"],90-60*sc.config["volumen"]),(20+min(0,volAnim),90)),(1,1,1))
    sc.render.draw_text(None,"FPS:"+str(int(glm.floor(sc.clock.get_fps()))),glm.vec2(0,0),glm.vec3(0.7,0.7,0.7),10,16);
    
def refresh_screen():
    #draw screen
    sc.ctx.screen.use();
    #sc.ctx.clear();
    sc.ctx.clear(color=(0,0,0));
    sc.render.draw_screen(sc.texture);

def loadState(state):
    sc.state = il.import_module("states."+state).State();
    fondo2load, sprites2load, sounds2load = sc.state.load();
    ass.load_backgrounds(fondo2load)
    ass.load_sprites(sprites2load)
    ass.load_sounds(sounds2load)

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
                if event.key == sc.config["keys"]["menu left"]:p_L = True;
                if event.key == sc.config["keys"]["menu down"]:p_D = True;
                if event.key == sc.config["keys"]["menu up"]:p_U = True;
                if event.key == sc.config["keys"]["menu right"]:p_R = True;
        
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
        sc.state.update(keypress);
        #draw
        refresh();
        refresh_screen();
        pg.display.flip(); 
        sc.deltatime = sc.clock.tick(60) * 0.001;