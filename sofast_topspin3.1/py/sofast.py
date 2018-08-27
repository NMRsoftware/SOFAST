#written by Youlin Xia
#this script works for both topspin2 and 3

import os, math

viewpdf = """
import os
os.system('evince /opt/MNMR/py/sofast.pdf')
"""

def myshape():
#[spnam1, spnam2] = myshape()
#generate cosine and sine modulated Pc9_4 shaped pulses
#the bandwidth is 5 or 4 ppm
#the modulation frequency is 3.8 ppm, so the centers of the two lobes are +3.8 or -3.8ppm from water frequency 4.7 ppm

  import os, os.path, math

  cnst2=5.0			  #5 ppm excitation bandwidth
  bf1= float(GETPAR("BF1")); 
  p41=7.2/(cnst2*bf1/1000000)	  #in us
   
  pw  =0.1*int(p41*10)  	  #keep 1 decimal
  freq=int(3.8*bf1)		  #integer

  spnam1 = '%s%.1f%s%d%s' % ('Pc9_4_90.pw', pw, 'us_cos', freq, 'Hz');    #MSG(spnam1)
  spnam2 = '%s%.1f%s%d%s' % ('Pc9_4_90.pw', pw, 'us_sin', freq, 'Hz');    #MSG(spnam2)

  import de.bruker.nmr.mfw.root.UtilPath as UtilPath;  #see sino2d.py  
  wave_path = "%s/exp/stan/nmr/lists/wave" % (UtilPath.getTopspinHome()); #MSG(wave_path)
  wave0 = "%s/%s" % (wave_path,"Pc9_4_90.1000")
  wave1 = "%s/%s" % (wave_path,spnam1)    
  wave2 = "%s/%s" % (wave_path,spnam2)

  if not os.path.exists(wave1):
     cmd1  = "cp %s %s" % (wave0,wave1);     
     cmd2  = "cp %s %s" % (wave0,wave2);     
     os.system(cmd1);
     os.system(cmd2); 

     cmd  = "st manipulate %s cosm2 %d %d" % (spnam1, pw, freq); XCMD(cmd)
     cmd  = "st manipulate %s sinm2 %d %d" % (spnam2, pw, freq); XCMD(cmd)

     am =2000000/(4*pw*0.125);
     msg ="Two new waves are generated:\n  %s\n  %s\n" %(wave1, wave2); 
     msg2="Amplitude of the shaped pulse should be %.1f Hz\n" % (am);
     MSG(msg + msg2)

  return [spnam1, spnam2]
  


#########################
#main program


execfile("/opt/MNMR/py/mymodule.py")
[cmd0,p1,pl1,o1p] = inputp1pl1()

EXEC_PYSCRIPT(viewpdf)

msg0="Choose your sofast experiment: "

value='1';
input = INPUT_DIALOG("Input",msg0,["number  ="],[value],[""],["1"])
value = int (input[0]); 
     
if value >24 or value<1: EXIT()




if value == 1: 
   XCMD("rpar HSQCFPF3GPPHWG all")

   XCMD("1 FnMODE States-TPPI")
   XCMD("pulprog IBS_SOFAST.x")
   XCMD(cmd0)
   bf2=float(GETPAR("BF2"))

   labeling= INPUT_DIALOG("labeling", "13C/15N labeled (a) or 15N-only labeled (b) sample? ", [""], ["a"], [""], ["1"])

   if labeling[0] == "a":
     XCMD("ZGOPTNS -DLABEL_CN")
   else:
     XCMD("ZGOPTNS  ")

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST3 120.0")
   XCMD("CNST4 95.0")

   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")

   if bf2 >= 165: 
     XCMD("spnam13 Crp80,0.5,20.1")
     XCMD("SPOAL13 0.5")
   else:
     XCMD("spnam13 Crp60,0.5,20.1")
     XCMD("SPOAL13 0.5")

   XCMD("gpnam1 SMSQ10.100")
   XCMD("gpnam2 SMSQ10.100")
   XCMD("GPZ1 11.0")
   XCMD("GPZ2 35.0")

   XCMD("O2P 110")
   XCMD("O3P 118")
   XCMD("D1 0.2")
   XCMD("1 SW 36")
   XCMD("2 AQ 0.05")

   msg="H-N sofast HMQC\nNote: \nPlease don't use get prosol. You only need to change p1 value."


