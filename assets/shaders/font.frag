#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform vec3 color;

void main() {
    fragColor = vec4(color,texture2D(u_texture_0,uv).r);
}