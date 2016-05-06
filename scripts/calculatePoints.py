import numpy as np

import sys

numFrenquencies = int(sys.argv[1])

frequencies = []

for i in range(numFrenquencies):
	frequencies.append(sys.argv[i+2])


received = []
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)
fingerprints = []
cardboardtop = []
openwithoutbox = []
clayflattop = []
for i in range(numFrenquencies):
	received.append(np.loadtxt('received_symbols'+str(frequencies[i])).view(complex).reshape(-1))
	fingerprints.append(received[i]/sent)

	cardboardtop.append(np.loadtxt('cardboardtop_'+str(frequencies[i]) + 'khz_16qam_fingerprint').view(complex).reshape(-1))
	openwithoutbox.append(np.loadtxt('openwithoutbox_'+str(frequencies[i]) + 'khz_16qam_fingerprint').view(complex).reshape(-1))
	clayflattop.append(np.loadtxt('clayflattop_'+str(frequencies[i]) + 'khz_16qam_fingerprint').view(complex).reshape(-1))






cardboardPoints = 0
openPoints = 0
clayPoints = 0

for j in range(len(frequencies)):
	for i in range(sent.size):
		cardboardRealDiff = np.square(fingerprints[j].real[i] - cardboardtop[j].real[i])
		cardboardImagDiff = np.square(fingerprints[j].imag[i] - cardboardtop[j].imag[i])
		cardboardDist = np.sqrt(cardboardRealDiff + cardboardImagDiff)

		openRealDiff = np.square(fingerprints[j].real[i] - openwithoutbox[j].real[i])
		openImagDiff = np.square(fingerprints[j].imag[i] - openwithoutbox[j].imag[i])
		openDist = np.sqrt(openRealDiff + openImagDiff)

		clayflattopRealDiff = np.square(fingerprints[j].real[i] - clayflattop[j].real[i])
		clayflattopImagDiff = np.square(fingerprints[j].imag[i] - clayflattop[j].imag[i])
		clayflattopDist = np.sqrt(clayflattopRealDiff + clayflattopImagDiff)

		
		minDist = min(cardboardDist, openDist, clayflattopDist)
		if(minDist == clayflattopDist):
			clayPoints += 1
		elif(minDist == openDist):
			openPoints += 1
		else:
			cardboardPoints += 1

total = float(cardboardPoints + openPoints + clayPoints)

print 'cardboard points = '
print cardboardPoints
print float(cardboardPoints)/total
print 'openPoints = '
print openPoints
print float(openPoints)/total
print 'clayPoints = '
print clayPoints
print float(clayPoints)/total

