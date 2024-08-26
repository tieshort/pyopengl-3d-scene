#version 440 core
layout (triangles, max_vertices = 3) in;
layout (triangles, max_vertices = 3) out;

in VS_OUT {
    vec3 Normal;
    vec3 FragPos;
} gs_in[];

out vec3 Normal;
out vec3 FragPos;

void main() {  
    for (int i = 0; i < 3; i++)
    {
        gl_Position = gl_in[i].gl_Position;
        Normal = gs_in[i].Normal;
        FragPos = gs_in[i].FragPos;
        EmitVertex();
    }  
    
    EndPrimitive();
}