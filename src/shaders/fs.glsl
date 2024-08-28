#version 440 core

#define NUM_DIRLIGHTS 1
#define NUM_POINTLIGHTS 1
#define NUM_SPOTLIGHTS 2

out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

struct DirLight
{
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};
struct PointLight
{
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};

struct SpotLight
{
    vec3 position;
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;

    float cutOff;
    float outerCutOff;
};

struct Material
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
    float transparency;
    float reflectivity;
    float refractive_index;
};

uniform vec3 viewPos;
uniform DirLight[NUM_DIRLIGHTS] dirlights;
uniform PointLight[NUM_POINTLIGHTS] pointlights;
uniform SpotLight[NUM_SPOTLIGHTS] spotlights;
uniform Material material;
uniform samplerCube skybox;

vec3 calcDirLight(DirLight light, vec3 normal, vec3 viewDir);
vec3 calcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);
vec3 calcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    
    vec3 result = vec3(0);

    for(int i = 0; i < NUM_DIRLIGHTS; i++)
    {
        result += calcDirLight(dirlights[i], norm, viewDir);
    }

    for(int i = 0; i < NUM_POINTLIGHTS; i++)
    {
        result += calcPointLight(pointlights[i], norm, FragPos, viewDir);
    }

    for(int i = 0; i < NUM_SPOTLIGHTS; i++)
    {
        result += calcSpotLight(spotlights[i], norm, FragPos, viewDir);
    }
    
    vec3 I = normalize(FragPos - viewPos);
    vec3 N = normalize(Normal);
    vec3 R = reflect(I, N);
    vec3 reflection = texture(skybox, R).rgb;

    float eta = 1.0 / material.refractive_index;
    vec3 T = refract(I, N, eta);
    vec3 refraction = texture(skybox, T).rgb;

    float fresnelFactor = pow(1.0 - max(dot(norm, viewDir), 0.0), 5.0);
    fresnelFactor = mix(0.1, 1.0, fresnelFactor);

    vec3 mirroredColor = mix(refraction, reflection, fresnelFactor);
    FragColor = vec4(mix(result, mirroredColor, material.reflectivity), 1.0 - material.transparency);

    bool enableGammaCorrection = false;
    if(enableGammaCorrection){
        float gamma = 2.2;
        FragColor.rgb = pow(FragColor.rgb, vec3(1.0 / gamma));
    }
}

// calculates the color when using a directional light.
vec3 calcDirLight(DirLight light, vec3 normal, vec3 viewDir)
{
    vec3 lightDir = normalize(-light.direction);

    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);

    // specular shading (blinn-phong / phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.shininess);
    // vec3 reflectDir = reflect(-lightDir, normal);
    // float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);

    // combine results
    vec3 ambient = light.ambient * material.ambient;
    vec3 diffuse = light.diffuse * diff * material.diffuse;
    vec3 specular = light.specular * spec * material.specular;
    return (ambient + diffuse + specular);
}

// calculates the color when using a point light.
vec3 calcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    vec3 lightDir = normalize(light.position - fragPos);

    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);

    // specular shading
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.shininess);
    // vec3 reflectDir = reflect(-lightDir, normal);
    // float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);

    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

    // combine results
    vec3 ambient = light.ambient * material.ambient;
    vec3 diffuse = light.diffuse * diff * material.diffuse;
    vec3 specular = light.specular * spec * material.specular;
    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
}

// calculates the color when using a spot light.
vec3 calcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    vec3 lightDir = normalize(light.position - fragPos);

    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);

    // specular shading
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.shininess);
    // vec3 reflectDir = reflect(-lightDir, normal);
    // float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);

    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

    // spotlight intensity
    float theta = dot(lightDir, normalize(-light.direction)); 
    float epsilon = light.cutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);
    
    // combine results
    vec3 ambient = light.ambient * material.ambient;
    vec3 diffuse = light.diffuse * diff * material.diffuse;
    vec3 specular = light.specular * spec * material.specular;
    ambient *= attenuation;
    diffuse *= attenuation * intensity;
    specular *= attenuation * intensity;
    return (ambient + diffuse + specular);
}