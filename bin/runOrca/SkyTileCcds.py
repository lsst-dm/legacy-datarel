#!/usr/bin/env python
#

from optparse import OptionParser
import lsst.daf.persistence as dafPersist
from lsst.obs.lsstSim import LsstSimMapper
from lsst.obs.cfht import CfhtMapper

usage = "usage: %prog  option  SKYTILE\nwhere\n   SKYTILE - identifies region whose overlapping CCDs are selected\nExample: %prog --cfht 100477\nExample: %prog --imsim 93687"
parser = OptionParser( usage = usage )
parser.add_option("-i", "--imsim", action="store_true", default=False, \
                  help="extract skytile from imsim dataset")
parser.add_option("-c", "--cfht", action="store_true", default=False,\
                  help="extract skytile from CFHT dataset")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("provide a single skytile")
skyTile = args[0]

if options.imsim and options.cfht:
    parser.error("options --imsim and --cfht are mutually exclusive")

if options.imsim:
   bf = dafPersist.ButlerFactory(
           mapper=LsstSimMapper(
               registry="/lsst/DC3/data/obstest/ImSim/registry.sqlite3"))
   butler = bf.create()
   print ">intids visit snap"
   for visitRet, snapRet, raftRet, sensorRet in \
           butler.queryMetadata("raw", "sensor", \
                ("visit", "raft", "sensor"), skytile=skyTile):
       for visit, raft, sensor, channel, snap in \
           butler.queryMetadata("raw", "channel", \
                ( "visit", "raft", "sensor", "channel", "snap" ), \
                visit=visitRet, raft=raftRet, sensor=sensorRet ):
           print "raw visit=%d snap=%d raft=%s sensor=%s channel=%s" \
                 % ( visit, snap, raft, sensor, channel )
else:
   cfhtRoot="/lsst/DC3/data/obstest/CFHTLS/"
   bf = dafPersist.ButlerFactory( mapper=CfhtMapper( root=cfhtRoot ))
   butler = bf.create()
   print ">intids visit ccd amp"
   for visitRet, ccdRet in \
           butler.queryMetadata( "raw", "ccd", ( "visit", "ccd" ), \
              skytile=skyTile):
       for visit,  ccd, amp in \
           butler.queryMetadata( "raw", "ccd", \
               ( "visit",  "ccd", "amp" ), \
               visit=visitRet,ccd=ccdRet ):
           print "raw visit=%d  ccd=%s amp=%s"  \
                 % ( visit,  ccd, amp )

   