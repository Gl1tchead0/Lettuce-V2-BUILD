#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform vec2 pos;
uniform vec2 size;

vec2 get_uv(vec2 xy) {
    xy.y = 1.0-xy.y;
    vec2 nuv = xy*size;
    return vec2(nuv.x,size.y-nuv.y)+pos;
}

void main() {
    fragColor = texture2D(u_texture_0,get_uv(uv));
}