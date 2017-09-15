#   csdl - Cross Stitched Spectral Density
#   Copyright (C) 2017 Robert Jordens <jordens@gmail.com>

from __future__ import (absolute_import, division, unicode_literals,
        print_function)
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def csdl(x, y, n=128, b=10, m=4, Fs=2., cut=.8, **kwargs):
    """
    Cross Stitched Spectral Density

    To cover large frequency spans the fft is performed with `n` bins
    for each `b` factor in frequency. In total there `m` ffts are
    stitched together. Always onesided, even for complex data.

    x, y: samples, real or complex, can be the same array (for psd)
    n: fft block size
    b: block scaling nyquist for the `i`-th block is `Fs/2*b**-i`
    m: number of fft blocks (the lowest frequency bin will be at
        `Fs/n*b**-(m - 1)`)
    cut: crossover point, crossover from the i-th to the i+1-th block
        happens at Fs/2*b**-(i + 1)*cut; the downsampling betwen blocks is
        performed using an 8th order Chebychev (I) filter with 0.1 dB ripple
    kwargs: passed to plt.mlab._spectral_helper()

    caveats:
        * the fft bin width (resolution) changes between blocks
        * if `scale_by_freq=True`, (1/Hz power spectral density)
          narrow signals go down by `b` per segment in power and
          noise remains at the same level between blocks
        * if `scale_by_freq=False` (absolute power), noise goes down by `b`
          per segment and narrow signals remain at the same level
    """
    x = np.asarray(x)
    f = []
    z = []
    fl = int(np.ceil(n/2./b*cut))
    fr = int(np.ceil(n/2.*cut))
    db, da = signal.cheby1(8, .1, cut/b)  # 8th order cheby1 .1dB ripple
    for i in range(m):
        zi, fi, t = plt.mlab._spectral_helper(x, y, NFFT=n, Fs=Fs*b**-i,
                                              sides="onesided", **kwargs)
        zi = zi.mean(1)
        if i > 0:
            zi, fi = zi[:fr], fi[:fr]
        if i < m - 1:
            zi, fi = zi[fl:], fi[fl:]
            x1 = signal.lfilter(db, da, x)[::b]
            if y is x:
                y = x1
            else:
                y = signal.lfilter(db, da, y)[::b]
            x = x1
        z.insert(0, zi)
        f.insert(0, fi)
    f, z = np.concatenate(f), np.concatenate(z)
    assert min(f) == f[0]
    assert f[1] == Fs/n*b**-(m - 1)
    return f, z
