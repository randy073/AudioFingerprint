import numpy as np

received = np.loadtxt('received_symbols').view(complex).reshape(-1)
sent = np.loadtxt('symbols_sent').view(complex).reshape(-1)
fingerprint = received/sent;




np.savetxt('openbox_2khz_fingerprint' , fingerprint.view(float).reshape(-1, 2))