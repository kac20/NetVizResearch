def parseLayoutCoords(filename):
    coords = {}
    file = open(filename, 'r')
    for line in file.readlines():
        [id, x, y]=line.strip().split()
        coords[id] = (x,y)
    return coords

print(parseLayoutCoords("layoutCoords_test.txt"))