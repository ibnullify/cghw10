import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    ambient = calculate_ambient(ambient, areflect) 
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)

    total_light = [ambient[0] + diffuse[0] + specular[0],
                   ambient[1] + diffuse[1] + specular[1],
                   ambient[2] + diffuse[2] + specular[2]]

    return limit_color(total_light)

def calculate_ambient(alight, areflect):
    ambient = [int(alight[0] * areflect[0]),
               int(alight[1] * areflect[1]),
               int(alight[2] * areflect[2])]
    
    return limit_color(ambient)

def calculate_diffuse(light, dreflect, normal):
    #Dot product of the normalizations
    normal_light = dot_product( normalize(normal) , normalize(light[LOCATION]) )
    diffuse = [int( (light[1][0] * dreflect[0]) * normal_light ),
               int( (light[1][1] * dreflect[1]) * normal_light ),
               int( (light[1][2] * dreflect[2]) * normal_light )]
     
    return limit_color(diffuse) 

def calculate_specular(light, sreflect, view, normal):
    color = [light[1][0] * sreflect[0],
             light[1][1] * sreflect[1],
             light[1][2] * sreflect[2]]

    normal_light = dot_product( normalize(normal) , normalize(light[LOCATION]) )
    if (normal_light <= 0):
        return [0,0,0]
    else:
        a = [x * 2 * normal_light for x in normalize(normal)]
        b = [i - j for i,j in zip( a, normalize(light[LOCATION] ))]
        c = [int( x * (dot_product( b, normalize(view) )**8 ) ) for x in color]
    return limit_color(c) 

def limit_color(color):    
    for x in range(len(color)):
        if color[x] <= 0:
            color[x] = 0
        elif (color[x] >= 255):
            color[x] = 255
        else:
            pass
    return color 

#vector functions
def normalize(vector):
    #magnitude is the root of the sum of the squares
    x = vector[0]**2
    y = vector[1]**2
    z = vector[2]**2
    magnitude = ( x + y + z )**0.5 #square root
    return ([value/magnitude for value in vector]) 

def dot_product(a, b):
    #sum of the products of corresponding entries
    return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2]) 


def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
