#!/usr/bin/env python
import argparse
import os
import os.path
import time
import numpy as np
from math import radians, pi, cos, sin, atan, exp, dist
from scipy.cluster.hierarchy import linkage, fcluster

'''
This file is the counterpart of the Python implementation of the MRF-based triangulation procedure introduced in
"Automatic Discovery and Geotagging of Objects from Street View Imagery"
by V. A. Krylov, E. Kenny, R. Dahyot.
https://arxiv.org/abs/1708.08417 to remove all geospatial coordinate transformations aimed at verifying the accuracy 
of the approach and its sensitivity to the input variations and hard coded parameters. 

version 1.1
Copyright (c) ADAPT centre, Trinity College Dublin, 2018

The module performs triangulation, MRF optimization to establish the optimal object configuration and clustering.
'''

###########################################
#  I N P U T     P A R A M E T E R S      #
###########################################

# preset parameters
MaxObjectDstFromCam = 25  # Max distance from camera to objects (in meters)
MaxDstInCluster = 1  # Maximal size of clusters employed (in meters)

# MRF optimization parameters
ICMiterations = 15		# Number of iterations for ICM
DepthWeight = 0.2		# weight alpha in Eq.(4)
ObjectMultiView = 0.2		# weight beta in  Eq.(4)
StandAlonePrice = max(1 - DepthWeight - ObjectMultiView, 0)  # weight (1-alpha-beta) in Eq. (4)

###########################################


# conversion from meters to (lat,lon)
def MetersToLatLon(mx, my):
    # Converts XY point from Spherical Mercator EPSG:4326 to lat/lon in WGS84 Datum
    originShift = 2 * pi * 6378137 / 2.0
    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0
    lat = 180 / pi * (2 * atan(exp(lat * pi / 180.0)) - pi / 2.0)
    return lat, lon


# calculating the intersection  point between two rays (specified each by camera position and depth-estimated object
# location). Refer to https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection where u = y, t = x
def Intersect(Object1, Object2):
    latC1 = Object1[5]
    latC2 = Object2[5]
    lonC1 = Object1[6]
    lonC2 = Object2[6]
    # normalized object lat/lon which does not take into account input depth
    latP1 = Object1[0]
    latP2 = Object2[0]
    lonP1 = Object1[1]
    lonP2 = Object2[1]
    print(latC1, lonC1, latP1, lonP1, latC2, lonC2, latP2, lonP2, flush=True)
    a1 = latP1 - latC1
    b1 = latP2 - latC2
    c1 = latC2 - latC1

    a2 = lonP1 - lonC1
    b2 = lonP2 - lonC2
    c2 = lonC2 - lonC1

    d = a2*b1-b2*a1
    if d:
        y = (a1*c2 - a2*c1) / d
    else:
        return -1, -1, 0, 0
    if a1 != 0:
        x = (b1*y+c1) / a1
    else:
        x = (b2*y+c2) / a2

    if (x < 0) or (y < 0):
        return -2, -2, 0, 0
    if (x > MaxObjectDstFromCam) or (y > MaxObjectDstFromCam):
        return -3, -3, 0, 0
    mx, my = a1*x+latC1, a2*x+lonC1
    # x and y are the distances of intersection to cameras C1 and C2, respectively,
    # and mx, my are (x, y) coordinate of intersection
    return x, y, mx, my


# calculate the MRF energy of an intersection
def CalcEnergyObject(ObjectsDst, ObjectsBase, ObjectsConnectivity, Object):
    inters = np.count_nonzero(ObjectsConnectivity[Object, :])
    if inters == 0:
        # increase energy if the view ray object has no intersection with other view ray objects
        return StandAlonePrice
    Energy = 0
    dpthmin, dpthmax = 1000, 0
    for i in range(len(ObjectsBase)):
        if ObjectsConnectivity[Object, i]:
            # increase energy by penalizing distance between triangulated distance and depth estimate
            dpthPen = DepthWeight*abs(ObjectsDst[Object, i] - (ObjectsBase[Object])[3])
            Energy += dpthPen
            dpth = ObjectsDst[Object, i]
            if dpth < dpthmin:
                dpthmin = dpth
            if dpth > dpthmax:
                dpthmax = dpth
    # increase energy by penalizing excessive spread for an object with multiple view ray intersections
    return Energy + ObjectMultiView*(dpthmax-dpthmin)


# calculate the averaged object location (used after clustering)
def CalcAvrgObject(Intersects, ObjectsConnectivity, Object):
    res = np.zeros(2)
    cnt = 0
    for i in range(Intersects.shape[0]):
        if ObjectsConnectivity[Object, i]:
            res[:] += Intersects[Object, i, :]
            cnt += 1
    if cnt:
        return res/cnt
    return res


