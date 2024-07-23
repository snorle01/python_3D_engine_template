#version 330 core
layout (location = 0) in vec3 in_position;

out vec4 clip_coords;

void main() {
    gl_Position = vec4(in_position, 1.0);
    clip_coords = gl_Position;
}