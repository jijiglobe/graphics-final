def calculate_normal( ax, ay, az, bx, by, bz ):
    normal = [0,0,0]
    normal[0] = ay * bz - az * by
    normal[1] = az * bx - ax * bz
    normal[2] = ax * by - ay * bx
    return normal

def calculate_dot( points, i ):
    #get as and bs to calculate the normal
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )

    #set up the view vector values
    vx = 0
    vy = 0
    vz = -1
    
    #calculate the dot product
    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz
    
    return dot

def calculate_flat( points, i, source):
    #get as and bs to calculate the normal
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )
    normalMag = (normal[0] ** 2 + normal[1] ** 2 + normal[2]) ** .5
    
    #set up the specular vector values
    vx = points[i][0] - source[0]
    vy = points[i][1] - source[1]
    vz = points[i][2] - source[2]
    specularMag = (vx ** 2 + vy ** 2 + vz ** 2) ** .5
    
    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz
    divisor = specularMag * normalMag
    
    diffuse = dot / divisor
    
    #normalize normal
    normal[0] = normal[0]/normalMag
    normal[1] = normal[1]/normalMag
    normal[2] = normal[2]/normalMag
    nmag = (normal[0] ** 2 + normal[1] ** 2 + normal[2]) ** .5

    #normalize specular vector
    vx = vx/specularMag
    vy = vy/specularMag
    vz = vz/specularMag
    specularMag = (vx ** 2 + vy ** 2 + vz ** 2) ** .5


    ndot = normal[0] * vx + normal[1] * vy + normal[2] * vz

    reflection = [vx - 2 * ndot * normal[0],
                  vy - 2 * ndot * normal[1],
                  vz - 2 * ndot * normal[2]]

    specdot = reflection[0] * 0 + reflection[1] * 0 + reflection[2] * -1
    divisor = normalMag * specularMag * 4
    specular = specdot / divisor
    """if specular > 1:
        specular = 1
    """
    """if specular < 0:
        specular = 0
    if diffuse < 0:
        diffuse = 0
    print diffuse + specular"""
    ans = (diffuse + specular) / 2
    if ans < 1:
        return ans
    else:
        return 1

def perspective_induce(points, p):
    #this doesn't work
    pass
"""    for x in range(3):
        #translate to the origin
        print "original: "+str(points[p+x])
        points[p+x][0] -= 250
        points[p+x][1] -= 250
        #induce perspective
        points[p+x][0] /= points[p+x][2] *.01
        points[p+x][1] /= points[p+x][2] *.01
        #translate back
        points[p+x][0] += 250
        points[p+x][1] += 250
        #convert to int
        points[p+x][0] = int(points[p+x][0])
        points[p+x][1] = int(points[p+x][1])
        print "new:    : "+str(points[p+x])
"""
