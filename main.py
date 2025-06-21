import pygame as pg;
import sys;
import glm;
import moderngl as mgl;
from engine import sprites as spr;
from engine import screen as sc;
from engine import assets as ass;
import importlib as il;

def refresh():
    #draw
    sc.ctx.clear();
    sc.screen_fbo.use();
    sc.ctx.clear(color=(1,1,1));
    sc.state.draw();
    sc.render.draw_text(None,"FPS:"+str(int(glm.floor(sc.clock.get_fps()))),glm.vec2(0,0),glm.vec3(0.7,0.7,0.7),10,16);
    
def refresh_screen():
    #draw screen
    sc.ctx.screen.use();
    sc.ctx.clear();
    sc.ctx.clear(color=(0,0,0));
    sc.render.draw_screen(sc.texture);

def loadState(state):
    sc.state = il.import_module("states."+state).State();
    fondo2load, sprites2load = sc.state.load();
    ass.load_backgrounds(fondo2load)
    ass.load_sprites(sprites2load)

if __name__ == '__main__':
    loadState("playState");
    
    image = pg.image.load('assets/images/vcr.png').convert_alpha();
    sc.vcrTex = sc.ctx.texture(size=image.get_size(), components=4, data=pg.image.tostring(image,"RGBA"));
    sc.vcrTex.filter = (mgl.LINEAR, mgl.LINEAR);
    sc.vcrSpr = spr.Sprite('assets/images/vcr.xml',sc.vcrTex.size);
    del image;
    
    while True:
        p_L = False;p_R = False;p_U = False;p_D = False;
        p_acept = False;p_back = False;
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit();
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:p_U = True;
                if event.key == pg.K_s:p_D = True;
                if event.key == pg.K_a:p_L = True;
                if event.key == pg.K_d:p_R = True;
                if event.key == pg.K_UP:p_U = True;
                if event.key == pg.K_DOWN:p_D = True;
                if event.key == pg.K_LEFT:p_L = True;
                if event.key == pg.K_RIGHT:p_R = True;
                if event.key == pg.K_RETURN:p_acept = True;
                if event.key == pg.K_ESCAPE:p_back = True;
            if event.type == pg.VIDEORESIZE:
                width, height = event.size;
                sc.real_res = event.size;
                sc.ctx.screen.viewport = (0,0,width,height);
        sc.render.ajust_screen();
        #update
        sc.state.update(p_L,p_R,p_U,p_D,p_acept,p_back);
        #draw
        refresh();
        refresh_screen();
        pg.display.flip(); 
        sc.deltatime = sc.clock.tick(60) * 0.001;