#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;
uniform vec4 color;

void main() {
    fragColor = texture2D(u_texture_0,uv) * color;
}