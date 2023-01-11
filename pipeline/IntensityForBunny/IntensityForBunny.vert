#version 130

in vec3 attr_position;
in vec4 attr_color;
uniform mat4 MVP;
out vec4 colorfromvs;

void main(void) 
{
    gl_Position = MVP * vec4(attr_position,1.0);
    colorfromvs = attr_color;
}
