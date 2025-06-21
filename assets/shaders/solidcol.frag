#version 330 core

layout (location = 0) out vec4 fragColor;

uniform vec4 col;

void main() {
    fragColor = col;
}