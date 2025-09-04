import glm;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(640,360);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
        self.lookBF = True;
        self.cmo = glm.vec2(0);
        
        self.facuF = 0;
        self.skiF = 0;
        self.tomF = 0;
        self.ruberF = 0;
        self.zeuhF = 0;
        self.ihanF = 0;
        
    def load(self):
        fondo2load = [("juan", "assets/images/tipicos/juan.png")];
        sprites2load = [("ski", "assets/images/tipicos/ski_e"), ("facu", "assets/images/tipicos/facuFNF"),
                        ("tom", "assets/images/tipicos/Tompoops"), ("ruber", "assets/images/tipicos/Ruber"),
                        ("zeu", "assets/images/tipicos/Zeuz"), ("jest", "assets/images/tipicos/fuckyou")];
        sounds2load = [];
        models2load = [];
        
        return fondo2load,sprites2load,sounds2load,models2load;
    def update(self):
        if sc.state.curBeat != sc.state.lastBeat:
            if sc.state.curBeat % 1 == 0:
                self.zeuhF = 0;
                self.skiF = 0;
                self.facuF = 0;
                self.tomF = 0;
                self.ruberF = 0;
        
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

        self.zeuhF = min(self.zeuhF+sc.deltatime*24, 15);
        sc.render.draw("zeu", "Zeuz Idle", int(self.zeuhF), glm.vec2(740, 360));
        self.skiF = min(self.skiF+sc.deltatime*24, 13);
        sc.render.draw("ski", "BF idle dance", int(self.skiF), glm.vec2(1000,400));
        self.facuF = min(self.facuF+sc.deltatime*24, 13);
        sc.render.draw_scale("facu", "facuFNF idle", int(self.facuF), glm.vec2(1300,150), glm.vec2(-1,1));
        self.ruberF = min(self.ruberF+sc.deltatime*24, 29);
        sc.render.draw_scale("ruber", "Ruber_idle", int(self.ruberF), glm.vec2(1300,200), glm.vec2(0.8));
        self.tomF = min(self.tomF+sc.deltatime*24, 13);
        sc.render.draw("tom", "Tom idle", int(self.tomF), glm.vec2(-200,180));
        sc.render.draw_scale("jest", "fuckyou idle", 0, glm.vec2(480,140), glm.vec2(1.2));

        sc.render.shaind = "blend";
        sc.render.shaders["blend"].program["color"].write(glm.vec4(1,1,1,0.2));
        sc.render.draw_background("juan", glm.vec3(1200, 900,0));
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