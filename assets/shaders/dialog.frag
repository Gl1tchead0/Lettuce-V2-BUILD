#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform vec2 pos;
uniform vec2 size;

uniform vec2 dsiz;

vec2 get_uv(vec2 xy) {
    xy.y = 1.0-xy.y;
    vec2 nuv = xy*size;
    return vec2(nuv.x,size.y-nuv.y)+pos;
}

void main() {
    vec2 pos = uv*dsiz;
    if(pos.x > dsiz.x - 0.55) {pos.x -= dsiz.x - 1;}
    else if(pos.x > 0.45) {pos.x = 0.45;}
    if(pos.y > dsiz.y - 0.5) {pos.y -= dsiz.y - 1;}
    else if(pos.y > 0.5) {pos.y = 0.5;}
    fragColor = texture2D(u_texture_0,get_uv(pos));
}