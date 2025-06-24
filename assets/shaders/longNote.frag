#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform float cut;
uniform float rep;
uniform vec4 img1;
uniform vec4 img2;

void main() {
    vec2 pos = vec2(uv.x,(uv.y-1.0)*rep+1.0);
    if(uv.y < cut) {
        fragColor = vec4(0.0);
        return;
    }
    if(pos.y > 0.0) {
        pos.y = 1.0-mod(pos.y,1.0);
        vec2 nuv = pos*img2.zw;
        fragColor = texture2D(u_texture_0,vec2(nuv.x,img2.w-nuv.y)+img2.xy);
    }
    else {
        pos.y = 1.0-mod(pos.y,1.0);
        vec2 nuv = pos*img1.zw;
        fragColor = texture2D(u_texture_0,vec2(nuv.x,img1.w-nuv.y)+img1.xy);
    }
}