import glm;
from engine import assets as tex;
import xml.etree.ElementTree as ET;

class Image:
    def __init__(self, xy, wh, imsz, offset=glm.vec2(0,0)):
        self.xy = xy / imsz;
        self.rwh = wh;
        self.wh = wh / imsz;
        self.offset = offset;

class Sprite:
    def __init__(self, dir,size):
        antanim = "_";
        self.imgz = size;#tex.textures[nombre].size;
        
        self.anims = {};
        anim = [];
        
        file = ET.parse(dir);
        root = file.getroot();
        for frame in root:
            if frame.attrib["name"][:-4] != antanim and antanim != "_":
                self.anims[antanim] = anim;
                anim = [];
            anim.append(Image(glm.vec2(int(frame.attrib["x"]),int(frame.attrib["y"])), 
                              glm.vec2(int(frame.attrib["width"]),int(frame.attrib["height"])), 
                              glm.vec2(self.imgz[0],self.imgz[1]),
                              glm.vec2(int(frame.attrib.get("frameX",0)),int(frame.attrib.get("frameY",0)))));
            antanim = frame.attrib["name"][:-4];
        self.anims[antanim] = anim;