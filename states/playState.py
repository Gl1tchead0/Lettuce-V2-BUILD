import glm;
import pygame as pg;
import json;
from engine import screen as sc;
from engine import sprites as spr;
from engine import assets as ass;
from engine import assets as tex;
from engine import musicPlayer as mp;

class State:
    def __init__(self):
        self.song = sc.song;
        self.songPos = 0;
        self.cam = glm.vec2(0,0);
        self.mp = mp.musicPlayer(sc.song);
        self.score = 0;
        self.acurasi = 0;
        self.acuCoun = 0;
        self.misses = 0;
        self.lastBeat = 0;
        self.curBeat = 0;
        self.lastStep = 0;
        self.curStep = 0;
        self.notePoses = []
        for i in range(4):
            self.notePoses.append(glm.vec2(50+120*i,30));
        for i in range(4):
            self.notePoses.append(glm.vec2(750+120*i,30));
        self.noteVector = glm.vec2(0,0);
    def load(self):
        #cargar chart
        self.chart = [];
        with open('assets/songs/'+sc.song+"/chart.json",'r') as file:
            chart = json.load(file);
        for sect in chart["song"]["notes"]:
            if sect["mustHitSection"]:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,(note[1]+4)%8,note[2],True]);
            else:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,note[1],note[2],True]);
        self.bpm = chart["song"]["bpm"]*0.01666666666666666666666666666667;
        #cargar los assets
        fondo2load = [];
        sprites2load = [];

        with open('assets/characters/'+chart["song"]["player1"]+".json",'r') as file:
            bfJs = json.load(file);
        self.bf = glm.vec2(bfJs["position"][0],bfJs["position"][1]);
        sprites2load.append(("bf" ,'assets/images/'+bfJs["image"]));
        
        #cargar al dad
        with open('assets/characters/'+chart["song"]["player2"]+".json",'r') as file:
            dadJs = json.load(file);
        self.dadP = glm.vec2(dadJs["position"][0],dadJs["position"][1]);
        self.dadS = dadJs["scale"];
        self.dadD = {};
        self.dadA = "idle";
        self.dadF = 0;
        self.dadPosing = 0;
        for anim in dadJs["animations"]:
            self.dadD[anim["anim"]] = (anim["name"],glm.vec2(anim["offsets"][0],anim["offsets"][1]));
        sprites2load.append(("dad",'assets/images/'+dadJs["image"]));
        
        sprites2load.append(("notes",'assets/images/NOTE_assets'));

        return fondo2load, sprites2load;

    def update(self,p_L,p_R,p_U,p_D,p_acept,p_back):
        self.songPos += sc.deltatime;
        semiSongPos = self.mp.stream_a.tell() / self.mp.stream_a.samplerate;
        if self.songPos < semiSongPos-0.2 or self.songPos > semiSongPos+0.2:
            self.songPos = semiSongPos;
        
        if p_acept:
            self.mp.paused = False;
            self.songPos = 0;
        #weas del beat
        self.curBeat = glm.floor(self.songPos/self.bpm);
        if self.curBeat != self.lastBeat:
            pass;
        self.lastBeat = self.curBeat;
        
        self.curStep = glm.floor((self.songPos/self.bpm)*10);
        if self.curStep != self.lastStep:
            if self.curStep%4 == 0 and self.dadPosing == 0:
                self.dadA = "idle";
                self.dadF = 0;
        self.lastStep = self.curStep;
        #controles del jugador
        inputs = [p_L,p_D,p_U,p_R];
        for note in self.chart:
            if note[3]:
                notePos = (note[0]-self.songPos)*5;
                if notePos < -1:
                    note[3] = False;
                    self.acurasi += 0;
                    self.acuCoun += 1;
                    self.misses += 1;
                elif note[1] > 3:
                    notePos = abs(notePos);
                    if inputs[note[1]-4] and notePos < 1:
                        note[3] = False;
                        inputs[note[1]-4] = False;
                        self.score += glm.floor(350*notePos);
                        self.acurasi += 1-notePos;
                        self.acuCoun += 1;
                        if notePos > 0.8:
                            print("You Suck!");
                        elif notePos > 0.6:
                            print("Shit");
                        elif notePos > 0.5:
                            print("Bad");
                        elif notePos > 0.4:
                            print("Bruh");
                        elif notePos > 0.31:
                            print("Meh");
                        elif notePos > 0.3:
                            print("Nice");
                        elif notePos > 0.2:
                            print("Good");
                        elif notePos > 0.1:
                            print("Great");
                        elif notePos > 0:
                            print("Sick!");
                        else:
                            print("Perfect!!");
                else:
                    if notePos < 0:
                        note[3] = False;
                        self.dadPosing = 0.6;
                        self.dadF = 0;
                        if note[1] == 0:
                            self.dadA = "singLEFT";
                        elif note[1] == 1:
                            self.dadA = "singDOWN";
                        elif note[1] == 2:
                            self.dadA = "singUP";
                        elif note[1] == 3:
                            self.dadA = "singRIGHT";
            
    def draw(self):
        #fondo mierdas
        
        #personajes mierdas
        self.dadPosing = max(self.dadPosing-sc.deltatime,0);
        self.dadF = min(self.dadF+sc.deltatime*24,len(tex.sprites["dad"].anims[self.dadD[self.dadA][0]])-1);
        sc.render.draw_scale("dad",self.dadD[self.dadA][0],int(glm.floor(self.dadF)),self.dadP,glm.vec2(self.dadS),suboffset=self.dadD[self.dadA][1])
        #hud mierdas
        finalAcur = 100;
        if self.acuCoun > 0:
            finalAcur = (self.acurasi/self.acuCoun)*100;
        sc.render.draw_text(None,"Score:"+str(int(self.score))+" - Misses:"+str(int(self.misses))+" - Accuracy:"+f"{finalAcur:.2f}%",glm.vec2(640,0),glm.vec3(0.7,0.7,0.7),10,16,aling="center");
        
        notesNames = ["arrowLEFT","arrowDOWN","arrowUP","arrowRIGHT","arrowLEFT","arrowDOWN","arrowUP","arrowRIGHT"];
        for i in range(len(self.notePoses)):
            sc.render.draw_scale("notes",notesNames[i],0,self.notePoses[i],glm.vec2(0.8,0.8));
        notesNames = ["purple","blue","green","red","purple","blue","green","red"];
        for note in self.chart:
            notePos = note[0]-self.songPos;
            if note[3]:
                sc.render.draw_scale("notes",notesNames[note[1]],0,self.notePoses[note[1]]+glm.vec2(0,notePos*1000),glm.vec2(0.8,0.8));
