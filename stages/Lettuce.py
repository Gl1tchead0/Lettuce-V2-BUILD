import glm;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(640,360);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
        self.lookBF = True;
        self.cmo = glm.vec2(0);

        self.shadDadA = {"idle": "PeacockIdle",
                         "singLEFT": "PeacockLeft",
                         "singDOWN": "PeacockDown",
                         "singUP": "PeacockUp",
                         "singRIGHT": "PeacockRight"};
        self.shadBFA = {"idle": "IDLE",
                         "singLEFT": "LEFT",
                         "singDOWN": "DOWN",
                         "singUP": "UP",
                         "singRIGHT": "RIGHT",
                         "singLEFTmiss": "leftmiss",
                         "singDOWNmiss": "downmiss",
                         "singUPmiss": "upmiss",
                         "singRIGHTmiss": "misright"};
        
    def load(self):
        fondo2load = [("piso", "assets/images/juaneFondo/piso.png")];
        sprites2load = [("bfS", "assets/images/bf reflej"), ("lS", "assets/images/letu reflej")];
        
        return fondo2load, sprites2load, [], [];
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
        self.cmf = max(self.cmf-sc.deltatime*3,0)
        sc.render.camP.xy = self.cmp + self.cmr * glm.cos(self.cmf) + self.cmo;
        sc.render.camP.z = -360*1.6;
    def draw(self):
        sc.ctx.clear(color=(1,1,1));

        sc.render.shaind = "juanePiso";
        sc.render.shaders["juanePiso"].program["scroll"].value = sc.render.camP.x*0.001;
        sc.render.draw_back_scale("piso", glm.vec3(-1300+sc.render.camP.x, 400,0), glm.vec2(8,2));
        #REEMPLAZAR POR PISO 3D

        sc.render.shaind = "sprite";
        sc.render.draw("lS", self.shadDadA[sc.state.dadA], int(sc.state.dadF), glm.vec2(-312,550));
        sc.render.draw("bfS", self.shadBFA[sc.state.bfA], int(sc.state.bfF), glm.vec2(765,700));
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