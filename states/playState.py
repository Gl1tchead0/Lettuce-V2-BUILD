import glm;
import pygame as pg;
import json;
import random as ran;
from engine import screen as sc;
from engine import sprites as spr;
from engine import assets as ass;
from engine import assets as tex;
from engine import musicPlayer as mp;
import importlib as il;

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
        self.camGame = glm.vec4(0,0,0,1);
        self.hudZoom = 1;
        self.pressed = [];
        self.notePoses = []
        for i in range(4):
            self.notePoses.append(glm.vec2(812+120*i,92));
        for i in range(4):
            self.notePoses.append(glm.vec2(112+120*i,92));
        self.noteVector = glm.vec2(0,0);
    def load(self):
        #cargar chart
        self.chart = [];
        self.longChart = [];
        mustHitSection = False;
        with open('assets/songs/'+sc.song+"/chart.json",'r') as file:
            chart = json.load(file);
        with open('assets/characters/'+chart["song"]["player1"]+".json",'r') as file:
            bfJs = json.load(file);
        with open('assets/characters/'+chart["song"]["player2"]+".json",'r') as file:
            dadJs = json.load(file);
        self.events = chart["song"]["events"];
        self.curEven = 0;
        self.bpm = chart["song"]["bpm"];i = 0;
        for sect in chart["song"]["notes"]:
            if sect["mustHitSection"]:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,note[1],True]);
                    if note[2] > 0:
                        self.longChart.append([note[0]*0.001,(note[0]+note[2])*0.001,note[1],1]);
                if mustHitSection != sect["mustHitSection"]:
                    self.events.append([((i*sect["sectionBeats"])/self.bpm)*60,
                                        [["Camera look at pos",bfJs["camera_position"][0],bfJs["camera_position"][1]]]]);
            else:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,(note[1]+4)%8,True]);
                    if note[2] > 0:
                        self.longChart.append([note[0]*0.001,(note[0]+note[2])*0.001,(note[1]+4)%8,1]);
                if mustHitSection != sect["mustHitSection"]:
                    self.events.append([((i*sect["sectionBeats"])/self.bpm)*60,
                                        [["Camera look at pos",dadJs["camera_position"][0],dadJs["camera_position"][1]]]]);
            mustHitSection = sect["mustHitSection"];
            i += 1;
        sorted(self.events,key=lambda x: x[0], reverse=True);
        self.stage = il.import_module("stages."+chart["song"]["stage"]).Stage();

        self.missS = []
        self.missS.append(pg.mixer.Sound("assets/sounds/missnote1.ogg"));
        self.missS.append(pg.mixer.Sound("assets/sounds/missnote2.ogg"));
        self.missS.append(pg.mixer.Sound("assets/sounds/missnote3.ogg"));
        #cargar los assets
        fondo2load = [];
        sprites2load = [];

        self.bfP = glm.vec2(bfJs["position"][0],bfJs["position"][1]);
        self.bfS = bfJs["scale"];
        self.bfD = {};
        self.bfA = "idle";
        self.bfF = 0;
        self.bfPosing = 0;
        for anim in bfJs["animations"]:
            self.bfD[anim["anim"]] = (anim["name"],glm.vec2(anim["offsets"][0],anim["offsets"][1]));
        sprites2load.append(("bf" ,'assets/images/'+bfJs["image"]));
        self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);
        
        #cargar al dad
        self.dadP = glm.vec2(dadJs["position"][0],dadJs["position"][1]);
        self.dadS = dadJs["scale"];
        self.dadD = {};
        self.dadA = "idle";
        self.dadF = 0;
        self.dadPosing = 0;
        for anim in dadJs["animations"]:
            self.dadD[anim["anim"]] = (anim["name"],glm.vec2(anim["offsets"][0],anim["offsets"][1]));
        sprites2load.append(("dad",'assets/images/'+dadJs["image"]));
        self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);
        
        sprites2load.append(("notes",'assets/images/NOTE_assets'));

        return fondo2load, sprites2load;

    def update(self,p_L,p_R,p_U,p_D,p_acept,p_back):
        self.songPos += sc.deltatime;
        semiSongPos = self.mp.stream_a.tell() / self.mp.stream_a.samplerate;
        if self.songPos < semiSongPos-0.2 or self.songPos > semiSongPos+0.2:
            self.songPos = semiSongPos;
        
        if p_acept:
            self.mp.paused = False;
            self.curEven = 0;
            self.songPos = 0;
        #weas del beat
        self.curStep = glm.floor((semiSongPos*self.bpm)*0.01666666666666666666666666666667);
        if self.curStep != self.lastStep:
            pass;
        self.lastStep = self.curStep;

        self.curBeat = glm.floor(self.curStep*0.25);
        if self.curBeat != self.lastBeat:
            if self.curBeat % 2 == 0:
                self.hudZoom = 1.05;
            if self.dadPosing == 0:
                self.dadA = "idle";
                self.dadF = 0;
            if self.bfPosing == 0:
                self.bfA = "idle";
                self.bfF = 0;
        self.lastBeat = self.curBeat;
        #controles del jugador
        for i in range(0,len(self.pressed)):
            if self.pressed[i] >= 0:
                self.pressed[i] = max(self.pressed[i]-sc.deltatime*12,0);
            else:
                self.pressed[i] = min(self.pressed[i]+sc.deltatime*12,0);

        inputs = [p_L,p_D,p_U,p_R];
        inputsP = [pg.key.get_pressed()[pg.K_d] or pg.key.get_pressed()[pg.K_LEFT],
                   pg.key.get_pressed()[pg.K_f] or pg.key.get_pressed()[pg.K_DOWN],
                   pg.key.get_pressed()[pg.K_j] or pg.key.get_pressed()[pg.K_UP],
                   pg.key.get_pressed()[pg.K_k] or pg.key.get_pressed()[pg.K_RIGHT],];
        for i in range(0,len(inputsP)):
            if inputsP[i] and self.pressed[i] >= 0:
                self.pressed[i] = 1;

        #notas largas
        for note in self.longChart:
            if note[3]:
                notePos = (note[0]-self.songPos)*10;
                if notePos < -1 and note[3] == 1:
                    note[3] = 0;
                elif note[2] < 4:
                    if sc.botplay:
                        if notePos <= 0:
                            note[3] = 2;
                            self.pressed[note[2]] = -1;
                            self.bfPosing = 0.25;
                            self.bfF = 0;
                            if note[2]-4 == 0:
                                self.bfA = "singLEFT";
                            elif note[2]-4 == 1:
                                self.bfA = "singDOWN";
                            elif note[2]-4 == 2:
                                self.bfA = "singUP";
                            elif note[2]-4 == 3:
                                self.bfA = "singRIGHT";
                        if (note[1]-self.songPos)*10 <= 0:
                            note[3] = 0;
                    else:
                        notePos = abs(notePos);
                        if inputsP[note[2]] and notePos < 1:
                            note[3] = 2;
                        if note[3] == 2:
                            if not inputsP[note[2]]:
                                note[3] = 0;
                                if (note[1]-self.songPos)*10 > 0:
                                    self.missS[ran.randint(0,2)].play();
                                    self.acurasi += 0;
                                    self.acuCoun += 1;
                                    self.misses += 1;
                                    self.bfPosing = 0.25;
                                    self.bfF = 0;
                                    if note[2] == 0:
                                        self.bfA = "singLEFTmiss";
                                    elif note[2] == 1:
                                        self.bfA = "singDOWNmiss";
                                    elif note[2] == 2:
                                        self.bfA = "singUPmiss";
                                    elif note[2] == 3:
                                        self.bfA = "singRIGHTmiss";
                            self.pressed[note[2]] = -1;
                            self.bfPosing = 0.25;
                            self.bfF = 0;
                            if note[2] == 0:
                                self.bfA = "singLEFT";
                            elif note[2] == 1:
                                self.bfA = "singDOWN";
                            elif note[2] == 2:
                                self.bfA = "singUP";
                            elif note[2] == 3:
                                self.bfA = "singRIGHT";
                else:
                    if notePos <= 0:
                        note[3] = 2;
                        self.pressed[note[2]] = -1;
                        self.dadPosing = 0.25;
                        self.dadF = 0;
                        if note[2]-4 == 0:
                            self.dadA = "singLEFT";
                        elif note[2]-4 == 1:
                            self.dadA = "singDOWN";
                        elif note[2]-4 == 2:
                            self.dadA = "singUP";
                        elif note[2]-4 == 3:
                            self.dadA = "singRIGHT";
                    if (note[1]-self.songPos)*10 <= 0:
                        note[3] = 0;
        #notas simples
        for note in self.chart:
            if note[2]:
                notePos = (note[0]-self.songPos)*10;
                if notePos < -1:
                    note[2] = False;
                    self.missS[ran.randint(0,2)].play();
                    self.acurasi += 0;
                    self.acuCoun += 1;
                    self.misses += 1;
                    self.bfPosing = 0.25;
                    self.bfF = 0;
                    if note[1] == 0:
                        self.bfA = "singLEFTmiss";
                    elif note[1] == 1:
                        self.bfA = "singDOWNmiss";
                    elif note[1] == 2:
                        self.bfA = "singUPmiss";
                    elif note[1] == 3:
                        self.bfA = "singRIGHTmiss";
                elif note[1] < 4:
                    if sc.botplay:
                        if notePos < 0:
                            note[2] = False;
                            self.pressed[note[1]] = -1;
                            self.bfPosing = 0.25;
                            self.bfF = 0;
                            if note[1] == 0:
                                self.bfA = "singLEFT";
                            elif note[1] == 1:
                                self.bfA = "singDOWN";
                            elif note[1] == 2:
                                self.bfA = "singUP";
                            elif note[1] == 3:
                                self.bfA = "singRIGHT";
                    else:
                        notePos = abs(notePos);
                        if inputs[note[1]] and notePos < 1:
                            note[2] = False;
                            self.pressed[note[1]] = -1;
                            inputs[note[1]] = False;
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
                            self.bfPosing = 0.25;
                            self.bfF = 0;
                            if note[1] == 0:
                                self.bfA = "singLEFT";
                            elif note[1] == 1:
                                self.bfA = "singDOWN";
                            elif note[1] == 2:
                                self.bfA = "singUP";
                            elif note[1] == 3:
                                self.bfA = "singRIGHT";
                else:
                    if notePos < 0:
                        note[2] = False;
                        self.pressed[note[1]] = -1;
                        self.dadPosing = 0.25;
                        self.dadF = 0;
                        if note[1]-4 == 0:
                            self.dadA = "singLEFT";
                        elif note[1]-4 == 1:
                            self.dadA = "singDOWN";
                        elif note[1]-4 == 2:
                            self.dadA = "singUP";
                        elif note[1]-4 == 3:
                            self.dadA = "singRIGHT";
        #eventos we
        if self.curEven < len(self.events):
            if self.events[self.curEven][0] < self.songPos:
                for even in self.events[self.curEven][1]:
                    self.stage.onEvent(even[0],even[1],even[2]);
                self.curEven += 1;
        #zooms del hud
        self.hudZoom += (1-self.hudZoom)*(0.05*(sc.deltatime*60));
        self.stage.update();
            
    def draw(self):
        #fondo mierdas
        sc.render.cam = self.camGame;
        self.stage.draw();
        #personajes mierdas
        self.bfPosing = max(self.bfPosing-sc.deltatime,0);
        self.bfF = min(self.bfF+sc.deltatime*24,len(tex.sprites["bf"].anims[self.bfD[self.bfA][0]])-1);
        sc.render.draw_cam_scale("bf",self.bfD[self.bfA][0],int(glm.floor(self.bfF)),self.bfP,glm.vec2(self.bfS),suboffset=self.bfD[self.bfA][1])

        self.dadPosing = max(self.dadPosing-sc.deltatime,0);
        self.dadF = min(self.dadF+sc.deltatime*24,len(tex.sprites["dad"].anims[self.dadD[self.dadA][0]])-1);
        sc.render.draw_cam_scale("dad",self.dadD[self.dadA][0],int(glm.floor(self.dadF)),self.dadP,glm.vec2(self.dadS),suboffset=self.dadD[self.dadA][1])
        #hud mierdas
        sc.render.cam = glm.vec4(0,0,0,self.hudZoom);
        finalAcur = 100;
        if self.acuCoun > 0:
            finalAcur = (self.acurasi/self.acuCoun)*100;
        sc.render.draw_cam_text(None,"Score:"+str(int(self.score))+" - Misses:"+str(int(self.misses))+" - Accuracy:"+f"{finalAcur:.2f}%",glm.vec2(640,0),glm.vec3(0.7,0.7,0.7),10,16,aling="center");
        if sc.botplay:
            sc.render.draw_cam_text(None,"(BOTPLAY)",glm.vec2(640,30),glm.vec3(0.7,0.7,0.7),10,16,aling="center");
        notesNames = ["arrowLEFT","arrowDOWN","arrowUP","arrowRIGHT","left press","down press","up press","right press","left confirm","down confirm","up confirm","right confirm"];
        for i in range(len(self.notePoses)):
            if self.pressed[i] == 0:
                sc.render.draw_cam_offset_scale("notes",notesNames[i%4],0,self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
            elif self.pressed[i] > 0:
                sc.render.draw_cam_offset_scale("notes",notesNames[i%4+4],int(glm.floor(self.pressed[i]*3)),self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
            else:
                sc.render.draw_cam_offset_scale("notes",notesNames[i%4+8],int(glm.floor(-self.pressed[i]*3)),self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
        notesNames = ["purple hold piece","blue hold piece","green hold piece","red hold piece","pruple end hold","blue hold end","green hold end","red hold end"];
        for note in self.longChart:
            if note[3]:
                posy1 = (note[0]-self.songPos)*1000;
                posy2 = (note[1]-self.songPos)*1000;
                anima1 = notesNames[note[2]%4]
                anima2 = notesNames[note[2]%4+4]
                scale = glm.vec2(0.8,posy2-posy1);
                position = self.notePoses[note[2]]+self.stage.modChart(posy1);
                tex.textures["notes"].use(0);
        
                model = glm.translate(glm.mat4x4(),glm.vec3(640,480,0));
                model = glm.scale(model,glm.vec3(sc.render.cam.w,sc.render.cam.w,1));
                model = glm.rotate(model,sc.render.cam.z,glm.vec3(0,0,1))
                model = glm.translate(model,glm.vec3(position-sc.render.cam.xy-glm.vec2(640,480),0));
                model = glm.scale(model,glm.vec3(glm.abs(tex.sprites["notes"].anims[anima1][0].rwh.x)*scale.x,scale.y,1));
                model = glm.translate(model,glm.vec3(-0.5,0,0));
                sc.render.shaders["longNote"].program["trans"].write(model);
                if note[3] == 2:
                    sc.render.shaders["longNote"].program["cut"].write(glm.float32(min(1,max(-posy1/(posy2-posy1),0))));
                else:
                    sc.render.shaders["longNote"].program["cut"].write(glm.float32(0));
                sc.render.shaders["longNote"].program["rep"].write(glm.float32(scale.y/(tex.sprites["notes"].anims[anima1][0].rwh.y*scale.x)));
                sc.render.shaders["longNote"].program["img1"].write(glm.vec4(tex.sprites["notes"].anims[anima1][0].xy,tex.sprites["notes"].anims[anima1][0].wh));
                sc.render.shaders["longNote"].program["img2"].write(glm.vec4(tex.sprites["notes"].anims[anima2][0].xy,tex.sprites["notes"].anims[anima2][0].wh));
                sc.render.shaders["longNote"].render();
        notesNames = ["purple","blue","green","red","purple","blue","green","red"];
        for note in self.chart:
            if note[2]:
                notePos = note[0]-self.songPos;
                sc.render.draw_cam_offset_scale("notes",notesNames[note[1]],0,self.notePoses[note[1]]+self.stage.modChart(notePos*1000),glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
