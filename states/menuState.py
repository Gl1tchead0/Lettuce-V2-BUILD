import glm;
import pygame as pg;
import json;
import glob;
import random as ran;
import main;
from engine import screen as sc;
from engine import sprites as spr;
from engine import assets as ass;
from engine import assets as tex;
from engine import musicPlayer as mp;
import importlib as il;

class State:
    def __init__(self):
        self.menu = 0;
        self.long = 2;
        self.select = 0;
        self.tecla = "";
        self.songs = [];
        folders = glob.glob('assets/songs/*/');
        for folder in folders:
            self.songs.append(folder[13:-1]);
    def load(self):
        #cargar los assets
        fondo2load = [];
        sprites2load = [];
        
        fondo2load.append(("logo",'assets/images/PyFunk.png'));

        return fondo2load, sprites2load;

    def update(self,keypress):
        if keypress == sc.config["keys"]["upA"] or keypress == sc.config["keys"]["upB"]:
            self.select = (self.select-1)%self.long;
        if keypress == sc.config["keys"]["downA"] or keypress == sc.config["keys"]["downB"]:
            self.select = (self.select+1)%self.long;
            
        if keypress == sc.config["keys"]["back"]:
            if self.menu == 1:#freeplay
                self.menu = 0;
                self.long = 2;
            elif self.menu == 2:#opciones
                self.menu = 0;
                self.long = 2;
                sc.save_data();
            elif self.menu == 3:
                self.menu = 2;
                self.long = 4;
            self.select = 0;
        elif keypress == sc.config["keys"]["accept"]:
            if self.menu == 0:#menu
                if self.select == 0:
                    self.menu = 1;
                    self.long = len(self.songs)+1;
                    self.select = 0;
                elif self.select == 1:
                    self.menu = 2;
                    self.long = 4;
                    self.select = 0;
            elif self.menu == 1:#freeplay
                if self.select == len(self.songs):
                    self.menu = 0;
                    self.long = 2;
                    self.select = 0;
                else:
                    sc.song = self.songs[self.select];
                    main.loadState("playState");
            elif self.menu == 2:#opciones
                if self.select == 0:
                    self.menu = 3;
                    self.long = 11;
                    self.select = 0;
                elif self.select == 1:
                    sc.config["botplay"] = not sc.config["botplay"];
                elif self.select == 2:
                    sc.config["downscroll"] = not sc.config["downscroll"];
                elif self.select == 3:
                    self.menu = 0;
                    self.long = 2;
                    self.select = 0;
                    sc.save_data();
            elif self.menu == 3:#custom controls
                if self.select == 0:
                    self.menu = 4;
                    self.tecla = "leftA";
                elif self.select == 1:
                    self.menu = 4;
                    self.tecla = "downA";
                elif self.select == 2:
                    self.menu = 4;
                    self.tecla = "upA";
                elif self.select == 3:
                    self.menu = 4;
                    self.tecla = "rightA";
                elif self.select == 4:
                    self.menu = 4;
                    self.tecla = "leftB";
                elif self.select == 5:
                    self.menu = 4;
                    self.tecla = "downB";
                elif self.select == 6:
                    self.menu = 4;
                    self.tecla = "upB";
                elif self.select == 7:
                    self.menu = 4;
                    self.tecla = "rightB";
                elif self.select == 8:
                    self.menu = 4;
                    self.tecla = "back";
                elif self.select == 9:
                    self.menu = 4;
                    self.tecla = "accept";
                elif self.select == 10:
                    self.menu = 2;
                    self.long = 4;
                    self.select = 0;
        elif self.menu == 4:#configurar tecla
            if keypress != None:
                sc.config["keys"][self.tecla] = keypress;
                self.menu = 3;
                self.long = 11;
            
    def draw(self):
        if self.menu == 0:#menu
            menu_text = "Menu:";
            opciones = [
                "freeplay",
                "opciones"
            ];
        elif self.menu == 1:#freeplay
            menu_text = "Freeplay:";
            opciones = None;
            opciones = list(self.songs);
            opciones.append("back");
        elif self.menu == 2:#opciones
            menu_text = "Opciones:";
            opciones = [
                "controles",
                "botplay : "+str(sc.config["botplay"]),
                "downscroll : "+str(sc.config["downscroll"]),
                "back"
            ];
        elif self.menu == 3:#custom controls
            menu_text = "Custom Controls:";
            opciones = [
                "A left = "+pg.key.name(sc.config["keys"]["leftA"]),
                "A down = "+pg.key.name(sc.config["keys"]["downA"]),
                "A up = "+pg.key.name(sc.config["keys"]["upA"]),
                "A right = "+pg.key.name(sc.config["keys"]["rightA"]),
                "B left = "+pg.key.name(sc.config["keys"]["leftB"]),
                "B down = "+pg.key.name(sc.config["keys"]["downB"]),
                "B up = "+pg.key.name(sc.config["keys"]["upB"]),
                "B right = "+pg.key.name(sc.config["keys"]["rightB"]),
                "back = "+pg.key.name(sc.config["keys"]["back"]),
                "accept = "+pg.key.name(sc.config["keys"]["accept"]),
                "back"
            ];
        
        sc.render.s_rect(glm.vec2(0),glm.vec2(1280,720),glm.vec4(0,0,0,0.5));
        
        if self.menu == 4:
            sc.render.draw_cam_text(None,"(Press the key you want to set)",glm.vec2(64,352),glm.vec3(0.7,0.7,0.7),10,16,aling="left");
        else:
            for i in range(len(opciones)):
                pos = 352+16*(i-self.select);
                tono = max(0,min(1-abs((pos-352)*0.01),1));
                if i == self.select:
                    sc.render.draw_cam_text(None,opciones[i],glm.vec2(75,pos),glm.vec3(tono,tono,tono),10,16,aling="left");
                else:
                    sc.render.draw_cam_text(None,opciones[i],glm.vec2(64,pos),glm.vec3(tono,tono,tono),10,16,aling="left");
            sc.render.draw_cam_text(None,menu_text,glm.vec2(64,232),glm.vec3(0.7,0.7,0.7),10,16,aling="left");
        
        sc.render.draw_background("logo",glm.vec2(700,32));