if value == 2 or value == 3: 
   XCMD("rpar HSQCGP all")

   XCMD("1 FnMODE States-TPPI")

   if value == 2:
      XCMD("pulprog IBS_C_SOFAST.x")
      XCMD(cmd0)
      XCMD("CNST1 0.9")
      XCMD("CNST2 5.0")
      XCMD("CNST3 120.0")
      XCMD("CNST4 125.0")
      
      XCMD("1 SW 22")
      XCMD("O2P 17")
      
      XCMD("spnam25 Pc9_4_90.1000")
      XCMD("SPOAL25 0.5")
      XCMD("spnam26 Reburp.1000")
      XCMD("SPOAL26 0.5")
      
      msg="H-C sofast HMQC\nNote: \nPlease don't use get prosol. You only need to change p1 value."

   if value == 3:
      XCMD("pulprog sfhmqc.aro")
      XCMD(cmd0)
      XCMD("CNST2 5.0")
      XCMD("CNST3 120.0")
      XCMD("CNST5 160.0")
      XCMD("CNST21 8.5")

      XCMD("1 SW 30")
      XCMD("O2P 125")
      
      XCMD("spnam27 Pc9_4_90.1000")
      XCMD("SPOAL27 0.5")
      XCMD("spnam28 Reburp.1000")
      XCMD("SPOAL28 0.5")
      
      msg="H-C sofast HMQC for aromatic ring\nNote: \nPlease don't use get prosol. You only need to change p1 value."
      
   cdec_garp()

   XCMD("gpnam1 SMSQ10.100")
   XCMD("gpnam2 SMSQ10.100")
   XCMD("gpnam3 SMSQ10.100")
   XCMD("GPZ1 11.0")
   XCMD("GPZ2 35.0")
   XCMD("GPZ3 25")

   XCMD("O3P 118")
   XCMD("NS 2")
   XCMD("D1 0.2")
   XCMD("1 fcor 0.5")

   XCMD("2 AQ 0.05") 


if value == 4: 
   XCMD("rpar HC2D_N all")

   XCMD("1 FnMODE States-TPPI")
   XCMD("pulprog sfCNhmqcgpph19")   
   XCMD(cmd0)
   XCMD("CNST2 5.0")		    
   XCMD("CNST3 120.0")		    
      
   [spnam1, spnam2] = myshape()
   cmd="spnam31 %s" % (spnam1); XCMD(cmd)
   XCMD("SPOAL31 0.5")
   
   cdec_garp()
   ndec_garp()

   XCMD("gpnam1 SMSQ10.100")
   XCMD("gpnam2 SMSQ10.50")
   XCMD("GPZ1 20")
   XCMD("GPZ2 60")

   cnst8="%.1f" % (36*float(GETPAR("BF3")))
   input = INPUT_DIALOG("Input","Please enter 15N spectral width in Hz",["cnst8  ="],[cnst8],[""],["1"])
   cmd1  = "cnst8 %s" % input[0]; XCMD(cmd1)

   XCMD("1 SW 22")
   XCMD("1 TD 128")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("NS 2")
   XCMD("D1 0.2")

   XCMD("2 AQ 0.05") 

   msg="""Simultaneous sofast 2D CN-HMQC\nNote:
1. Please don't use get prosol. You only need to change p1 value.
2. TD(F1) <= L1. L1 is shown in the parameter panel of command 'ased' 
   Decreasing SW(F2) or increasing cnst8 may increase the L1 value!"""