# hierarchical clustering
def MyClust(intersects, MaxIntraDegreeDst):
    Z = linkage(np.asarray(intersects))
    clusters = fcluster(Z, MaxIntraDegreeDst, criterion='distance') - 1
    NumClusters = max(clusters) + 1
    IntersectClusters = np.zeros((NumClusters, 3))
    for i in range(len(intersects)):
        IntersectClusters[clusters[i], 0] += (intersects[i])[0]
        IntersectClusters[clusters[i], 1] += (intersects[i])[1]
        IntersectClusters[clusters[i], 2] += 1
    return IntersectClusters


# only PAIRWISE intersections
def main(inputfilename, outputfilename):
    start = time.time()
    ObjectsBase = []

    if not os.path.isfile(inputfilename):
        print('Input file not found. Aborting.')
        return

    if os.path.isfile(outputfilename):
        os.remove(outputfilename)

    try:
        f1 = open(outputfilename, 'w')
        f1.close()
    except Exception as ex:
        print(f'A file with the specified ouput name cannot be created. Aborting. {ex}')
        return

    ###############################
    # A L L  O B J E C T S        #
    ###############################
    with open(inputfilename, 'r') as f:
        next(f)	 # skip the first line
        for line in f:
            nums = line.split(',')
            if len(nums) < 3:
                print('Broken entry ignored')
            if len(nums) < 4:  # if a depth estimate is not available
                mx, my, bearing, depth = float(nums[0]), float(nums[1]), float(nums[2]), 5
            else:
                mx, my, bearing, depth = float(nums[0]), float(nums[1]), float(nums[2]), float(nums[3])
            if depth <= 0:
                depth = 5

            # calculating the object positions from camera position + bearing + depth_estimate
            br1 = radians(bearing)
            yCP = my + depth * cos(br1)  # depth-based positions
            xCP = mx + depth * sin(br1)
            yCP1 = my + 1.0 * cos(br1)	 # normalized positions (at 1m distance from camera)
            xCP1 = mx + 1.0 * sin(br1)
            ObjectsBase.append((xCP1, yCP1, bearing, depth, 0, mx, my, xCP, yCP))

    print("All detected objects: {0:d}".format(len(ObjectsBase)))

    #############################
    # A D M I S S I B L E       #
    #############################

    # the maximal distance between the two camera positions observing the same object
    MaxCamDst = 1.5 * MaxObjectDstFromCam

    NumIntersects = 0
    ObjectsDst = np.zeros((len(ObjectsBase), len(ObjectsBase)))
    Intersects = np.zeros((len(ObjectsBase), len(ObjectsBase), 2))
    for i in range(len(ObjectsBase)):
        if i % 1000 == 0 and i > 0:
            print('Parsed {} object entries ({:.2f}%)'.format(i, 100. * i / len(ObjectsBase)))
        ObjectsDst[i, i] = -5
        for j in range(i+1, len(ObjectsBase)):
            c1_y = ObjectsBase[i][6]
            c1_x = ObjectsBase[i][5]
            c2_y = ObjectsBase[j][6]
            c2_x = ObjectsBase[j][5]
            CamDstMtrs = dist([c1_x, c1_y], [c2_x, c2_y])

            # cam_positions - same (less than 1m apart) or too far
            if CamDstMtrs < 0.5 or CamDstMtrs > MaxCamDst:
                ObjectsDst[i, j] = -4
                ObjectsDst[j, i] = -4
                continue
            ObjectsDst[i, j], ObjectsDst[j, i], Intersects[i, j, 0], Intersects[i, j, 1] = Intersect(ObjectsBase[i],
                                                                                                     ObjectsBase[j])
            Intersects[j, i, 0], Intersects[j, i, 1] = Intersects[i, j, 0], Intersects[i, j, 1]
            print(i, j, ObjectsDst[i, j], ObjectsDst[j, i], Intersects[i, j, 0], Intersects[i, j, 1])
            if ObjectsDst[i, j] > 0:
                NumIntersects += 1

    print("All admissible intersections: {0:d}".format(NumIntersects))
    print(f"Intersects: {Intersects}", flush=True)

    ObjectsConnectivity = np.zeros((len(ObjectsBase), len(ObjectsBase)), dtype=np.uint8)
    ObjectsConnectivityViableOptions = np.zeros(len(ObjectsBase), dtype=np.uint8)
    for i in range(len(ObjectsBase)):
        ObjectsConnectivityViableOptions[i] = np.count_nonzero(ObjectsDst[i, :] > 0)
    print(ObjectsConnectivityViableOptions)

    #############################
    #           I C M           #
    #############################

    np.random.seed(int(100000.0 * time.time()) % 1000000000)
    chngcnt = 0
    for ICMiter in range(ICMiterations * len(ObjectsBase)):
        if (ICMiter+1) % (len(ObjectsBase)) == 0:
            print('Iteration #{}: accepted {} changes'.format((ICMiter + 1) / (len(ObjectsBase)), chngcnt))
            chngcnt = 0
        # randomly select a viable pair of intersections testObject <-> testObjectPair
        testObject = np.random.randint(0, len(ObjectsBase))
        if ObjectsConnectivityViableOptions[testObject] == 0:  # no pairing possible (standalone - )
            print(f'{testObject} is standalone with no pairings', flush=True)
            continue

        randnum = 1 + np.random.randint(0, ObjectsConnectivityViableOptions[testObject])
        curcnt = 0
        testObjectPair = 0
        for i in range(len(ObjectsBase)):
            if ObjectsDst[testObject, i] > 0:
                curcnt += 1
            if curcnt == randnum:
                testObjectPair = i
                break

        EnergyOld = CalcEnergyObject(ObjectsDst, ObjectsBase, ObjectsConnectivity, testObject)
        EnergyOld += CalcEnergyObject(ObjectsDst, ObjectsBase, ObjectsConnectivity, testObjectPair)
        ObjectsConnectivity[testObject, testObjectPair] = 1 - ObjectsConnectivity[testObject, testObjectPair]
        ObjectsConnectivity[testObjectPair, testObject] = 1 - ObjectsConnectivity[testObjectPair, testObject]
        EnergyNew = CalcEnergyObject(ObjectsDst, ObjectsBase, ObjectsConnectivity, testObject)
        EnergyNew += CalcEnergyObject(ObjectsDst, ObjectsBase, ObjectsConnectivity, testObjectPair)
        print(f'EnergyOld: {EnergyOld}, EnergyNew: {EnergyNew}')
        if EnergyNew <= EnergyOld:
            # keep the connection between testObject and testObjectPair for this iteration
            chngcnt += 1
            print(f'keep the connection {testObject}-{testObjectPair}, energy: {EnergyNew}', flush=True)
            continue

        # revert to the old configuration
        ObjectsConnectivity[testObject, testObjectPair] = 1 - ObjectsConnectivity[testObject, testObjectPair]
        ObjectsConnectivity[testObjectPair, testObject] = 1 - ObjectsConnectivity[testObjectPair, testObject]
    #############################
    #    C L U S T E R I N G    #
    #############################
    mx, my = (ObjectsBase[0])[0], (ObjectsBase[0])[1]
    # cos(45) and sin(45) are all equal to 0.707, so d45 is the projected distance of MaxDisInCluster to x and y
    d45 = 0.707 * MaxDstInCluster
    ax, ay = mx + d45, my + d45
    ax1, ay1 = mx, my
    MaxDegreeDstInCluster = ((ax - ax1) ** 2 + (ay - ay1) ** 2) ** 0.5
    print(MaxDegreeDstInCluster)

    ICMintersect = []
    ifObjectIntersects = np.zeros(len(ObjectsBase), dtype=np.uint8)
    for i in range(len(ObjectsBase)):
        res = CalcAvrgObject(Intersects, ObjectsConnectivity, i)
        print(f'{i}: {res}', flush=True)
        if res[0]:
            ifObjectIntersects[i] = 1
            ICMintersect.append((res[0], res[1]))

    print("ICM inrersections: {0:d}".format(len(ICMintersect)))
    print(ICMintersect)
    IntersectClusters = MyClust(ICMintersect, MaxDegreeDstInCluster)
    print(IntersectClusters)
    NumClusters = IntersectClusters.shape[0]
    with open(outputfilename, "w") as inter:
        inter.write("X,Y,score\n")
        for i in range(NumClusters):
            inter.write("{0:f},{1:f},{2:d}\n".format(IntersectClusters[i, 0]/IntersectClusters[i, 2],
                                                     IntersectClusters[i, 1]/IntersectClusters[i, 2],
                                                     int(IntersectClusters[i, 2])))
    print("Number of output ICM clusters: {0:d}".format(NumClusters))

    print("Elapsed total time: {0:.2f} seconds.".format(time.time() - start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--inputfilename', type=str, default='data/pole_input.csv', help='input file name with path')
    parser.add_argument('--outputfilename', type=str, default='data/pole_detection.csv',
                        help='output file name with path')

    args = parser.parse_args()
    inputfilename = args.inputfilename
    outputfilename = args.outputfilename
    main(inputfilename, outputfilename)
