import glm;
import numpy as np;
import glob;
import os;
import pygame as pg;
from engine import assets as tex;
from engine import screen as sc;

class Renderer:
    def __init__(self):
        #vertices
        vertexs = [(0,0),(1,0),(1,1),(0,1)];
        indices = [(0,2,3),(0,1,2)];
        vertex_data = self.get_data(vertices=vertexs,indices=indices);
        simvbo = sc.ctx.buffer(vertex_data);
        vbo = sc.ctx.buffer(np.hstack([vertex_data,vertex_data]));
        
        self.shaders = {};
        self.shaind = "sprite";
        files = glob.glob('assets/shaders/*.frag');
        for file in files:
            program = None;
            dir = file[15:-5];
            if os.path.exists(f'assets/shaders/{dir}.vert'):
                vert = open(f'assets/shaders/{dir}.vert').read()
                frag = open(f'assets/shaders/{dir}.frag').read()
                program = sc.ctx.program(vertex_shader=vert, fragment_shader=frag);
                if dir != "solidcol":
                    program['u_texture_0'] = 0;
                if dir != "screen":
                    program["proj"].write(sc.proj);
            else:
                vert = open(f'assets/shaders/sprite.vert').read()
                frag = open(f'assets/shaders/{dir}.frag').read()
                program = sc.ctx.program(vertex_shader=vert, fragment_shader=frag);
                program['u_texture_0'] = 0;
                program["proj"].write(sc.proj);
            
            if dir == "solidcol":
                self.shaders[dir] = sc.ctx.vertex_array(program,[(simvbo, '2f', 'in_position')]);
            else:
                self.shaders[dir] = sc.ctx.vertex_array(program,[(vbo, '2f 2f', 'in_textcoord_0', 'in_position')]);
    
    @staticmethod
    def get_data(vertices,indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array (data, dtype='f4');
    
    def ajust_screen(self):
        model = None;
        n_wid = sc.real_res[1] * 1.7777777777777777777777777777778;
        n_hei = sc.real_res[0] * 0.5625;
        if n_hei < sc.real_res[1]:
            model = glm.translate(glm.mat4(),glm.vec3(-1,-1+(sc.real_res[1]-n_hei)/sc.real_res[1],0));
            model = glm.scale(model,glm.vec3(1,n_hei/sc.real_res[1],1));
            model = glm.scale(model,glm.vec3(2,2,1));
            sc.real_mouse.x = (pg.mouse.get_pos()[0]/sc.real_res[0])*1280;
            sc.real_mouse.y = ((pg.mouse.get_pos()[1]-(sc.real_res[1]-n_hei)*0.5)/n_hei)*720;
            sc.real_mouse.y = max(0,min(720,sc.real_mouse.y));
        else:
            model = glm.translate(glm.mat4(),glm.vec3(-1+(sc.real_res[0]-n_wid)/sc.real_res[0],-1,0));
            model = glm.scale(model,glm.vec3(n_wid/sc.real_res[0],1,1));
            model = glm.scale(model,glm.vec3(2,2,1));
            sc.real_mouse.x = ((pg.mouse.get_pos()[0]-(sc.real_res[0]-n_wid)*0.5)/n_wid)*1280;
            sc.real_mouse.y = (pg.mouse.get_pos()[1]/sc.real_res[1])*720;
            sc.real_mouse.x = max(0,min(1280,sc.real_mouse.x));
        self.shaders["screen"].program["trans"].write(model);
    
    def draw_screen(self, tex):
        tex.use(0);
        self.shaders["screen"].render();
            
    def draw_text(self, font, text, position, color, sep,scale=32,aling="left"):
        if aling == "center":
            position.x -= (len(text)*sep-sep+scale)*0.5;
        if aling == "right":
            position.x -= len(text)*sep-sep+scale;
            
        if font == None:
            sc.vcrTex.use(0);
            texto = list(text);
            for i in range(len(texto)):
                anima = texto[i];
                if anima != " ":
                    pos = glm.vec2(position.x+i*sep,position.y);
                    model = glm.translate(glm.mat4(),glm.vec3(pos-sc.vcrSpr.anims[anima][0].offset,0));
                    model = glm.scale(model,glm.vec3(scale,scale,1));
                    self.shaders["font"].program["trans"].write(model);
                    self.shaders["font"].program["color"].write(color);
                    self.shaders["font"].program["pos"].write(sc.vcrSpr.anims[anima][0].xy);
                    self.shaders["font"].program["size"].write(sc.vcrSpr.anims[anima][0].wh);
                    self.shaders["font"].render();
        else:
            tex.textures[font.tex].use(0);
            texto = list(text);
            for i in range(len(texto)):
                anima = texto[i];
                if anima != " ":
                    pos = glm.vec2(position.x+i*sep,position.y);
                    model = glm.translate(glm.mat4(),glm.vec3(pos-font.anims[anima][0].offset,0));
                    model = glm.scale(model,glm.vec3(glm.abs(font.anims[anima][0].rwh.x)*scale,glm.abs(font.anims[anima][0].rwh.y)*scale,1));
                    self.shaders["font"].program["trans"].write(model);
                    self.shaders["font"].program["color"].write(color);
                    self.shaders["font"].program["pos"].write(font.anims[anima][0].xy);
                    self.shaders["font"].program["size"].write(font.anims[anima][0].wh);
                    self.shaders["font"].render();
    
    def draw_background(self, fondo,position):
        tex.textures[fondo].use(0);
        
        model = glm.translate(glm.mat4(),glm.vec3(position,0));
        model = glm.scale(model,glm.vec3(tex.textures[fondo].size[0],tex.textures[fondo].size[1],1));
        self.shaders[self.shaind].program["trans"].write(model);
        self.shaders[self.shaind].program["pos"].write(glm.vec2(0,0));
        self.shaders[self.shaind].program["size"].write(glm.vec2(1,1));
        
        self.shaders[self.shaind].render();
    
    def draw(self, sprite, anima,index, position, offset=glm.vec2(0,0),suboffset=glm.vec2(0,0),usecam=True):
        tex.textures[sprite].use(0);
        
        if usecam:
            model = glm.translate(glm.mat4(),glm.vec3(position-tex.sprites[sprite].anims[anima][index].offset-suboffset,0));
        else:
            model = glm.translate(glm.mat4(),glm.vec3(position-tex.sprites[sprite].anims[anima][index].offset-suboffset,0));
        model = glm.scale(model,glm.vec3(glm.abs(tex.sprites[sprite].anims[anima][index].rwh.x),glm.abs(tex.sprites[sprite].anims[anima][index].rwh.y),1));
        model = glm.translate(model,-glm.vec3(offset.x,offset.y,0));
        self.shaders[self.shaind].program["trans"].write(model);
        
        self.shaders[self.shaind].program["pos"].write(tex.sprites[sprite].anims[anima][index].xy);
        self.shaders[self.shaind].program["size"].write(tex.sprites[sprite].anims[anima][index].wh);
        self.shaders[self.shaind].render();
        
    def draw_scale(self, sprite, anima,index, position, scale, offset=glm.vec2(0,0),suboffset=glm.vec2(0,0),usecam=True):
        tex.textures[sprite].use(0);
        
        if usecam:
            model = glm.translate(glm.mat4(),glm.vec3(position-tex.sprites[sprite].anims[anima][index].offset*scale-suboffset,0));
        else:
            model = glm.translate(glm.mat4(),glm.vec3(position-tex.sprites[sprite].anims[anima][index].offset*scale-suboffset,0));
        model = glm.scale(model,glm.vec3(glm.abs(tex.sprites[sprite].anims[anima][index].rwh.x)*scale.x,glm.abs(tex.sprites[sprite].anims[anima][index].rwh.y)*scale.y,1));
        model = glm.translate(model,-glm.vec3(offset.x,offset.y,0));
        self.shaders[self.shaind].program["trans"].write(model);
        
        self.shaders[self.shaind].program["pos"].write(tex.sprites[sprite].anims[anima][index].xy);
        self.shaders[self.shaind].program["size"].write(tex.sprites[sprite].anims[anima][index].wh);
        self.shaders[self.shaind].render();
        
    def draw_transformed(self, sprite, anima, index, position, angle, scale, offset=glm.vec2(0,0), radians=False):
        tex.textures[sprite].use(0);
        
        if not radians: angle = glm.radians(angle);
        ofs = glm.vec2((tex.sprites[sprite].anims[anima][index].offset.x*glm.cos(angle)-tex.sprites[sprite].anims[anima][index].offset.y*glm.sin(angle))*scale.x,
                       (tex.sprites[sprite].anims[anima][index].offset.x*glm.sin(angle)+tex.sprites[sprite].anims[anima][index].offset.y*glm.cos(angle))*scale.y);
        model = glm.translate(glm.mat4(),glm.vec3(position-ofs,0));
        model = glm.rotate(model,angle,glm.vec3(0,0,1));
        model = glm.scale(model,glm.vec3(tex.sprites[sprite].anims[anima][index].rwh.x*scale.x
                                        ,tex.sprites[sprite].anims[anima][index].rwh.y*scale.y,1))
        model = glm.translate(model,-glm.vec3(offset.x,offset.y,0));
        self.shaders[self.shaind].program["trans"].write(model);
        
        self.shaders[self.shaind].program["pos"].write(tex.sprites[sprite].anims[anima][index].xy);
        self.shaders[self.shaind].program["size"].write(tex.sprites[sprite].anims[anima][index].wh);
        self.shaders[self.shaind].render();
        
    def s_rect(self, position, scale, color):#shrek XD
        model = glm.translate(glm.mat4(),glm.vec3(position,0));
        model = glm.scale(model,glm.vec3(scale,1));
        self.shaders["solidcol"].program["trans"].write(model);
        self.shaders["solidcol"].program["col"].write(color);
        
        self.shaders["solidcol"].render();