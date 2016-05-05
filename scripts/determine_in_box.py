import numpy as np

received = np.loadtxt('received_symbols').view(complex).reshape(-1)
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)

openBoxFingerprint = np.loadtxt('openbox_2khz_fingerprint').view(complex).reshape(-1)
closedBoxFingerprint = np.loadtxt('closedbox_2khz_fingerprint').view(complex).reshape(-1)

openBoxTotal = sum(np.abs(received - openBoxFingerprint))
closedBoxTotal = sum(np.abs(received - closedBoxFingerprint))

print 'openBox = '
print openBoxTotal
print 'closedBox = '
print closedBoxTotal