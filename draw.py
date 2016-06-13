from display import *
from matrix import *
from gmath import calculate_dot, calculate_flat, perspective_induce
from math import cos, sin, pi

MAX_STEPS = 100

def scanline_conversion( screen, top, mid, bot, zbuffer, color):
    c = 0
    while bot[1] + c < top[1]:
        dx0 = (0.0 + top[0] - bot[0])/(top[1] - bot[1])
        dz0 = (0.0 + top[2] - bot[2])/(top[1] - bot[1])
        if bot[1] + c < mid[1]:
            dx1 = (0.0 + mid[0] - bot[0]) / (mid[1] - bot[1])
            dz1 = (0.0 + mid[2] - bot[2])/ (mid[1] - bot[1])
            draw_line(screen,
                      bot[0] + c*dx0,
                      bot[1] + c,
                      bot[2] + c * dz0,
                      bot[0] + c*dx1,
                      bot[1] + c,
                      bot[2] + c * dz1,
                      zbuffer, color)
        else:
            dx1 = (0.0 + top[0] - mid[0]) / (top[1] - mid[1])
            dz1 = (0.0 + top[2] - mid[2]) / (top[1] - mid[1])
            draw_line(screen,
                      bot[0] + c*dx0,
                      bot[1] + c,
                      bot[2] + c * dz0,
                      mid[0] + (c + bot[1] - mid[1])*dx1,
                      bot[1] + c,
                      mid[2] + (c + bot[1] - mid[1]) * dz1,
                      zbuffer, color)
        c = c + 1

def vertical_conversion(screen, top, mid, bot, zbuffer, color):
    c = 0
    while bot[0] + c < top[0]:
        dy0 = (0.0 + top[1] - bot[1])/(top[0] - bot[0])
        dz0 = (0.0 + top[2] - bot[2])/(top[0] - bot[0])
        if bot[0] + c < mid[0]:
            dy1 = (0.0 + mid[1] - bot[1]) / (mid[0] - bot[0])
            dz1 = (0.0 + mid[2] - bot[2])/ (mid[0] - bot[0])
            draw_line(screen,
                      bot[0] + c, #x0
                      bot[1] + c*dy0, #y0
                      bot[2] + c * dz0, #z0
                      bot[0] + c, #x1
                      bot[1] + c*dy1, #y1
                      bot[2] + c * dz1, #z1
                      zbuffer, color)
        else:            
            dy1 = (0.0 + top[1] - mid[1]) / (top[0] - mid[0])
            dz1 = (0.0 + top[2] - mid[2]) / (top[0] - mid[0])
            draw_line(screen,
                      bot[0] + c, #x0
                      bot[1] + c*dy0, #y0
                      bot[2] + c*dz0, #z0
                      bot[0] + c, #x1
                      mid[1] + (c + bot[0] - mid[0])*dy1, #y1
                      mid[2] + (c + bot[0] - mid[0]) * dz1, #z1
                      zbuffer, color)
                      
        c = c + 1

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )

def draw_polygons( points, screen, zbuffer, color, **optional_parameters ):
    if "specular_point" in optional_parameters and "specular_value" in optional_parameters:
        specular_point = optional_parameters["specular_point"]
        specular_value = optional_parameters["specular_value"]
        specular = True
    else:
        specular_point = [0,0,0]
        specular_value = 200
        specular = True
       
    if specular_point == None:
        specular_point = [0,0,0]

    if "ambient" in optional_parameters:
        ambient_value = optional_parameters["ambient"]
        ambient = True
    else:
        ambient_value = 10
        ambient = True
    print specular_point

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return
    black = [0,0,0]
    p = 0
    while p < len( points ) - 2:
        perspective_induce(points, p)
        if calculate_dot( points, p ) < 0:
            shade = color
            if ambient:
                shade[0] = ambient_value
                shade[1] = ambient_value
                shade[2] = ambient_value

            if specular:
                specular = calculate_flat(points, p, specular_point)
                #print specular
                if specular > 0:
                    shade[0] += int(specular * specular_value)
                    shade[1] += int(specular * specular_value)
                    shade[2] += int(specular * specular_value)
                    #print shade
                
            #set top,mid,bot as proper coordinates
            top = []
            bot = []
            for i in range(3):
                if points[p+i][1]==max(points[p][1],
                                       points[p+1][1],
                                       points[p+2][1]) and top==[]:
                    top = points[p+i]
                elif points[p+i][1]==min(points[p][1],
                                         points[p+1][1],
                                         points[p+2][1]) and bot==[]:
                    bot = points[p+i]
                else:
                    mid = points[p+i]
            #perform horizontal scanline conversion
            scanline_conversion( screen, top, mid, bot, zbuffer, shade )

            #set left, mid, and right for vertical conversion
            right = []
            left = []
            midx = []
            for i in range(3):
                if points[p+i][0]==max(points[p][0],
                                       points[p+1][0],
                                       points[p+2][0]) and right==[]:
                    right = points[p+i]
                elif points[p+i][0]==min(points[p][0],
                                         points[p+1][0],
                                         points[p+2][0]) and left==[]:
                    left = points[p+i]
                else:
                    midx = points[p+i]
            #perform vertical scanline conversion
            vertical_conversion( screen, right, midx, left, zbuffer, shade)

            draw_line( screen, points[p][0], points[p][1], points[p][2],
                       points[p+1][0], points[p+1][1], points[p+1][2],
                       zbuffer, color )
            draw_line( screen, points[p+1][0], points[p+1][1], points[p+1][2],
                       points[p+2][0], points[p+2][1], points[p+2][2],
                       zbuffer, color )
            draw_line( screen, points[p+2][0], points[p+2][1], points[p+2][2],
                       points[p][0], points[p][1], points[p][2],
                       zbuffer, color )
        p+= 3



def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, zbuffer, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2],
                   zbuffer, color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, z0, x1, y1, z1, zbuffer, color ):
    dx = x1 - x0
    dy = y1 - y0
    dz = 0
    if dx!=0 or dy!=0:
        dz = (z1 - z0) / (dx * dx + dy * dy) ** (0.5)
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
        dz = 0 - dz
        z0,z1 = z1,z0
    if dx!=0 and dy!=0:
        dz = (z1-z0)/max(dx,dy)
    z = z0
    if dx == 0:
        y = y0
        while y <= y1:
            plot(screen, color, zbuffer, x0, y, z)
            y = y + 1
            z = z + dz
    elif dy == 0:
        x = x0
        while x <= x1:
            plot(screen, color, zbuffer, x, y0, z)
            x = x + 1
            z = z + dz
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, zbuffer, x, y, z)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            z = z + dz
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, zbuffer, x, y, z)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            z = z + dz
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, zbuffer, x, y, z)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            z = z + dz
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, zbuffer, x, y, z)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            z = z + dz
            d = d + dx

