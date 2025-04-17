def project(p, width, height, fov, viewer_dist):
    factor = fov / (viewer_dist + p[2])
    x = p[0]*factor + width/2
    y = -p[1]*factor + height/2
    return (x,y)