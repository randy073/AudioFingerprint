from . import common
from . import equalizer
from . import dsp

import numpy as np
import logging
import itertools

log = logging.getLogger(__name__)


class Sender(object):
    def __init__(self, fd, config, gain=1.0):
        self.gain = gain
        self.offset = 0
        self.fd = fd
        self.modem = dsp.MODEM(config.symbols)
        self.carriers = config.carriers / config.Nfreq
        self.pilot = config.carriers[config.carrier_index]
        self.silence = np.zeros(equalizer.silence_length * config.Nsym)
        self.iters_per_report = config.baud  # report once per second
        self.padding = [0] * config.bits_per_baud
        self.equalizer = equalizer.Equalizer(config)

    def write(self, sym):
        sym = np.array(sym) * self.gain
        data = common.dumps(sym)
        self.fd.write(data)
        self.offset += len(sym)

    def start(self):
        for value in equalizer.prefix:
            self.write(self.pilot * value)

        symbols = self.equalizer.train_symbols(equalizer.equalizer_length)
        signal = self.equalizer.modulator(symbols)
        self.write(self.silence)
        self.write(signal)
        self.write(self.silence)

    def modulate(self, bits):
        fileName = "symbols_sent"
        writeFile = open(fileName, 'w')
        bits = itertools.chain(bits, self.padding)
        Nfreq = len(self.carriers)
        symbols_iter = common.iterate(self.modem.encode(bits), size=Nfreq)
        for i, symbols in enumerate(symbols_iter, 1):
           # writeFile.write(format(symbols))
            writeFile.write(str(symbols.real))
            writeFile.write(" ")
            writeFile.write(str(symbols.imag))
            writeFile.write("\n")
            self.write(np.dot(symbols, self.carriers))
            if i % self.iters_per_report == 0:
                total_bits = i * Nfreq * self.modem.bits_per_symbol
                log.debug('Sent %10.3f kB', total_bits / 8e3)
