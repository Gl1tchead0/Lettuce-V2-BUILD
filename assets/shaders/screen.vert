#version 330 core

layout (location = 0) in vec2 in_textcoord_0;
layout (location = 1) in vec2 in_position;

out vec2 uv;
uniform mat4 trans;

void main() { 
    uv = in_textcoord_0;
    gl_Position = trans * vec4(in_position, 0.0, 1.0);
}