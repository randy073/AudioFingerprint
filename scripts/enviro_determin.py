import numpy as np

import sys

fingerprintFname1 = sys.argv[1]
fingerprintFname2 = sys.argv[2]

received = np.loadtxt('received_symbols').view(complex).reshape(-1)
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)

fingerprint = received/sent

openBoxFingerprint = np.loadtxt(fingerprintFname1).view(complex).reshape(-1)
closedBoxFingerprint = np.loadtxt(fingerprintFname2).view(complex).reshape(-1)

openPoints = 0
closedPoints = 0

for i in range(received.size):
	openRealDiff = np.square(fingerprint.real[i] - openBoxFingerprint.real[i])
	openImagDiff = np.square(fingerprint.imag[i] - openBoxFingerprint.imag[i])
	openDist = np.sqrt(openRealDiff + openImagDiff)

	closedRealDiff = np.square(fingerprint.real[i] - closedBoxFingerprint.real[i])
	closedImagDiff = np.square(fingerprint.imag[i] - closedBoxFingerprint.imag[i])
	closedDist = np.sqrt(closedRealDiff + closedImagDiff)

	if(openDist < closedDist):
		openPoints += 1
	else:
		closedPoints += 1



openBoxTotal = sum(np.abs(fingerprint - openBoxFingerprint))
closedBoxTotal = sum(np.abs(fingerprint - closedBoxFingerprint))

print 'Environment 1 = '
print openBoxTotal
print 'Environment 2 = '
print closedBoxTotal

print 'First enviro points = '
print openPoints
print 'Second enviro points = '
print closedPoints

# if(openBoxTotal > closedBoxTotal):
# 	print "It's a closed box!!!"
# else:
# 	print "It's a open box!!!"