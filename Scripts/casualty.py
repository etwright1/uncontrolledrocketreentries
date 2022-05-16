#
# From norabolig (A. Boley)
# Modifed by etwright1
#
import KeplerTools as KT
import numpy as np
RE=6378e3 # equatorial radius

def latWeights(dlat,a,inc,NNU=10000,m0=5.97e24,PLOT=False):
  ''' give dlat [deg], a in [m] and inc in [deg]'''

  twopi = np.pi*2
  nu = np.linspace(0,twopi,NNU,endpoint=False)
  inc = inc *twopi/360
  m1 = 0.
  ecc =0.
  Omega =0.
  w = 0.

  dlat = 0.5 #degrees
  nlat = int(180/dlat)
  vals = np.zeros(nlat)
  lats = 90-np.linspace(dlat/2,180-dlat/2,nlat,endpoint=True)


  for f in nu:
     X,Y,Z,VX,VY,VZ = KT.getXYZVVV(f,a,w,ecc,Omega,inc,m0,m1)
     rad = np.sqrt(X*X+Y*Y)
     r = np.sqrt(X*X+Y*Y+Z*Z)
     colat = np.arccos(Z/r)
     lat = (np.pi*0.5-colat)*360/twopi
     ilat = min(int( (90-lat)/dlat ),nlat-1)
     vals[ilat]+=1

  sum = np.sum(vals)
  vals = vals/NNU
  
  if PLOT:
    ana=np.zeros(len(lats))
    dlat_rad=dlat*twopi/360
    for i in range(len(lats)):
      print(lats[i],inc*360/twopi)
      if abs(lats[i]) <=inc*360/twopi:
        if abs(abs(lats[i])-inc*360/twopi) < 1e-9:
           s = 1
           if lats[i]<0: s=-1
           ana[i]=max(np.cos((lats[i]-s*dlat*7/16)*twopi/360)/(np.pi*(np.sin(inc)**2-np.sin((lats[i]-s*dlat*7/16)*twopi/360)**2)**0.5),0)*dlat_rad/8
           ana[i]+=max(np.cos((lats[i]-s*dlat*5/16)*twopi/360)/(np.pi*(np.sin(inc)**2-np.sin((lats[i]-s*dlat*5/16)*twopi/360)**2)**0.5),0)*dlat_rad/8
           ana[i]+=max(np.cos((lats[i]-s*dlat*3/16)*twopi/360)/(np.pi*(np.sin(inc)**2-np.sin((lats[i]-s*dlat*3/16)*twopi/360)**2)**0.5),0)*dlat_rad/8
           ana[i]+=max(np.cos((lats[i]-s*dlat*1/16)*twopi/360)/(np.pi*(np.sin(inc)**2-np.sin((lats[i]-s*dlat*1/16)*twopi/360)**2)**0.5),0)*dlat_rad/8
        else: ana[i] = max(np.cos(lats[i]*twopi/360)/(np.pi*(np.sin(inc)**2-np.sin(lats[i]*twopi/360)**2)**0.5),0)*dlat_rad

    import matplotlib.pylab as plt
    plt.figure()
    plt.plot(lats,vals)
    plt.plot(lats,ana)
    plt.ylabel("Time Fraction")
    plt.xlabel("Latitude [deg]")
    plt.show()

  return vals,lats


def worldPopulation(NLAT=360,NLON=720,filename="gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev11_2000_30_min.asc",PLOT=False):
  import numpy as np

  fh=open(filename,"r")
  counts=np.zeros((NLAT,NLON))

  twopi=np.pi*2

  ilat=0
  for line in fh:
     if len(line) < 32: continue
     vals=np.array(line.split(" ") )
     counts[ilat,:]=vals[0:-1]
     ilat+=1

  pop=0
  dlat = np.pi/NLAT
  dlon = twopi/NLON
  for ilat in range(NLAT):
     for ilon in range(NLON):
        if counts[ilat,ilon]<0:continue
        pop += counts[ilat,ilon]

  print("Population [Billion]",pop/1e9)

  popPerLat = np.zeros(NLAT)
  for ilat in range(NLAT):
     for ilon in range(NLON):
        if counts[ilat,ilon]<0:continue
        popPerLat[ilat]+=counts[ilat,ilon]

  denPerLat = np.zeros(NLAT)
  totarea=0
  for ilat in range(NLAT):
      area = (twopi * (np.cos(ilat*dlat)-np.cos( (ilat+1)*dlat) ))*RE**2
      totarea+=area
      denPerLat[ilat] =popPerLat[ilat]/area

  print("Santity check: Total area = {} m^2".format(totarea))
  print("Santity check: Total Pop  = {}    ".format(np.sum(popPerLat)))
  

  if PLOT:
    import matplotlib.pylab as plt

    plt.figure()
    plt.contourf(counts)
    plt.gca().invert_yaxis()

    plt.figure()
    plt.title("popPerLat array values")
    plt.plot(popPerLat)
    plt.show()

    plt.figure()
    plt.title("denPerLat array values")
    plt.plot(denPerLat)
    plt.show()

    plt.show()

  return popPerLat,denPerLat,counts

def riskInc(dlat,NLAT=360,NLON=720,NINC=90,filename="gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev11_2000_30_min.asc"):
 
    twopi = np.pi*2
    incs = np.zeros(NINC)
    dinc = np.pi/(2*NINC)
    for i in range(NINC): incs[i] = (i+0.5)*dinc

    popPerLat,denPerLat,counts = worldPopulation(NLAT=NLAT,NLON=NLON,filename=filename)

    riskPerInc = np.zeros(NINC)

    dlat_rad = dlat*twopi/360

   
    a  = 550e3+RE  # this does not really matter, but we pass it anyway
    for i in range(NINC):
        print("Task flow: Working on inc {}".format(incs[i]*360/twopi))
        w,lats=latWeights(dlat=dlat,a=a,inc=incs[i]*360/twopi)
#        for ilat in range(len(lats)):
#          w[ilat] = max(np.cos(lats[ilat]*twopi/360)/(np.pi*(np.sin(incs[i])**2-np.sin(lats[ilat]*twopi/360)**2)**0.5),0)*dlat_rad
 
#DEBUG   import matplotlib.pylab as plt
#        plt.figure()
#        plt.plot(w)
#        plt.figure()
#        plt.plot(popPerLat)
#        plt.figure()
#        plt.plot(w*popPerLat)
#        plt.show()

        sumPop=0.
#        for l in range(len(lats)):
#            if incs[i]*360/twopi > abs(lats[l]): sumPop+=popPerLat[l]*w[l]
          
        riskPerInc[i]=np.sum(w*denPerLat)

    import matplotlib.pylab as plt
    plt.figure()
    plt.plot(incs*360/twopi,riskPerInc)
    plt.show()    
