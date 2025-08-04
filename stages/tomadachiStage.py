import glm;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(0);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
        self.lookBF = True;
        self.cmo = glm.vec2(0);
    def load(self):
        fondo2load = [];
        sprites2load = [];
        fondo2load.append(("piso" ,'assets/images/tomachiFondo/pisoPisoRap.png'));
        fondo2load.append(("arbustos" ,'assets/images/tomachiFondo/pisoRap.png'));
        fondo2load.append(("fuente" ,'assets/images/tomachiFondo/fuente_y_cartel.png'));
        return fondo2load,sprites2load;
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
        sc.state.camGame.z = -self.cmo.x*0.001;
        self.cmf = max(self.cmf-sc.deltatime*3,0)
        sc.state.camGame.xy = self.cmp + self.cmr * glm.cos(self.cmf) + self.cmo;
        sc.state.camGame.w = 0.6;
    def draw(self):
        sc.render.s_rect(glm.vec2(0),glm.vec2(1280,720),glm.vec4(1,1,1,1));
        sc.render.draw_cam_background("piso",glm.vec2(-600,500));
    def onEvent(self,type,val1,val2):
        if type == "Change look":
            self.lookBF = val1;
        if type == "Camera look at pos":
            self.cmp = (glm.vec2(val1,val2)+sc.state.camGame.xy)*0.5;
            self.cmr = glm.vec2(val1,val2)-self.cmp;
            self.cmf = 3.1415926535897932384626433832795;
    def modChart(self,notePos):
        return glm.vec2(0,notePos);