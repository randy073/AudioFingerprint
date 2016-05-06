import numpy as np
import sys

fingerprintFname = sys.argv[1]

received = np.loadtxt('received_symbols').view(complex).reshape(-1)
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)
fingerprint = received/sent;
print type(fingerprint)




np.savetxt(fingerprintFname, fingerprint.view(float).reshape(-1, 2), header='1')