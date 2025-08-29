#version 330 core

layout (location = 0) in vec2 in_position;
layout (location = 1) in vec3 in_color;

out vec3 color;
uniform mat4 proj;
uniform mat4 trans;

void main() { 
    color = in_color;
    gl_Position = proj * trans * vec4(in_position, 0.0, 1.0);
}