import glm;
import pygame as pg;
import moderngl as mgl;
from engine import assets as ass;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(640,360);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
        self.lookBF = True;
        self.cmo = glm.vec2(0);
        
        self.rotSt = 0;
    def load(self):
        fondo2load = [];
        sprites2load = [];
        sounds2load = [];
        models2load = [];

        fondo2load.append(("piso" ,'assets/images/tomachiFondo/pisoPisoRap.png'));
        fondo2load.append(("arbustos" ,'assets/images/tomachiFondo/pisoRap.png'));
        fondo2load.append(("fuente" ,'assets/images/tomachiFondo/fuente_y_cartel.png'));
        fondo2load.append(("steve" ,'assets/images/steve.png'));

        models2load.append(("steve","assets/models/steve"));
        
        return fondo2load,sprites2load,sounds2load,models2load;
    def update(self):
        ass.textures["steve"].filter = (mgl.NEAREST, mgl.NEAREST);
        self.rotSt += sc.deltatime;
        #weas de la camara
        if self.lookBF:
            if sc.state.bfA == "idle":
                self.cmo += (glm.vec2(0,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.bfA == "singLEFT":
                self.cmo += (glm.vec2(-30,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.bfA == "singRIGHT":
                self.cmo += (glm.vec2(30,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.bfA == "singUP":
                self.cmo += (glm.vec2(0,-30)-self.cmo)*(5*sc.deltatime);
            elif sc.state.bfA == "singDOWN":
                self.cmo += (glm.vec2(0,30)-self.cmo)*(5*sc.deltatime);
        else:
            if sc.state.dadA == "idle":
                self.cmo += (glm.vec2(0,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.dadA == "singLEFT":
                self.cmo += (glm.vec2(-30,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.dadA == "singRIGHT":
                self.cmo += (glm.vec2(30,0)-self.cmo)*(5*sc.deltatime);
            elif sc.state.dadA == "singUP":
                self.cmo += (glm.vec2(0,-30)-self.cmo)*(5*sc.deltatime);
            elif sc.state.dadA == "singDOWN":
                self.cmo += (glm.vec2(0,30)-self.cmo)*(5*sc.deltatime);
        sc.render.camR.z = -self.cmo.x*0.001;
        self.cmf = max(self.cmf-sc.deltatime*3,0)
        sc.render.camP.xy = self.cmp + self.cmr * glm.cos(self.cmf) + self.cmo;
        sc.render.camP.z = -360*1.4;
        #sc.render.camP.w = 0.6;
    def draw(self):
        sc.ctx.clear(color=(1,1,1));
        sc.render.draw_background("piso",glm.vec2(-600,500));
        #for i in range(20):
        #    model = glm.translate(glm.mat4x4(),glm.vec3(i*100,500,0));
        #    model = glm.rotate(model,glm.radians(180),glm.vec3(1,0,0));
        #    model = glm.rotate(model,(self.rotSt+i)*i,glm.vec3(1,1,1));
        #    model = glm.scale(model,glm.vec3(300,300,300))
        #    sc.render.draw_model("steve","steve",model);
    def onEvent(self,type,val1,val2):
        if type == "Change look":
            self.lookBF = val1;
        if type == "Camera look at pos":
            self.cmp = (glm.vec2(val1,val2)+sc.render.camP.xy)*0.5;
            self.cmr = glm.vec2(val1,val2)-self.cmp;
            self.cmf = 3.1415926535897932384626433832795;
    def modChart(self,notePos):
        if sc.config["downscroll"]:
            return glm.vec2(0,-notePos);
        else:
            return glm.vec2(0,notePos);