if value == 5: 
   XCMD("rpar NOESYHSQCF3GP193D all")
   XCMD("GPNAM1 SMSQ10.32")
   XCMD("GPNAM2 SMSQ10.50")
   XCMD("GPNAM3 SMSQ10.50")
   XCMD("GPNAM4 SMSQ10.32")
   XCMD("GPNAM5 SMSQ10.50")
   XCMD("GPNAM6 SMSQ10.32")
   XCMD("GPNAM7 SMSQ10.50")
   XCMD("GPZ1 2.0")
   XCMD("GPZ2 21.0")
   XCMD("GPZ3 -80.0")
   XCMD("GPZ4 15.0")
   XCMD("GPZ5 30.0")
   XCMD("GPZ6 60.0")
   XCMD("GPZ7 30.13")
   XCMD("P16 500u")
   XCMD("P17 300u")
   
   XCMD("pulprog noesysftrosy3d.Hall-NHn");   
   XCMD("2 FNMODE Echo-Antiecho");
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST5 95.0")
   
   XCMD("SPNAM25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("SPNAM26 Reburp.1000")
   XCMD("SPOAL26 1.0")
   XCMD("SPNAM28 Eburp2.1000")
   XCMD("SPOAL28 0.0")
   XCMD("SPNAM29 Eburp2tr.1000")
   XCMD("SPOAL29 1.0")

   bf2=float(GETPAR("BF2"))
   if bf2 >= 165: 
     XCMD("spnam13 Crp80,0.5,20.1")
     XCMD("SPOAL13 0.5")
   else:
     XCMD("spnam13 Crp60,0.5,20.1")
     XCMD("SPOAL13 0.5")
      
   XCMD("1 SW 11")
   XCMD("1 td 256")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 110")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-TROSY for Hall(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 6: 
   XCMD("rpar HCACOGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfhmqcnoesyhmqc3d.Cm-CmHm");
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST3 110.0")
   XCMD("CNST4 125.0")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   XCMD("1 SW 22")
   XCMD("2 SW 22")   
   XCMD("1 td 128")
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("2 reverse FALSE")

   msg="sofast 3D HMQC-NOESY-HMQC for Cm(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 7: 
   XCMD("rpar HCACOGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfhmqcnoesyhmqc3d.Ca-CmHm");
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 125.0")
   XCMD("CNST5 160.0")
   XCMD("CNST21 8.5")
   XCMD("CNST22 125")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   XCMD("1 SW 30")
   XCMD("2 SW 22")   
   XCMD("1 td 128")
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("2 reverse FALSE")

   msg="sofast 3D HMQC-NOESY-HMQC for Caro(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 8: 
   XCMD("rpar HCANGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfNhmqcnoesyhmqc3d.N-CmHm");
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 125.0")
   XCMD("CNST5 95.0")
   XCMD("CNST7 8.5")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 55")
   XCMD("gpz3 30")
   
   XCMD("1 SW 36")
   XCMD("2 SW 22")   
   XCMD("1 td 128")
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("2 reverse FALSE")

   msg="sofast 3D HMQC-NOESY-HMQC for N(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 9: 
   XCMD("rpar HNCAGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfhmqcnoesyNhmqc3d.Cm-NHn");   
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 125.0")
   XCMD("CNST5 95.0")
   XCMD("CNST7 8.5")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 55")
   XCMD("gpz3 30")
   
   XCMD("1 SW 22")
   XCMD("1 td 128")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-HMQC for Cm(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."


if value == 10: 
   XCMD("rpar HNCAGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfhmqcnoesyNhmqc3d.Ca-NHn");   
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 160.0")
   XCMD("CNST5 95.0")
   XCMD("CNST21 8.5")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 55")
   XCMD("gpz3 30")
   
   XCMD("1 SW 30")
   XCMD("1 td 128")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 125")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-HMQC for Cm(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."





if value == 11: 
   XCMD("rpar HNN3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfNhmqcnoesyNhmqc3d.N-NHn");   
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST3 110.0")
   XCMD("CNST5 95.0")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   XCMD("1 SW 36")
   XCMD("1 td 128")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   XCMD('digmod digital')  #in the parameter file, the digmod is baseopt that needs "acqt0=-p1*2/3.1416" in pulse sequence
   msg="sofast 3D NOESY-HMQC for N(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 12: 
   XCMD("rpar HCACOGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.50")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfCNhmqcnoeCNhmqc3d.NCm-NCmHnHm");
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()
   ndec_garp()

   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   
   [spnam1, spnam2] = myshape()
   cmd="spnam29 %s" % (spnam1); XCMD(cmd)
   cmd="spnam31 %s" % (spnam1); XCMD(cmd)
   XCMD("SPOAL29 0.5")
   XCMD("SPOAL31 0.5")
         
   cnst8="%.1f" % (36*float(GETPAR("BF3")))
   input = INPUT_DIALOG("Input","Please enter 15N spectral width in Hz",["cnst8  ="],[cnst8],[""],["1"])
   cmd1  = "cnst8 %s" % input[0]; XCMD(cmd1)

   XCMD("gpz1 25")
   XCMD("gpz2 35")
   XCMD("gpz3 30")
   
   XCMD("1 SW 22")
   XCMD("2 SW 22")   
   XCMD("1 td 200")
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("2 reverse FALSE")

   msg="""sofast simultaneous 3D HMQC-NOESY-HMQC for NCm(F1)-NCm(F2)HnHm(F3)
Note: 
1. Please don't use get prosol. You only need to change p1 value.
2. TD(F2) <= L1; TD(F1) <= 2*L1. L1 is shown in the parameter panel of command 'ased' .
   Decreasing SW(F2) & SW(F1) or increasing cnst8 may increase the L1 value!
3. The value of TD(F1) should be 2-time of regular TD(F1) because two sets of data are acquired simultaneously.
4. Use 'split ipap 2' to split the acquired data.
5. Acquisition order is 312. When you use nmrPipe's command bruker to convert Bruker data to nmrPipe,
   please don't forget to swap parameters of F1 and F2 or Y and Z dimensions because nmrPipe supposes the
   acquisition order is 321. """



if value == 13: 
   MSG('Please choose other experiment!')
   msg='Please choose other experiment!'


if value == 14 or value == 15: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   if value == 14:
      XCMD("pulprog noesysfhmqc3d.Hall-CmHm");
      XCMD("CNST3 110.0")
   if value == 15:
      XCMD("pulprog sfnoesyhmqc3d.HnHa-CmHm");
      XCMD("CNST3 90.0")
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST4 125.0")
   XCMD("CNST21 8.5")
   XCMD("CNST22 125")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   if value == 14:
      XCMD("1 SW 11")
      XCMD("1 td 256")
   if value == 15:
      XCMD("1 SW 5.5")
      XCMD("1 td 128")
   XCMD("2 SW 22")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   if value == 14:
      msg="sofast 3D NOESY-HMQC for Hall(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."
   if value == 15:
      msg="sofast 3D NOESY-HMQC for HnHa(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."

if value == 16: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfnoesyhmqc3d.Hm-CmHm");
   XCMD("CNST3 110.0")
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST4 125.0")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   XCMD("1 SW 3")
   XCMD("1 td 64")
   XCMD("2 SW 22")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-HMQC for Hm(F1)-Cm(F2)Hm(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."


if value == 17: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfnoesyhmqc3d.HnHaHm-CmHm");

   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 125.0")
   
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")

   [spnam1, spnam2] = myshape()
   cmd="spnam29 %s" % (spnam1); XCMD(cmd)
   cmd="spnam30 %s" % (spnam2); XCMD(cmd)
   XCMD("SPOAL29 0.5")
   XCMD("SPOAL30 0.5")
         
   XCMD("gpz1 25")
   XCMD("gpz2 35")
   XCMD("gpz3 30")
   
   XCMD("1 SW 5.5")
   XCMD("1 td 256")  #64 increments for 5.5 ppm of HN or HM
      
   XCMD("2 SW 22")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   msg="""sofast simultaneous 3D NOESY-HMQC for HnHaHM(F1)-Cm(F2)Hm(F3)
1. Please don't use get prosol. You only need to change p1 value.
2. Use 'split ipap 2' to split the acquired data.
3. Acquisition order is 312. When you use nmrPipe's command bruker to convert Bruker data to nmrPipe,
   please don't forget to swap parameters of F1 and F2 or Y and Z dimensions because nmrPipe supposes the
   acquisition order is 321. """





if value == 18 or value == 19: 
   XCMD("rpar NOESYHSQCF3GP193D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   if value == 18:
      XCMD("pulprog sfnoesyNhmqc3d.HnHa-NHn");
      XCMD("CNST3 110.0")
   if value == 19:
      XCMD("pulprog noesysfNhmqc3d.Hall-NHn");
      XCMD("CNST3 90.0")
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST5 95.0")
   XCMD("CNST22 125.0")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 20")
   XCMD("gpz2 30")
   XCMD("gpz3 60")
   
   if value == 18:
      XCMD("1 SW 5.5")
      XCMD("1 td 128")
   if value == 19:
      XCMD("1 SW 11")
      XCMD("1 td 256")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   if value == 18:
      msg="sofast 3D NOESY-HMQC for HnHa(F1)-Nm(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."
   if value == 19:
      msg="sofast 3D NOESY-HMQC for Hall(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."



if value == 20 or value == 21: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   if value == 20:
      XCMD("pulprog noesysfCNhmqc3d19.Hall-NCmHnHm");
   if value == 21:
      XCMD("pulprog sfCNnoesyCNhmqc3d.Hall-NCmHnHm");

   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()
   ndec_garp()

   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   
   [spnam1, spnam2] = myshape()
   cmd="spnam29 %s" % (spnam1); XCMD(cmd)
   cmd="spnam30 %s" % (spnam2); XCMD(cmd)
   cmd="spnam31 %s" % (spnam1); XCMD(cmd)
   XCMD("SPOAL29 0.5")
   XCMD("SPOAL30 0.5")
   XCMD("SPOAL31 0.5")
         
   cnst8="%.1f" % (36*float(GETPAR("BF3")))
   input = INPUT_DIALOG("Input","Please enter 15N spectral width in Hz",["cnst8  ="],[cnst8],[""],["1"])
   cmd1  = "cnst8 %s" % input[0]; XCMD(cmd1)

   XCMD("gpz1 25")
   XCMD("gpz2 35")
   XCMD("gpz3 30")
   
   if value == 20:
      XCMD("1 SW 11")
      XCMD("1 td 256")  #128 increments for 11 ppm of Hall
   if value == 21:
      XCMD("1 SW 5.5")
      XCMD("1 td 256")	#64 increments for 5.5 ppm of HN or HM
      
   XCMD("2 SW 22")   
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")

   if value == 20:
      msg="""sofast simultaneous 3D NOESY-HMQC for Hall(F1)-NCm(F2)HnHm(F3)
1. Please don't use get prosol. You only need to change p1 value.
2. TD(F2) <= L1. L1 is shown in the parameter panel of command 'ased'. 
   Decreasing SW(F2) or increasing cnst8 may increase the L1 value!"""

   if value == 21:
      msg="""sofast simultaneous 3D NOESY-HMQC for HnHaHM(F1)-NCm(F2)HnHm(F3)
1. Please don't use get prosol. You only need to change p1 value.
2. TD(F2) <= L1. L1 is shown in the parameter panel of command 'ased'. 
   Decreasing SW(F2) or increasing cnst8 may increase the L1 value!
3. Use 'split ipap 2' to split the acquired data.
4. Acquisition order is 312. When you use nmrPipe's command bruker to convert Bruker data to nmrPipe,
   please don't forget to swap parameters of F1 and F2 or Y and Z dimensions because nmrPipe supposes the
   acquisition order is 321. """



if value == 22: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.50")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfhmqcnoesyCNhmqc3d.Ha-NCmHnHm");
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()
   ndec_garp()

   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 160.0")
   XCMD("CNST21 8.5")
   XCMD("CNST22 125.0")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")

   [spnam1, spnam2] = myshape()
   cmd="spnam31 %s" % (spnam1); XCMD(cmd)
   XCMD("SPOAL31 0.5")
         
   cnst8="%.1f" % (36*float(GETPAR("BF3")))
   input = INPUT_DIALOG("Input","Please enter 15N spectral width in Hz",["cnst8  ="],[cnst8],[""],["1"])
   cmd1  = "cnst8 %s" % input[0]; XCMD(cmd1)

   XCMD("gpz1 25")
   XCMD("gpz2 35")
   XCMD("gpz3 30")
   
   XCMD("1 SW 3")
   XCMD("2 SW 22")   
   XCMD("1 td 40")
   XCMD("2 td 64")
   XCMD("O2P 17")
   XCMD("O3P 118")
   XCMD("2 reverse FALSE")

   msg="""sofast simultaneous 3D HMQC-NOESY-HMQC for Ha(F1)-NCm(F2)HnHm(F3)
Note:
1. Please don't use get prosol. You only need to change p1 value.
2. TD(F2) <= L1. L1 is shown in the parameter panel of command 'ased'. 
   Decreasing SW(F2) or increasing cnst8 may increase the L1 value!"""


if value == 23: 
   XCMD("rpar NOESYHSQCETGP3D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfnoesyhmqc3d.Hm-CaHa");
   XCMD("CNST3 110.0")
   XCMD("2 FNMODE States-TPPI");
   XCMD(cmd0)

   cdec_garp()

   XCMD("CNST1 0.9")
   XCMD("CNST2 5.0")
   XCMD("CNST5 160.0")
   XCMD("CNST21 8.5")
   XCMD("CNST22 17")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 25")
   XCMD("gpz3 30")
   
   XCMD("1 SW 4")
   XCMD("1 td 80")
   XCMD("2 SW 30")   
   XCMD("2 td 64")
   XCMD("O2P 125")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-HMQC for Hm(F1)-Ca(F2)Ha(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."


if value == 24: 
   XCMD("rpar NOESYHSQCF3GP193D all")
   XCMD("GPNAM1 SMSQ10.100")
   XCMD("GPNAM2 SMSQ10.100")
   XCMD("GPNAM3 SMSQ10.100")
   
   XCMD("pulprog sfnoesyNhmqc3d.Hm-NHn");
   XCMD("CNST3 110.0")
   XCMD("2 FNMODE States-TPPI");
   XCMD("cpdprg5 garp")
   XCMD(cmd0)

   ndec_garp()

   XCMD("CNST1 8.5")
   XCMD("CNST2 5.0")
   XCMD("CNST3 90.0")
   XCMD("CNST4 4.0")
   XCMD("CNST5 95.0")
   XCMD("CNST21 0.9")
   
   XCMD("spnam25 Pc9_4_90.1000")
   XCMD("SPOAL25 0.5")
   XCMD("spnam26 Reburp.1000")
   XCMD("SPOAL26 0.5")
   XCMD("spnam27 Pc9_4_90.1000")
   XCMD("SPOAL27 0.5")
   XCMD("spnam28 Reburp.1000")
   XCMD("SPOAL28 0.5")
      
   XCMD("gpz1 20")
   XCMD("gpz2 30")
   XCMD("gpz3 60")
   
   XCMD("1 SW 4")
   XCMD("1 td 128")
   XCMD("2 SW 36")   
   XCMD("2 td 64")
   XCMD("O2P 16")
   XCMD("O3P 118")

   msg="sofast 3D NOESY-HMQC for Hm(F1)-N(F2)Hn(F3)\nNote: \nPlease don't use get prosol. You only need to change p1 value."




XCMD("d1 0.2")
if value >4 and value != 13: setd8(0.3)
XCMD("sw 16")
XCMD("td 2k")	#XCMD("aq 50m")
setd19()
XCMD("rg 128")
XCMD('bc_mod qpol')
settitle(msg)



