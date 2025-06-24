import pygame as pg;
import moderngl as mgl;
import glm;
import json as js;
import os;
from engine import renderer as ren;

pg.init();

real_res = (1280,720);
real_mouse = glm.vec2(0,0);

pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3);
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3);
pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE);
win = pg.display.set_mode(real_res,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE);
pg.display.set_caption("PyFunkin");
ctx = mgl.create_context(require=330);
#ctx.enable(flags=mgl.DEPTH_TEST);
clock = pg.time.Clock();
deltatime = 0;

ctx.enable(mgl.BLEND);
ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA);

texture = ctx.texture((1280,720), 3);
texture.filter = (mgl.LINEAR, mgl.LINEAR);
#drb = ctx.depth_renderbuffer((960,540));
screen_fbo = ctx.framebuffer(color_attachments=[texture]);
proj = glm.ortho(0.0, 1280.0, 720.0, 0.0, -1000.0, 1000.0);

render = ren.Renderer();

vcrTex = None;
vcrSpr = None;
state = None;

song = "TomachiP";
botplay = True;

#pg.event.set_grab(True);

#font = pg.font.Font("assets/Moderniz.otf",12);