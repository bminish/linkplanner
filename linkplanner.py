#!/usr/bin/python
#
#
# By brendan Minish (bminish@gmail.com) 2014 as a learning excercise
# Licence GPL v3 
# 


import math
import sys

from StringIO import StringIO


class LINK(object):
    """ This is an instance of a wireless link"""
    C = 3e8


    def __init__(self):
        self._frequency = 5825
        self._txpower = 17
        self._feedloss = 1
        self._rxgain = 23
        self._txgain = 23
        self._rxsens = -74
        self._distance = 10
        self._cfactor = 0.5
        self._tfactor = 1.0
#        self._c = 3e8

    def getFrequency(self):
        return self._frequency
    def setFrequency(self, v):
        if v:
            try:
                x = float(v)
                self._frequency = x
            except:
                raise ValueError("Frequency must be in MHz")
        elif not v:
            pass
    frequency = property(getFrequency, setFrequency)

    def getTxpower(self):
        return self._txpower
    def setTxpower(self, v):
        if v:
            try:
                x = float(v)
                self._txpower = x
            except:
                raise ValueError("TX power must be in dBm") 
        elif not v:
            pass
    txpower = property(getTxpower, setTxpower)

    def getFeedloss(self):
        return self._feedloss
    def setFeedloss(self, v):
        if v:
            try:
                x = float(v)
                self._feedloss = x
            except:
                raise ValueError("Feeder Loss must be in dB")
        elif not v:
            pass
    feedloss = property(getFeedloss, setFeedloss)

    def getRxgain(self):
        return self._rxgain
    def setRxgain(self, v):
        if v:
            try:
                x = float(v)
                self._rxgain = x
            except:
                raise ValueError("RX antenna Gain must be in dBi")
        elif not v:
            pass
    rxgain = property(getRxgain, setRxgain)

    def getTxgain(self):
        return self._txgain
    def setTxgain(self, v):
        if v:
            try:
                x = float(v)
                self._txgain = x
            except:
                raise ValueError("TX antenna Gain must be in dBi")
        elif not v:
            pass
    txgain = property(getTxgain, setTxgain)
    
    def getRxsens(self):
        return self._rxsens
    def setRxsens(self, v):
        if v:
            try:
                x = float(v)
                self._rxsens = x
            except:
                raise ValueError("RX Sensitivity must be in dBm")
        elif not v:
            pass
    rxsens = property(getRxsens, setRxsens)

    def getDistance(self):
        return self._distance
    def setDistance(self, v):
        if v:
            try:
                x = float(v)
                self._distance = x
            except:
                raise ValueError("Distance must be In Km")
        elif not v:
            pass
    distance = property(getDistance, setDistance)

    def getCfactor(self):
        return self._cfactor
    def setCfactor(self, v):
        if v:
            try:
                x = float(v)
                if x > 0.09 and x < 0.51:
                    self._cfactor = x
                else:
                    raise ValueError("Climate factor must be between 0.1 (dry) and 0.5 (wet)")
            except:
                raise ValueError("Climate factor must be between 0.1 (dry) and 0.5 (wet)")
        elif not v:
            pass
               
    cfactor = property(getCfactor, setCfactor)

    def getTfactor(self):
        return self._tfactor
    def setTfactor(self, v):
        if v:
            try:
                x = float(v)
                if x > 0.24 and x < 4.01:
                    self._tfactor = x
                else:
                   raise ValueError("Terrain factor between 0.25 (Mountains) and 4 (smooth)")
            except:
                raise ValueError("Terrain factor between 0.25 (Mountains) and 4 (smooth)")
        elif not v:
            pass



    tfactor = property(getTfactor, setTfactor)

    def exportLink(self, f):
        ploss = 10 * math.log10((self.C ** 2) / ((4 * math.pi * self.distance * 1e3 * self.frequency * 1e6) ** 2 ))
        erp = self.txpower + self.txgain - self.feedloss 
        rxsig = erp + ploss + self.rxgain - self.feedloss 
        margin = rxsig - self.rxsens
        avail = ( 1 - 2.5/1e6 * self.cfactor * self.tfactor * self.frequency / 1e3 * (self.distance / 1.6) ** 3 * 10 **( - margin / 10))
        if avail <= 0:
            avail = 0
        outage = (525600 - avail * 525600) / 60

        f.write("ERP in dBm       = %.1f\n" % erp)
        f.write("RSSI in dBm      = %.0f\n" % rxsig)
        f.write("Path loss in dB  = %.0f\n" % ploss)
        f.write("Link Margin  dB  = %.0f\n" % margin)
        f.write("Link Avalability = %.6f\n" % avail)
        f.write("Outage Hours/Yr  = %s\n" % outage)


#testing = link()
#f = StringIO()
#testing.exportLink(f)
#print(f.getvalue())


def doInput(link):
    """ gets the varous input for a link plan and sanity checks """
    gotInput = False
    while not gotInput:

        while True:
            try:
                if link.frequency:
                    prompt = "Frequency [%.0f]Mhz? " % link.frequency
                else:
                    prompt = "Frequency in MHz? "
                link.frequency = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.txpower:
                    prompt = "TX power [%.1f]dBm? " % link.txpower
                else:
                    prompt = "TX power in dBm? "
                link.txpower = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.feedloss:
                    prompt = "Feeder Losses (total) [%.1f]dBm? " % link.feedloss
                else:
                    prompt = "Feeder Losses (total) dBm? "
                link.feedloss = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.rxgain:
                    prompt = "RX Antenna gain [%.1f]dBi? " % link.rxgain
                else:
                    prompt = "RX Antenna gain dBi? "
                link.rxgain = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.txgain:
                    prompt = "TX Antenna gain [%.1f]dBi? " % link.txgain
                else:
                    prompt = "TX Antenna gain dBi? "
                link.txgain = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.rxsens:
                    prompt = "RX Sensitivity [%.1f]dBm? " % link.rxsens
                else:
                    prompt = "RX Sensitivity dBm? "
                link.rxsens = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.distance:
                    prompt = "Link Distance [%.3f]Km? " % link.distance
                else:
                    prompt = "Link Distance in Km? "
                link.distance = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.cfactor:
                    prompt = "Climate factor (0.1 dry) to (0.5 Humid) [%.2f]? " % link.cfactor
                else:
                    prompt = "Climate factor (0.1 dry) to (0.5 Humid) ? "
                link.cfactor = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break

        while True:
            try:
                if link.tfactor:
                    prompt = "Terrain factor (0.25 Mountains, 1 Average, 4 Smooth) [%.2f]? " % link.tfactor
                else:
                    prompt = "Terrain factor (0.25 Mountains, 1 Average, 4 Smooth) ? "
                link.tfactor = raw_input(prompt)
            except ValueError as strerror:
                print strerror
                continue
            break




        gotInput = True
    
    f = StringIO()
    link.exportLink(f)
    print
    print "Based in input values, link calulation is"
    print(f.getvalue())




def main():
    
    link = LINK()
    doInput(link)


if __name__ == "__main__":
    main()
