from Scroller import *
import sys
args = sys.argv[1:]
id = args[0]
pw = args[1]
scroller = Scroller(id, pw)
scroller.run()