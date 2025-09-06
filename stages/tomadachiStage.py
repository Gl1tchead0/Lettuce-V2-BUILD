import random
import glm;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(200,480);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
        self.lookBF = True;
        self.cmo = glm.vec2(0);

        self.miisF = 0;
        self.tipicoF = 0;
        self.cosmoF = 0;
        self.juanF = 0;

        self.maruF = 0;
        self.maruDir = True;

        self.left_choices  = ["fabi","facu","bronto","bit","wilson","tipico"]
        self.right_choices = ["cosmos","ski","nare","yoyo","qbo","snom"]

        self.left_selected  = random.sample(self.left_choices, 3)
        self.right_selected = random.sample(self.right_choices, 3)
        
        self.rotSt = 0;
    def load(self):
        fondo2load = [];
        sprites2load = [("mii", "assets/images/tomachiFondo/miis")];
        sounds2load = [];

        fondo2load.append(("piso" ,'assets/images/tomachiFondo/pisoPisoRap.png'));
        fondo2load.append(("arbustos" ,'assets/images/tomachiFondo/pisoRap.png'));
        fondo2load.append(("fuente" ,'assets/images/tomachiFondo/fuente_y_cartel.png'));
        
        return fondo2load,sprites2load,sounds2load, [];
    def update(self):
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
        self.cmf = max(self.cmf-sc.deltatime*3,0);
        self.miisF = min(self.miisF+sc.deltatime*24,14);
        self.tipicoF = (self.tipicoF + sc.deltatime*24) % 30;
        self.juanF = (self.juanF + sc.deltatime*24) % 4;
        self.cosmoF = (self.cosmoF + sc.deltatime*24) % 50;

        sc.render.camP.xy = self.cmp + self.cmr * glm.cos(self.cmf) + self.cmo;
        sc.render.camP.z = -360*1.4;
    
        if sc.state.curBeat != sc.state.lastBeat:
            if sc.state.curBeat % 1 == 0:
                self.miisF = 0;
                self.maruDir = not self.maruDir;
            if sc.state.curBeat % 2 == 0:
                self.maruF = 0;
    
        self.maruF += sc.deltatime*24;
        maruMax = 14 + 14*self.maruDir;
        if self.maruF >= maruMax: self.maruF = maruMax;
    
    def draw(self):
        sc.ctx.clear(color=(1,1,1));
        sc.render.shaind = "blend";
        sc.render.shaders["blend"].program["color"].write(glm.vec4(1,1,1,0.2))
        sc.render.draw_scale("mii", "juane", int(self.juanF), glm.vec2(-780+sc.render.camP.x*0.4, 100), glm.vec2(0.6))

        sc.render.shaind = "tomachiPiso";
        sc.render.shaders["tomachiPiso"].program["scroll"].value = sc.render.camP.x*0.0002;
        sc.render.draw_background("piso",glm.vec3(-1700,550,0));
        sc.render.shaind = "sprite";
        sc.render.draw_background("arbustos",glm.vec3(-900+sc.render.camP.x*0.5, 350,0));
        sc.render.draw_back_scale("fuente",glm.vec3((-450+sc.render.camP.x*0.25, 0),0), glm.vec2(0.6));

        sc.render.draw_scale("mii", "maru", int(self.maruF), glm.vec2(50+sc.render.camP.x*0.25, 240), glm.vec2(0.9));

        positions_left = [
            glm.vec2(-500+sc.render.camP.x*0.15, 150),
            glm.vec2(-700+sc.render.camP.x*0.12, 100),
            glm.vec2(-900+sc.render.camP.x*0.1, 150),
            glm.vec2(-600+sc.render.camP.x*0.1, 350),
            glm.vec2(-1000+sc.render.camP.x*0.1, 330),
            glm.vec2(-750, 330)
        ];
        positions_right = [
            glm.vec2(700+sc.render.camP.x*0.4, 100),
            glm.vec2(600+sc.render.camP.x*0.25, 300),
            glm.vec2(400+sc.render.camP.x*0.15, 150),
            glm.vec2(850+sc.render.camP.x*0.12, 200),
            glm.vec2(700+sc.render.camP.x*0.1, 350),
            glm.vec2(1400, 500)
        ];

        for k, name in enumerate(self.right_choices):
            if name in self.right_selected:
                if name != "cosmos":
                    sc.render.draw("mii", name, int(self.miisF), positions_right[k]);
                else: 
                    sc.render.draw_scale("mii", "cosmos", int(self.cosmoF), positions_right[k], glm.vec2(0.8));

        for k, name in enumerate(self.left_choices):
            if name in self.left_selected:
                if name != "tipico":
                    sc.render.draw("mii", name, int(self.miisF), positions_left[k]);
                else: 
                    sc.render.draw("mii", "tipico", int(self.tipicoF), positions_left[k]);
    
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