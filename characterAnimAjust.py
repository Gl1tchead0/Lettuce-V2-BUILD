import pygame as pg;
import sys;
import glm;
import json;
import os;
from engine import sprites as spr;
from engine import screen as sc;
from engine import assets as ass;

char = "ruber";
anim = 0;
frame = 0;
ghost = 0;
cam = glm.vec2(-640,-360);

lastMouse = [0,0];

poses = {};

if __name__ == '__main__':
    ass.load_sprites([(char,'assets/characters/'+char+'/sprite')]);
    anims = list(ass.sprites[char].anims.keys());
    animsc = len(anims);

    if os.path.exists('assets/characters/'+char+'/sprite.json'):
        with open('assets/characters/'+char+'/sprite.json', 'r') as file:
            poses = json.load(file);
    else:
        for an in anims:
            poses[an] = [0,0];
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit();
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    anim = (anim - 1) % animsc;
                if event.key == pg.K_s:
                    anim = (anim + 1) % animsc;
                if event.key == pg.K_SPACE:
                    ghost = anim;
                if event.key == pg.K_RETURN:
                    with open('assets/characters/'+char+'/sprite.json', 'w') as file:
                        json.dump(poses, file);
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 2:
                    lastMouse = pg.mouse.get_pos();
            if event.type == pg.VIDEORESIZE:
                width, height = event.size;
                sc.real_res = event.size;
                sc.ctx.screen.viewport = (0,0,width,height);
        sc.render.ajust_screen();
        #update
        frame = (frame + sc.deltatime*24) % len(ass.sprites[char].anims[anims[anim]]);
        if pg.mouse.get_pressed()[0]:
            poses[anims[anim]][0] += lastMouse[0]-pg.mouse.get_pos()[0];
            poses[anims[anim]][1] += lastMouse[1]-pg.mouse.get_pos()[1];
            lastMouse = pg.mouse.get_pos();
        if pg.mouse.get_pressed()[1]:
            cam.x += lastMouse[0]-pg.mouse.get_pos()[0];
            cam.y += lastMouse[1]-pg.mouse.get_pos()[1];
            lastMouse = pg.mouse.get_pos();
        #draw
        sc.ctx.clear();
        sc.screen_fbo.use();
        sc.ctx.clear(color=(0,0,0.5));
        sc.render.draw(char,anims[ghost],0,-cam-poses[anims[ghost]]);
        sc.render.s_rect(glm.vec2(0,0),glm.vec2(1280,720),glm.vec4(0,0,0.5,0.5));
        sc.render.draw(char,anims[anim],int(glm.floor(frame)),-cam-poses[anims[anim]]);
        sc.render.s_rect(-cam,glm.vec2(100,1),glm.vec4(1,0,0,1));
        sc.render.s_rect(-cam,glm.vec2(1,100),glm.vec4(0,1,0,1));
        #draw screen
        sc.ctx.screen.use();
        sc.ctx.clear();
        sc.ctx.clear(color=(0,0,0.5));
        sc.render.draw_screen(sc.texture);

        pg.display.set_caption("PyFunkin | FPS:"+str(int(glm.floor(sc.clock.get_fps()))));
        pg.display.flip();
        sc.deltatime = sc.clock.tick(60) * 0.001;