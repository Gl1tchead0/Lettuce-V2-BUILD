import glm;
from engine import screen as sc;

class Stage:
    def __init__(self):
        self.cmp = glm.vec2(0);
        self.cmr = glm.vec2(0);
        self.cmf = 0;
    def load(self):
        pass;
    def update(self):
        #weas de la camara
        self.cmf = max(self.cmf-sc.deltatime*5,0)
        sc.state.camGame.xy = self.cmp + self.cmr * glm.cos(self.cmf);
        sc.state.camGame.w = 0.6;
    def draw(self):
        pass;
    def onEvent(self,type,val1,val2):
        if type == "Camera look at pos":
            self.cmp = (glm.vec2(val1,val2)+sc.state.camGame.xy)*0.5;
            self.cmr = glm.vec2(val1,val2)-self.cmp;
            self.cmf = 3.1415926535897932384626433832795;
    def modChart(self,notePos):
        return glm.vec2(0,notePos);