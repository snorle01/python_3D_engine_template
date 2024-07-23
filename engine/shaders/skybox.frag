#version 330 core
out vec4 fragColor;

in vec4 clip_coords;

uniform samplerCube u_texture_skybox;
uniform mat4 m_inv_proj_view;

void main() {
    vec4 world_coords = m_inv_proj_view * clip_coords;
    vec3 tex_cube_coords = normalize(world_coords.xyz / world_coords.w);
    fragColor = texture(u_texture_skybox, tex_cube_coords);
}