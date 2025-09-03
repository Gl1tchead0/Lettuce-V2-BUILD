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
        pass;
    def load(self):
        #cargar los assets
        fondo2load = [];
        sprites2load = [];
        sounds2load = [];
        models2load = [];

        sc.mp.change_audio_a("assets/songs/gameOver.ogg");
        sc.mp.change_audio_b("assets/songs/gameOver.ogg");
        sc.mp.paused = False;

        return fondo2load, sprites2load, sounds2load,models2load;

    def update(self,keypress):
        if keypress == sc.config["keys"]["back"]:
            main.loadState("menuState");
            return True;
        elif keypress == sc.config["keys"]["accept"]:
            main.loadState("playState");
            return True;
        sc.mp.VOLUME_A = sc.trueVol;
        sc.mp.VOLUME_B = 0;
            
    def draw(self):
        pass;

    def drawHUD(self):
        sc.ctx.clear(0,0,0,1);
        sc.render.draw_text(None,"Game Over",glm.vec2(640,360),glm.vec3(1,0,0),10,16,aling="center");