#version 130

in vec4 colorfromvs;
out vec4 color;

void main(void) 
{
    color = colorfromvs;    
}
