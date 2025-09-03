import glm;
import pygame as pg;
import json;
import random as ran;
from engine import screen as sc;
from engine import sprites as spr;
from engine import assets as ass;
from engine import musicPlayer as mup;
import importlib as il;
import main;

class State:
    def __init__(self):
        self.song = sc.song;
        self.songPos = -5;
        self.score = 0;
        self.acurasi = 0;
        self.acuCoun = 0;
        self.misses = 0;
        self.lastBeat = 0;
        self.curBeat = 0;
        self.lastStep = 0;
        self.curStep = 0;
        self.stepOfset = 0;
        self.timeOffset = 0;
        self.live = 1;

        self.bump = 1;
        
        self.intro = glm.vec2(0,0);
        
        self.speed = 1;
        
        self.ratingAlpha = 0;
        self.numbersAlpha = 0;
        self.comboAlpha = 0;
        self.rating = "shit";
        
        self.hudZoom = 1;
        self.pressed = [];
        self.presDif = [0,0,0,0];
        self.notePoses = [];
        if sc.config["downscroll"]:
            for i in range(4):
                self.notePoses.append(glm.vec2(772+130*i,628));
            for i in range(4):
                self.notePoses.append(glm.vec2(112+130*i,628));
        else:
            for i in range(4):
                self.notePoses.append(glm.vec2(772+130*i,92));
            for i in range(4):
                self.notePoses.append(glm.vec2(112+130*i,92));
        self.noteVector = glm.vec2(0,0);
        self.pausa = False;
        self.pauseOpt = 0;
        self.songFrame = 0;
        self.songFade = 0;
        
    def load(self):
        #cargar chart
        self.chart = [];
        self.longChart = [];
        mustHitSection = False;
        
        sc.mp.change_audio_a('assets/songs/'+sc.song+"/inst.ogg");
        sc.mp.change_audio_b('assets/songs/'+sc.song+"/voices.ogg");
        sc.mp.paused = True;
        
        with open('assets/songs/'+sc.song+"/chart.json",'r') as file:
            chart = json.load(file);
        with open('assets/characters/'+chart["song"]["player1"]+".json",'r') as file:
            bfJs = json.load(file);
        with open('assets/characters/'+chart["song"]["player2"]+".json",'r') as file:
            dadJs = json.load(file);
        if "events" in chart["song"]:
            self.events = chart["song"]["events"];
        else:
            self.events = [];
        self.curEven = 0;
        self.bpm = chart["song"]["bpm"];
        self.songPos = -5*60/self.bpm;
        self.speed = chart["song"]["speed"];i = 0;
        for sect in chart["song"]["notes"]:
            if sect["changeBPM"]:
                self.events.append([((i*sect["sectionBeats"])/self.bpm)*60,[["Change bpm",sect["bpm"]]]]);
            if sect["mustHitSection"]:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,note[1],True]);
                    if note[2] > 0:
                        self.longChart.append([note[0]*0.001,(note[0]+note[2])*0.001,note[1],1]);
                if mustHitSection != sect["mustHitSection"]:
                    if "sectionBeats" in sect:
                        self.events.append([((i*sect["sectionBeats"])/self.bpm)*60,
                                        [["Change look",True,0],["Camera look at pos",bfJs["camera_position"][0],bfJs["camera_position"][1]]]]);
                    else:
                        self.events.append([((i*4)/self.bpm)*60,
                                        [["Change look",True,0],["Camera look at pos",bfJs["camera_position"][0],bfJs["camera_position"][1]]]]);
            else:
                for note in sect["sectionNotes"]:
                    self.chart.append([note[0]*0.001,(note[1]+4)%8,True]);
                    if note[2] > 0:
                        self.longChart.append([note[0]*0.001,(note[0]+note[2])*0.001,(note[1]+4)%8,1]);
                if mustHitSection != sect["mustHitSection"]:
                    if "sectionBeats" in sect:
                        self.events.append([((i*sect["sectionBeats"])/self.bpm)*60,
                                        [["Change look",False,0],["Camera look at pos",dadJs["camera_position"][0],dadJs["camera_position"][1]]]]);
                    else:
                        self.events.append([((i*4)/self.bpm)*60,
                                        [["Change look",False,0],["Camera look at pos",dadJs["camera_position"][0],dadJs["camera_position"][1]]]]);
            mustHitSection = sect["mustHitSection"];
            i += 1;
        sorted(self.events,key=lambda x: x[0], reverse=True);
        self.stage = il.import_module("stages."+chart["song"]["stage"]).Stage();
        #cargar los assets
        fondo2load,sprites2load,sounds2load,models2load = self.stage.load();

        self.bfP = glm.vec2(bfJs["position"][0],bfJs["position"][1]);
        self.bfS = bfJs["scale"];
        self.bfD = {};
        self.bfA = "idle";
        self.bfF = 0;
        self.bfC = glm.vec3(bfJs["healthbar_colors"][0]/255,bfJs["healthbar_colors"][1]/255,bfJs["healthbar_colors"][2]/255);
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
        self.dadC = glm.vec3(dadJs["healthbar_colors"][0]/255,dadJs["healthbar_colors"][1]/255,dadJs["healthbar_colors"][2]/255);
        for anim in dadJs["animations"]:
            self.dadD[anim["anim"]] = (anim["name"],glm.vec2(anim["offsets"][0],anim["offsets"][1]));
        sprites2load.append(("dad",'assets/images/'+dadJs["image"]));
        self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);self.pressed.append(0);
        
        sprites2load.append(("notes",'assets/images/NOTE_assets'));
        sprites2load.append(("hud",'assets/images/hudWeas'));

        fondo2load.append(("icon1","assets/images/icons/"+dadJs["healthicon"]+".png"))
        fondo2load.append(("icon2","assets/images/icons/"+bfJs["healthicon"]+".png"))
        fondo2load.append(("icon1l","assets/images/icons/"+dadJs["healthicon"]+"-lose.png"))
        fondo2load.append(("icon2l","assets/images/icons/"+bfJs["healthicon"]+"-lose.png"))
        
        sounds2load.append(("mis1",'assets/sounds/missnote1.ogg'));
        sounds2load.append(("mis2",'assets/sounds/missnote2.ogg'));
        sounds2load.append(("mis3",'assets/sounds/missnote3.ogg'));
        
        sounds2load.append(("int1",'assets/sounds/intro1.ogg'));
        sounds2load.append(("int2",'assets/sounds/intro2.ogg'));
        sounds2load.append(("int3",'assets/sounds/intro3.ogg'));
        sounds2load.append(("intG",'assets/sounds/introGo.ogg'));

        return fondo2load, sprites2load,sounds2load,models2load;

    def update(self,keypress):
        if self.pausa:#pausa
            if keypress == sc.config["keys"]["menu up"]:
                self.pauseOpt = (self.pauseOpt-1)%3;
            if keypress == sc.config["keys"]["menu down"]:
                self.pauseOpt = (self.pauseOpt+1)%3;

            if keypress == sc.config["keys"]["back"]:
                sc.mp.change_audio_a('assets/songs/'+sc.song+"/inst.ogg");
                sc.mp.change_audio_b('assets/songs/'+sc.song+"/voices.ogg");
                sc.mp.stream_a.seek(self.songFrame);
                sc.mp.stream_b.seek(self.songFrame);
                self.pausa = False;
            if keypress == sc.config["keys"]["accept"]:
                if self.pauseOpt == 0:
                    sc.mp.change_audio_a('assets/songs/'+sc.song+"/inst.ogg");
                    sc.mp.change_audio_b('assets/songs/'+sc.song+"/voices.ogg");
                    sc.mp.stream_a.seek(self.songFrame);
                    sc.mp.stream_b.seek(self.songFrame);
                    self.pausa = False;
                elif self.pauseOpt == 1:
                    main.loadState("playState");
                    return True;
                else:
                    main.loadState("menuState");
                    return True;

            self.songFade = min(1,self.songFade+sc.deltatime*0.1);

            sc.mp.VOLUME_A = (self.songFade*self.songFade)*sc.trueVol;
            sc.mp.VOLUME_B = 0;
            return;
        
        self.songPos += sc.deltatime;
        semiSongPos = self.songPos;
        if sc.mp.paused:
            if self.songPos >= 0:
                sc.mp.paused = False;
                sc.mp.stream_a.seek(0);
                sc.mp.stream_b.seek(0);
        else:
            semiSongPos = sc.mp.stream_a.tell() / sc.mp.stream_a.samplerate;
            if semiSongPos >= (sc.mp.stream_a.frames_total / sc.mp.stream_a.samplerate) - 0.1:
                #terminar la song
                main.loadState("menuState");
                return True;
            if self.songPos < semiSongPos-0.2 or self.songPos > semiSongPos+0.2:
                self.songPos = semiSongPos;
            
        missS = ["mis1","mis2","mis3"];
        
        if keypress == sc.config["keys"]["accept"] or keypress == sc.config["keys"]["back"]:
            self.songFrame = sc.mp.stream_a.tell();
            sc.mp.VOLUME_A = 0;
            sc.mp.VOLUME_B = 0;
            self.songFade = 0;
            sc.mp.change_audio_a('assets/songs/pausa.ogg');
            sc.mp.change_audio_b('assets/songs/pausa.ogg');
            self.pausa = True;
        #weas del beat
        self.curStep = self.stepOfset+glm.floor(((semiSongPos-self.timeOffset)*self.bpm)*0.01666666666666666666666666666667);
        if self.curStep != self.lastStep:
            if self.songPos < 0:
                if self.curStep == -4:
                    ass.sounds["int3"].play();
                if self.curStep == -3:
                    self.intro.x = 0;
                    self.intro.y = 1;
                    ass.sounds["int2"].play();
                if self.curStep == -2:
                    self.intro.x = 1;
                    self.intro.y = 1;
                    ass.sounds["int1"].play();
                if self.curStep == -1:
                    self.intro.x = 2;
                    self.intro.y = 1;
                    ass.sounds["intG"].play();
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
            self.bump = 1.3;
        self.lastBeat = self.curBeat;
        
        #controles del jugador
        for i in range(0,len(self.pressed)):
            if self.pressed[i] >= 0:
                self.pressed[i] = max(self.pressed[i]-sc.deltatime*24,0);
            else:
                self.pressed[i] = min(self.pressed[i]+sc.deltatime*24,0);

        inputs = [0,0,0,0];
        inputsP = [pg.key.get_pressed()[sc.config["keys"]["leftA"]] or pg.key.get_pressed()[sc.config["keys"]["leftB"]],
                   pg.key.get_pressed()[sc.config["keys"]["downA"]] or pg.key.get_pressed()[sc.config["keys"]["downB"]],
                   pg.key.get_pressed()[sc.config["keys"]["upA"]] or pg.key.get_pressed()[sc.config["keys"]["upB"]],
                   pg.key.get_pressed()[sc.config["keys"]["rightA"]] or pg.key.get_pressed()[sc.config["keys"]["rightB"]],];
        for i in range(0,len(inputsP)):
            if self.presDif[i] != inputsP[i]:
                inputs[i] = inputsP[i];
            
        self.presDif = inputsP;
        
        for i in range(0,len(inputsP)):
            if inputsP[i] and self.pressed[i] >= 0:
                self.pressed[i] = 1;

        #notas largas
        for note in self.longChart:
            if note[3]:
                notePos = (note[0]-self.songPos)*5;
                if notePos < -1 and note[3] == 1:
                    note[3] = 0;
                elif note[2] < 4:
                    if sc.config["botplay"]:
                        if notePos <= 0:
                            note[3] = 2;
                            self.pressed[note[2]] = -1;
                            self.bfPosing = 0.25;
                            self.bfF = 0;
                            self.live += 0.025;
                            if note[2]-4 == 0:
                                self.bfA = "singLEFT";
                            elif note[2]-4 == 1:
                                self.bfA = "singDOWN";
                            elif note[2]-4 == 2:
                                self.bfA = "singUP";
                            elif note[2]-4 == 3:
                                self.bfA = "singRIGHT";
                        if (note[1]-self.songPos)*5 <= 0:
                            note[3] = 0;
                    else:
                        notePos = abs(notePos);
                        if inputs[note[2]] and notePos < 1:
                            note[3] = 2;
                        if note[3] == 2:
                            if not inputsP[note[2]]:
                                note[3] = 0;
                                if (note[1]-self.songPos-0.2)*5 > 0:
                                    ass.sounds[missS[ran.randint(0,2)]].play();
                                    self.acurasi += 0;
                                    self.acuCoun += 1;
                                    self.misses += 1;
                                    self.bfPosing = 0.25;
                                    self.live -= 0.05;
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
                            self.live += 0.025;
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
                notePos = (note[0]-self.songPos)*5;
                if notePos < -1 and not sc.config["botplay"]:
                    note[2] = False;
                    ass.sounds[missS[ran.randint(0,2)]].play();
                    self.acurasi += 0;
                    self.acuCoun += 1;
                    self.misses += 1;
                    self.bfPosing = 0.25;
                    self.live -= 0.05;
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
                    if sc.config["botplay"]:
                        if notePos < 0:
                            note[2] = False;
                            self.pressed[note[1]] = -1;
                            self.bfPosing = 0.25;
                            self.live += 0.025;
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
                            self.live += 0.025;
                            self.acuCoun += 1;
                            if notePos > 0.6:#Shit
                                self.ratingAlpha = 1;
                                self.rating = "shit";
                            elif notePos > 0.4:#Bad
                                self.ratingAlpha = 1;
                                self.rating = "bad";
                            elif notePos > 0.2:#Good
                                self.ratingAlpha = 1;
                                self.rating = "good";
                            else:#Sick
                                self.ratingAlpha = 1;
                                self.rating = "sick";
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
                    if even[0] == "Change bpm":
                        self.bpm = even[1];
                        self.stepOfset = self.curStep;
                        self.timeOffset = self.songPos;
                    else:
                        self.stage.onEvent(even[0],even[1],even[2]);
                self.curEven += 1;
        #zooms del hud
        self.hudZoom += (1-self.hudZoom)*(2*sc.deltatime);
        self.ratingAlpha = max(self.ratingAlpha-sc.deltatime,0);

        self.bump += (1-self.bump)*(7*sc.deltatime);

        #limites y perder
        self.live = min(2,self.live);
        
        #boludeces del volumen
        sc.mp.VOLUME_A = sc.trueVol;
        sc.mp.VOLUME_B = sc.trueVol;
        
        self.intro.y = max(self.intro.y-sc.deltatime*3,0);
        self.stage.update();
    
    def draw(self):
        #fondo mierdas
        #sc.render.cam = self.camGame;
        self.shaind = "sprite";
        self.stage.draw();
        self.shaind = "sprite";
        #personajes mierdas
        self.bfPosing = max(self.bfPosing-sc.deltatime,0);
        self.bfF = min(self.bfF+sc.deltatime*24,len(ass.sprites["bf"].anims[self.bfD[self.bfA][0]])-1);
        sc.render.draw_scale("bf",self.bfD[self.bfA][0],int(glm.floor(self.bfF)),self.bfP,glm.vec2(self.bfS),suboffset=self.bfD[self.bfA][1])

        self.dadPosing = max(self.dadPosing-sc.deltatime,0);
        self.dadF = min(self.dadF+sc.deltatime*24,len(ass.sprites["dad"].anims[self.dadD[self.dadA][0]])-1);
        sc.render.draw_scale("dad",self.dadD[self.dadA][0],int(glm.floor(self.dadF)),self.dadP,glm.vec2(self.dadS),suboffset=self.dadD[self.dadA][1])
            
    def drawHUD(self):
        #hud mierdas
        sc.render.camT = glm.translate(glm.mat4x4(),glm.vec3(640,480,0));
        sc.render.camT = glm.scale(sc.render.camT,glm.vec3(self.hudZoom));
        sc.render.camT = glm.translate(sc.render.camT,-glm.vec3(640,480,0));
        #sc.render.cam = glm.vec4(0,0,0,self.hudZoom);
        finalAcur = 100;
        if self.acuCoun > 0:
            finalAcur = (self.acurasi/self.acuCoun)*100;
        sc.render.draw_text(None,"Score:"+str(int(self.score))+" - Misses:"+str(int(self.misses))+" - Accuracy:"+f"{finalAcur:.2f}%",glm.vec2(640,0),glm.vec3(0.7,0.7,0.7),10,16,aling="center");
        if sc.config["botplay"]:
            sc.render.draw_text(None,"(BOTPLAY)",glm.vec2(640,30),glm.vec3(0.7,0.7,0.7),10,16,aling="center");
        #dibujar barra de vida
        sc.render.s_rect(glm.vec2(320,630),glm.vec2(640,20),glm.vec4(0,0,0,1));
        sc.render.s_rect(glm.vec2(325,635),glm.vec2(630,10),glm.vec4(self.bfC,1));
        sc.render.s_rect(glm.vec2(325,635),glm.vec2(630*((2-self.live)*0.5),10),glm.vec4(self.dadC,1));
        sc.render.draw_back_scale("icon1",glm.vec3(955-315*self.live-70,645,0),glm.vec2(self.bump),glm.vec2(0.5));
        sc.render.draw_back_scale("icon2",glm.vec3(955-315*self.live+70,645,0),glm.vec2(-self.bump,self.bump),glm.vec2(0.5));

        notesNames = ["arrowLEFT","arrowDOWN","arrowUP","arrowRIGHT","left press","down press","up press","right press","left confirm","down confirm","up confirm","right confirm"];
        for i in range(len(self.notePoses)):
            if self.pressed[i] == 0:
                sc.render.draw_offset_scale("notes",notesNames[i%4],0,self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
            elif self.pressed[i] > 0:
                sc.render.draw_offset_scale("notes",notesNames[i%4+4],int(glm.floor(3-self.pressed[i]*3)),self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
            else:
                sc.render.draw_offset_scale("notes",notesNames[i%4+8],int(glm.floor(3+self.pressed[i]*3)),self.notePoses[i],glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
        notesNames = ["purple hold piece","blue hold piece","green hold piece","red hold piece","pruple end hold","blue hold end","green hold end","red hold end"];
        for note in self.longChart:
            if note[3]:
                posy1 = (note[0]-self.songPos)*400*self.speed;
                posy2 = (note[1]-self.songPos)*400*self.speed;
                anima1 = notesNames[note[2]%4]
                anima2 = notesNames[note[2]%4+4]
                scale = glm.vec2(0.8,posy2-posy1);
                position = self.notePoses[note[2]]+self.stage.modChart(posy1);
                ass.textures["notes"].use(0);
        
                model = glm.translate(glm.mat4x4(),glm.vec3(position,0));
                if sc.config["downscroll"]:
                    model = glm.scale(model,glm.vec3(glm.abs(ass.sprites["notes"].anims[anima1][0].rwh.x)*scale.x,-scale.y,1));
                else:
                    model = glm.scale(model,glm.vec3(glm.abs(ass.sprites["notes"].anims[anima1][0].rwh.x)*scale.x,scale.y,1));
                model = glm.translate(model,glm.vec3(-0.5,0,0));
                sc.render.shaders["longNote"].program["proj"].write(sc.proj);
                sc.render.shaders["longNote"].program["trans"].write(model);
                sc.render.shaders["longNote"].program["cam"].write(sc.render.camT);
                if note[3] == 2:
                    sc.render.shaders["longNote"].program["cut"].write(glm.float32(min(1,max(-posy1/(posy2-posy1),0))));
                else:
                    sc.render.shaders["longNote"].program["cut"].write(glm.float32(0));
                sc.render.shaders["longNote"].program["rep"].write(glm.float32(scale.y/(ass.sprites["notes"].anims[anima1][0].rwh.y*scale.x)));
                sc.render.shaders["longNote"].program["img1"].write(glm.vec4(ass.sprites["notes"].anims[anima1][0].xy,ass.sprites["notes"].anims[anima1][0].wh));
                sc.render.shaders["longNote"].program["img2"].write(glm.vec4(ass.sprites["notes"].anims[anima2][0].xy,ass.sprites["notes"].anims[anima2][0].wh));
                sc.render.shaders["longNote"].render();
        notesNames = ["purple","blue","green","red","purple","blue","green","red"];
        cant = 0;
        for note in self.chart:
            if note[2] and cant < 100:
                notePos = note[0]-self.songPos;
                cant += 1;
                sc.render.draw_offset_scale("notes",notesNames[note[1]],0,self.notePoses[note[1]]+self.stage.modChart(notePos*400*self.speed),glm.vec2(0.8,0.8),glm.vec2(0.5,0.5));
            #else:
            #    break;
            
        sc.render.shaind = "blend";
        sc.render.shaders["blend"].program["color"].write(glm.vec4(1,1,1,self.ratingAlpha));
        sc.render.draw("hud",self.rating,0,glm.vec2(640,360+self.ratingAlpha*100),glm.vec2(0.5,0.5));
        #3,2,1,go   self.intro
        sc.render.shaders["blend"].program["color"].write(glm.vec4(1,1,1,self.intro.y));
        sc.render.draw_scale("hud","intro",int(glm.floor(self.intro.x)),glm.vec2(640,360),glm.vec2(0.8+self.intro.y*0.2),glm.vec2(0.5,0.5));
        sc.render.shaind = "sprite";

        if self.pausa:
            sc.render.s_rect(glm.vec2(0,0),glm.vec2(1280,720),glm.vec4(0,0,0,0.8));
            opciones = [
                "resume",
                "restart",
                "menu"
            ];
            for i in range(len(opciones)):
                pos = 352+16*(i-self.pauseOpt);
                tono = max(0,min(1-abs((pos-352)*0.01),1));
                if i == self.pauseOpt:
                    sc.render.draw_text(None,opciones[i],glm.vec2(75,pos),glm.vec3(tono,tono,tono),10,16,aling="left");
                else:
                    sc.render.draw_text(None,opciones[i],glm.vec2(64,pos),glm.vec3(tono,tono,tono),10,16,aling="left");
            sc.render.draw_text(None,"pausa",glm.vec2(64,232),glm.vec3(0.7,0.7,0.7),10,16,aling="left");