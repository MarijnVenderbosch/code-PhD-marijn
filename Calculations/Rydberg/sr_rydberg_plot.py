from arc import *

atom= Strontium88()

calc = LevelPlot(atom)
level = calc.makeLevels(5,5,0,3,sList=[0,1])
calc.drawLevels()
calc.showPlot()