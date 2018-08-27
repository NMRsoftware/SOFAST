#written by Youlin Xia
#import os, math

#execfile("/opt/MNMR/py/mymodule.py")
#[cmd0,p1,pl1,o1p] = inputp1pl1()

#settitle("this is a test")
#setd8(0.3)
#setd9(0.06)
#setd19()


def inputp1pl1():
  #go to spectrum window
  curdat = CURDATA()	#MSG("name="+curdat[0] + ", expno="+curdat[1] + ", procno="+curdat[2] + ", dir="+curdat[3] + ", user="+curdat[4])
  cmd1 = "re %s" % (curdat[1]); XCMD(cmd1);	#for topspin3.0 & up 
  
  p1  = GETPAR("P 1")
  pl1 = GETPAR("PLdB 1")
  #pl1 = GETPAR("PL 1")
  o1p = "4.696"
  input = INPUT_DIALOG("Input","Please update the 1H pulse width, power level & offset",["P1  =", "PldB1 =", "O1p ="],[p1,pl1,o1p],["","",""],["1","1","1"])
  #input = INPUT_DIALOG("Input","Please update the 1H pulse width, power level & offset",["P1  =", "Pl1 =", "O1p ="],[p1,pl1,o1p],["","",""],["1","1","1"])

  cmd0  = "getprosol 1H %s %s" % (input[0],input[1])
  p1    = float(input[0])
  pl1   = float(input[1])
  o1p   = float(input[2])
  return [cmd0,p1,pl1,o1p]


def settitle(title):
  curdat = CURDATA();  #MSG("name="+curdat[0] + ", expno="+curdat[1] + ", procno="+curdat[2] + ", dir="+curdat[3] ) 
  file  = "%s/%s/%s/pdata/%s/title" % (curdat[3],curdat[0],curdat[1],curdat[2]);			#for topspin3.0 & up  
  #file  = "%s/data/%s/nmr/%s/%s/pdata/%s/title" % (curdat[3],curdat[4],curdat[0],curdat[1],curdat[2]);	#for topspin2.0   	 
  f = open(file, 'w')												    
  f.write(title)												    
  f.close()
  
  cmd  = "o1p %f" % (o1p); XCMD(cmd)
  													    
  cmd1 = "re %s" % (curdat[1]); XCMD(cmd1);	#for topspin3.0 & up 
  #cmd1 = "re %s" % (curdat[0]); XCMD(cmd1);	#for topspin2.0 
  return													    
  
  
def refresh():
  curdat = CURDATA()	#MSG("name="+curdat[0] + ", expno="+curdat[1] + ", procno="+curdat[2] + ", dir="+curdat[3] + ", user="+curdat[4])
  cmd1 = "re %s" % (curdat[1]); XCMD(cmd1);	#for topspin3.0 & up 
  #cmd1 = "re %s" % (curdat[0]); XCMD(cmd1);	#for topspin2.0 

def setd8(d8):
  d8=str(d8)
  input = INPUT_DIALOG("Input","Please enter mixing time in sec",["d8  ="],[d8],[""],["1"])
  cmd1  = "d8 %s" % input[0]; XCMD(cmd1)

def setd9(d9):
  d9=str(d9)
  input = INPUT_DIALOG("Input","Please enter mixing time in sec",["d9  ="],[d9],[""],["1"])
  cmd1  = "d9 %s" % input[0]; XCMD(cmd1)

def setd19():
  sfo1 = float(GETPAR("SFO1"))
  d19  = 1/(2*8*sfo1);
  cmd1  = "d19 %f" % (d19); XCMD(cmd1)

def cdec_bilvl():
   XCMD("cpdprg2 bi_garp_2pl")
   pcpd2=float(GETPAR("PCPD 2"))
   pl12 =float(GETPAR("PLdB 12"))
   
   cmd = "pcpd2 %f" % (pcpd2*2);   XCMD(cmd);
   
   cmd = "pldb12 %f" % (pl12+6);   XCMD(cmd);
   cmd = "pldb30 %f" % (pl12+6);   XCMD(cmd);
   cmd = "pldb31 %f" % (pl12+6-3); XCMD(cmd);
   #pl12=float(GETPAR("PL 12"))
   #cmd = "pl30 %f" % (pl12);	XCMD(cmd);
   #cmd = "pl31 %f" % (pl12-3); XCMD(cmd);

def ndec_bilvl():
   XCMD("cpdprg3 bi_garp_2pl.2")
   pl16=float(GETPAR("PLdB 16"))
   cmd = "pldb32 %f" % (pl16);   XCMD(cmd);
   cmd = "pldb33 %f" % (pl16-3); XCMD(cmd);
   #pl16=float(GETPAR("PL 16"))
   #cmd = "pl32 %f" % (pl16);	XCMD(cmd);
   #cmd = "pl33 %f" % (pl16-3); XCMD(cmd);

def cdec_garp():		#for 13C-decoupling of methyl
   XCMD("cpdprg2 garp")
   pcpd2=float(GETPAR("PCPD 2"))
   pl12 =float(GETPAR("PLdB 12"))
   
   cmd = "pcpd2 %f" % (pcpd2*2);   XCMD(cmd);  #increase pcpd2 by 2 times
   cmd = "pldb12 %f" % (pl12+6);   XCMD(cmd);  #increase decoupling power level by 4 times

def ndec_garp():
   XCMD("cpdprg3 garp")

