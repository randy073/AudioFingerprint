import numpy as np
import sys

fingerprintFname = sys.argv[1] #get name of fingerprint file


received = np.loadtxt('received_symbols').view(complex).reshape(-1)
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)
fingerprint = received/sent;

print 'received = '
print fingerprint


oldFingerprint = np.loadtxt(fingerprintFname, skiprows = 1).view(complex).reshape(-1)
print 'oldFingerprint = '
print oldFingerprint

numOfFingerprints = 0

with open(fingerprintFname, 'r') as f:
	firstLine = f.readline()
	firstLine = firstLine.strip()
	firstLine = firstLine.translate(None, '#')
	if firstLine:
		numOfFingerprints = int(firstLine)

numOfFingerprints += 1
print 'numOfFingerprints = '
print numOfFingerprints
print '\n'

receivedReal = fingerprint.real
oldReal = oldFingerprint.real
newReal = (oldReal * (numOfFingerprints-1) + receivedReal)/numOfFingerprints

receivedImag = fingerprint.imag
oldImg = oldFingerprint.imag
newImg = (oldImg* (numOfFingerprints-1) + receivedImag)/numOfFingerprints

newFingerprint = np.vectorize(complex)(newReal, newImg)

print 'newFingerprint = '
print newFingerprint





np.savetxt(fingerprintFname , newFingerprint.view(float).reshape(-1, 2), header=str(numOfFingerprints))