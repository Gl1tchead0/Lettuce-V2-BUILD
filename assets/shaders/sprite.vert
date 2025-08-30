#version 330 core

layout (location = 0) in vec2 in_textcoord_0;
layout (location = 1) in vec2 in_position;

out vec2 uv;
uniform mat4 proj;
uniform mat4 trans;
uniform mat4 cam;

uniform vec2 pos;
uniform vec2 size;

void main() { 
    vec2 xy = in_textcoord_0;
    xy.y = 1.0-xy.y;
    vec2 nuv = xy*size;
    uv = vec2(nuv.x,size.y-nuv.y)+pos;
    gl_Position = proj * cam * trans * vec4(in_position, 0.0, 1.0);
}