#   csdl - Cross Stitched Spectral Density
#   Copyright (C) 2017 Robert Jordens <jordens@gmail.com>

from __future__ import (absolute_import, division, unicode_literals,
        print_function)

from csdl import csdl

import numpy as np
import matplotlib.pyplot as plt


def main():
    n = 1000000
    f = np.array([1e-6, 1.])
    y = [np.random.randn(n).astype(np.complex64)/2**.5]
    for i in range(2):
        y = [np.cumsum(y[0])*2*np.pi] + y + [np.r_[0, np.diff(y[-1])/2/np.pi]]
    for i in range(6):
        m = np.sin(.3*10**-i*2*np.pi*np.arange(n))/10.
        for j, yi in enumerate(y):
            yi[:] += 10**((2 - j)*i)*m

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_ylim(-160, 160)
    ax.set_xlim(*f)
    ax.grid(True, "major", linestyle="-", alpha=.2)
    ax.grid(True, "minor", linestyle=":", alpha=.2)
    ax.set_xscale("log")
    kwargs = dict(Fs=1., scale_by_freq=True)
    for i, yi in enumerate(y):
        ci = "rgbkc"[i]
        i -= 2
        ax.psd(yi, NFFT=1 << 14, label=str(i), color=ci, linestyle="-",
               alpha=.4, sides="onesided",
               detrend="linear", **kwargs)
        ax.plot(f, 20*np.log10(f**i), color=ci, linestyle="--")
        fl, yl = csdl(yi, yi, detrend_func=plt.mlab.detrend_linear,
                **kwargs)
        ax.plot(fl, 10*np.log10(yl.real), color=ci, linestyle="-", marker=".")
    ax.legend(loc="best")
    fig.savefig("csdl.png")
    plt.show()


if __name__ == "__main__":
    main()
