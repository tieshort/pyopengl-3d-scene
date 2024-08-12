#version 400 core

out vec4 FragColor;

in vec2 TexCoords;
in vec3 FragPos;
in vec3 Normal;

uniform sampler2D texture1;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;

uniform vec3 ambient;
uniform vec3 diffuse;
uniform vec3 specular;
uniform float shininess;

void main()
{
    vec3 ambient = ambient * lightColor;

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = lightColor * (diff * diffuse);

    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = lightColor * (spec * specular);

    vec3 result = (ambient + diffuse + specular);
    // FragColor = vec4(result, 1.0) * texture(texture1, TexCoords);
    FragColor = vec4(result, 1.0);
}