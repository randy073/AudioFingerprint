import numpy as np

import sys
import os



numFrenquencies = int(sys.argv[1])
material = sys.argv[2]

frequencies = []

for i in range(numFrenquencies):
	frequencies.append(sys.argv[i+3])




received = []
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)
fingerprints = []
cardboardtop = []
cardboardRaised = []
openwithoutbox = []
wood = []
metal = []
plastic = []
for i in range(numFrenquencies):
	received.append(np.loadtxt('received_symbols'+str(frequencies[i])).view(complex).reshape(-1))
	fingerprints.append(received[i]/sent)

	cardboardtop.append(np.loadtxt('cardboardtop_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))
	cardboardRaised.append(np.loadtxt('cardboardraised_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))
	openwithoutbox.append(np.loadtxt('openwithoutbox_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))
	wood.append(np.loadtxt('wood_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))
	metal.append(np.loadtxt('claypyramid_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))
	plastic.append(np.loadtxt('plastic_'+str(frequencies[i]) + 'khz_16qam_fingerprint_long').view(complex).reshape(-1))






cardboardPoints = 0
cardboardRaisedPoints = 0
openPoints = 0
woodPoints = 0
metalPoints = 0
plasticPoints = 0

for j in range(len(frequencies)):
	for i in range(sent.size):
		cardboardRealDiff = np.square(fingerprints[j].real[i] - cardboardtop[j].real[i])
		cardboardImagDiff = np.square(fingerprints[j].imag[i] - cardboardtop[j].imag[i])
		cardboardDist = np.sqrt(cardboardRealDiff + cardboardImagDiff)

		cardboardRaisedRealDiff = np.square(fingerprints[j].real[i] - cardboardRaised[j].real[i])
		cardboardRaisedImagDiff = np.square(fingerprints[j].imag[i] - cardboardRaised[j].imag[i])
		cardboardRaisedDist = np.sqrt(cardboardRaisedRealDiff + cardboardRaisedImagDiff)

		openRealDiff = np.square(fingerprints[j].real[i] - openwithoutbox[j].real[i])
		openImagDiff = np.square(fingerprints[j].imag[i] - openwithoutbox[j].imag[i])
		openDist = np.sqrt(openRealDiff + openImagDiff)

		woodRealDiff = np.square(fingerprints[j].real[i] - wood[j].real[i])
		woodImagDiff = np.square(fingerprints[j].imag[i] - wood[j].imag[i])
		woodDist = np.sqrt(woodRealDiff + woodImagDiff)

		metalRealDiff = np.square(fingerprints[j].real[i] - metal[j].real[i])
		metalImagDiff = np.square(fingerprints[j].imag[i] - metal[j].imag[i])
		metalDist = np.sqrt(metalRealDiff + metalImagDiff)

		plasticRealDiff = np.square(fingerprints[j].real[i] - plastic[j].real[i])
		plasticImagDiff = np.square(fingerprints[j].imag[i] - plastic[j].imag[i])
		plasticDist = np.sqrt(plasticRealDiff + plasticImagDiff)

		
		minDist = min(cardboardDist, openDist, woodDist, metalDist, cardboardRaisedDist)
		if(minDist == cardboardDist):
			cardboardPoints += 1
		elif(minDist == openDist):
			openPoints += 1
		elif(minDist == woodDist):
			woodPoints += 1
		elif(minDist == metalDist):
			metalPoints += 1
		elif(minDist == plasticDist):
			plasticPoints += 1
		elif(minDist == cardboardRaisedDist):
			cardboardRaisedPoints += 1

total = float(cardboardPoints + openPoints + woodPoints + metalPoints + plasticPoints + cardboardRaisedPoints)

plasticCorrelate = np.correlate(plastic[0],received[0])
cardboardCorrelate = np.correlate(cardboardtop[0],received[0])

print 'plastic correlation'
print plasticCorrelate
print 'cardbaord correlation'
print cardboardCorrelate
print 'metal correlation'
print np.correlate(metal[0],received[0])
print 'wood correlation'
print np.correlate(wood[0],received[0])
print 'open correlation'
print np.correlate(openwithoutbox[0],received[0])

print 'cardboard points = '
print cardboardPoints
print float(cardboardPoints)/total

print 'cardboardRaisedPoints = '
print cardboardRaisedPoints
print float(cardboardRaisedPoints)/total

print 'openPoints = '
print openPoints
print float(openPoints)/total

print 'clayflatPoints = '
print woodPoints

print float(woodPoints)/total
print 'metalPoints = '
print metalPoints
print float(metalPoints)/total

print 'plasticPoints = '
print plasticPoints
print float(plasticPoints)/total


maxPoints = max(cardboardPoints,openPoints, woodPoints, metalPoints, plasticPoints, cardboardRaisedPoints)

if(maxPoints == cardboardPoints):
	os.system("say 'cardboard low'")
	guess = 'cardboardlow'
elif(maxPoints == openPoints):
	os.system("say 'open top'")
	guess = 'opentop'
elif(maxPoints == woodPoints):
	os.system("say 'clay flat'")
	guess = 'clayflat'
elif(maxPoints == metalPoints):
	os.system("say 'clay pyramid'")
	guess = 'claypyramid'
elif(maxPoints == plasticPoints):
	os.system("say 'plastic'")
elif(maxPoints == cardboardRaisedPoints):
	os.system("say 'cardboard raised'")
	guess = 'cardboardraised'

print 'guess ='
print guess
print 'material - '
print material

writeFile = open('shapeData.csv','a')
writeFile.write(material)
writeFile.write(', ')
writeFile.write(guess)
writeFile.write(', ')
writeFile.write(str(cardboardPoints))
writeFile.write(', ')
writeFile.write(str(cardboardRaisedPoints))
writeFile.write(', ')
writeFile.write(str(woodPoints)) #clay flat
writeFile.write(', ')
writeFile.write(str(metalPoints)) #clay pyramid
writeFile.write(', ')
writeFile.write(str(openPoints))
writeFile.write('\r\n')

