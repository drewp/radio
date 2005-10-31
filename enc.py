#!/usr/bin/env python
'''An example of encoding using the Python wave module'''
from __future__ import division
import ogg.vorbis, wave

        

import popen2
(child_stdout,child_stdin) = popen2.popen2("rec -c 2 -r 44100 -t wav -")

inwav = wave.open(child_stdout,'r')


secs_in_this_file = 0
file_serial = 0
while 1:
    fout = open('/my/music/radio/spool/105.3fm/out.%d.ogg' % file_serial, 'w')

    vd = ogg.vorbis.VorbisInfo(channels = 2,
                               rate = 44100,
                               quality = 0.0).analysis_init()
    os = ogg.OggStreamState(5)
    map(os.packetin, vd.headerout())
    og = os.flush()
    while og:
        og.writeout(fout)
        og = os.flush()
    nsamples = 1024


    eos = 0
    total = 0
    while not eos:
        data = inwav.readframes(nsamples)
        total = total + nsamples
        if not data:
            vd.write(None)
            break
        vd.write_wav(data)

        vb = vd.blockout()
        while vb:
            vb.analysis()
            vb.addblock()

            op = vd.bitrate_flushpacket()
            while op:
                os.packetin(op)
                while not eos:
                    og = os.pageout()
                    if not og: break
                    og.writeout(fout)
                    eos = og.eos()
                op = vd.bitrate_flushpacket()
            vb = vd.blockout()
        secs_in_this_file += nsamples / 44100
        if secs_in_this_file > 5*60:
            eos=1
            secs_in_this_file = 0
            file_serial += 1
            break
        
