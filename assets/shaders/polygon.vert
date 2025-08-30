#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

out vec3 color;
uniform mat4 proj;
uniform mat4 trans;
uniform mat4 cam;

void main() { 
    color = in_color;
    gl_Position = proj * cam * trans * vec4(in_position, 1.0);
}