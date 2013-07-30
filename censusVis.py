import shpUtils
import matplotlib.pyplot as plt

censusfile = "censusdata/t_sf1_p9_ct.csv"
shapefile = "shapefile/nyct2010.shp"

def loadCensusData(censusfile):
	m = {}
	maxPop = 0
	count = 0
	with open(censusfile) as lines:
		for line in lines:
			a = line.split(",")
			pop = int(a[5])
			m[a[2]+a[3]] = pop
			if pop > 1500:
				count += 1
			if pop > maxPop:
				maxPop = pop
	return (m, maxPop)

colours = {0:"#F7FCF0", 1:"#E0F3DB", 2:"#CCEBC5", 3:"#A8DDB5", 4:"#7BCCC4", 5:"#4EB3D3", 6:"#2B8CBE", 7:"#0868AC", 8:"#084081"}
(census, maxPop) = loadCensusData(censusfile)
maxPop = 1500
unit = maxPop/8
# load the shapefile
shpRecords = shpUtils.loadShapefile(shapefile)
	

for i in range(0,len(shpRecords)):
	# x and y are empty lists to be populated with the coords of each geometry.
	x = []
	y = []
	for j in range(0,len(shpRecords[i]['shp_data']['parts'][0]['points'])):
	# This is the number of vertices in the ith geometry.
	# The parts list is [0] as it is singlepart.
		# get x and y coordinates.
		tempx = float(shpRecords[i]['shp_data']['parts'][0]['points'][j]['x'])
		tempy = float(shpRecords[i]['shp_data']['parts'][0]['points'][j]['y'])
		x.append(tempx)
		y.append(tempy) # Populate the lists  

		# Creates a polygon in matplotlib for each geometry in the shapefile
	boroCode = shpRecords[i]["dbf_data"]["BoroCode"]
	ctCode = (shpRecords[i]["dbf_data"]["CT2010"] + "x").strip("0").strip("x")# strip prefix 0 from the string
	boroCTCode = boroCode + ctCode
	pop = census[boroCTCode] #Get population in the cencus tract
	if pop > maxPop:
		pop = maxPop
	colour = colours[pop/unit]
	plt.fill(x, y, fc=colour, ec='0.7', lw=0.1)

#Create legend
p0 = plt.Rectangle((0, 0), 1, 1, fc=colours[0])
p1 = plt.Rectangle((0, 0), 1, 1, fc=colours[1])
p2 = plt.Rectangle((0, 0), 1, 1, fc=colours[2])
p3 = plt.Rectangle((0, 0), 1, 1, fc=colours[3])
p4 = plt.Rectangle((0, 0), 1, 1, fc=colours[4])
p5 = plt.Rectangle((0, 0), 1, 1, fc=colours[5])
p6 = plt.Rectangle((0, 0), 1, 1, fc=colours[6])
p7 = plt.Rectangle((0, 0), 1, 1, fc=colours[7])
p8 = plt.Rectangle((0, 0), 1, 1, fc=colours[8])

plt.legend([p0,p1,p2,p3,p4,p5,p6,p7,p8],\
["0-%d people" %((1*unit-1)),\
"%d-%d people" %(1*unit,(2*unit-1)),\
"%d-%d people" %(2*unit,(3*unit-1)),\
"%d-%d people" %(3*unit,(4*unit-1)),\
"%d-%d people" %(4*unit,(5*unit-1)),\
"%d-%d people" %(5*unit,(6*unit-1)),\
"%d-%d people" %(6*unit,(7*unit-1)),\
"%d-%d people" %(7*unit,(8*unit-1)),\
">%d people" %(8*unit)],\
prop={'size':5}, loc = 4)

plt.title("Where do Asian live in New York City (@KienPham)")
plt.axis('off')
plt.savefig('asian.jpg', format='jpg', dpi=700)
plt.show()
  
