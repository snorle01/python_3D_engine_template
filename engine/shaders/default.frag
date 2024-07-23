#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 frag_pos;

struct light_class {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform light_class light;
uniform sampler2D u_texture_0;
uniform vec3 cam_pos;

vec3 get_light(vec3 color) {
    vec3 normalized_normal = normalize(normal);
    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 light_dir = normalize(light.position - frag_pos);
    float diff = max(0, dot(light_dir, normalized_normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 view_dir = normalize(cam_pos - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, normalized_normal);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    color = get_light(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}