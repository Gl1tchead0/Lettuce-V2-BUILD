#version 330 core

layout (location = 0) in vec2 in_position;

uniform mat4 proj;
uniform mat4 trans;

void main() { 
    gl_Position = proj * trans * vec4(in_position, 0.0, 1.0);
}