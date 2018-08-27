;IBS_SOFAST.x
;d0 starts from 0

;avance-version (13/02/28)
;;SOFAST HMQC
;2D H-1/X correlation via heteronuclear zero and double quantum
;   coherence
;phase sensitive
;with decoupling during acquisition
;
;P.Schanda and B. Brutscher, J. Am. Chem. Soc. 127, 8014 (2005)
;
;$CLASS=IBS
;$DIM=2D
;$TYPE=
;$SUBTYPE=
;$COMMENT=

prosol relations=<triple>

#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>

define delay dNH

"d11=30m"
"d12=20u"
"dNH=1s/(cnst4*2)"


"in0=inf1"

;"d0=in0/2-p21*4/3.1415"
"d0=0"
/*******************************************************************/
/*   calculation of shaped 1H pulse parameters                     */
/*******************************************************************/

"p41=7.2/(cnst2*bf1/1000000)" /*  PC9  pulse length  */
"spw25=plw1*(pow((cnst3/90.0)*(p1/p41)/0.125,2))" /* PC9  power level  */
	;"sp25=pl1-20*log((cnst3/90.0)*(p1/p41)/0.125)/log(10)" /* PC9  power level  */
"spoff25=bf1*(cnst1/1000000)-o1"  /*  PC9  offset */
;"spoal25=0.5"

"p42=4.875/(cnst2*bf1/1000000)" /* REBURP pulse length  */
"spw26=plw1*(pow((p1*2/p42)/0.0798,2))"   /* REBURP power level  */
	;"sp26=pl1-20*log((p1*2/p42)/0.0798)/log(10)"   /* REBURP power level  */
"spoff26=bf1*(cnst1/1000000)-o1" /* REBURP offset */
;"spoal26=0.5"


/*******************************************************************/
/*   13C Adiabatic pulse                                           */
/*******************************************************************/

;"p8=500u"       /*      SPNAM 13","Crp80,0.5,20.1   */
;"if ( bf2 < 165 ) {spw13=plw2*(pow((p3/25.5832),2)); } else{spw13=plw2*(pow((p3/22.1557),2));} "

/*******************************************************************/
/*   calculation of 15N decoupling                                 */
/*******************************************************************/
;"pcpd3=300u"
;"plw26 =plw3*(pow((p21/pcpd3),2))" /* CPD  power level  */

"DELTA1=dNH-p16-d16-p41*0.55"
"DELTA2=p41*0.55-de-4u"




1 ze 
  d11 pl16:f3
2 d1 do:f3
3 d12 pl3:f3
  50u UNBLKGRAD

  "d21 = d0 - p21*0.637*2"
  if "d21 < 0"
   { 
   "d21 = 0"
   }

  p16:gp2
  d16

  (p41:sp25 ph1):f1
  p16:gp1
  d16

#   ifdef LABEL_CN
  (center (p42:sp26 ph2):f1 (DELTA1 p21 ph3 d21 p21 ph4 DELTA1):f3  (p8:sp13 ph1):f2)
#   else
  (center (p42:sp26 ph2):f1 (DELTA1 p21 ph3 d21 p21 ph4 DELTA1):f3 )
#   endif /*LABEL_CN*/


  DELTA2
  p16:gp1
  d16 pl16:f3
  4u BLKGRAD
  go=2 ph31 cpd3:f3 
  d1 do:f3 mc #0 to 2 
     F1PH(calph(ph3, +90), caldel(d0, +in0))
exit 
  

ph1=0 
ph2=0 
ph3=0 2
ph4=0 0 2 2 
ph31=0 2 2 0


;pl3 : f3 channel - power level for pulse (default)
;pl26: f3 channel - power level for CPD/BB decoupling (low power)
;sp13: f2 channel - shaped pulse 180 degree (adiabatic)



;sp23: f1 channel - shaped pulse 120 degree 
;                   (Pc9_4_120.1000)
;sp24: f1 channel - shaped pulse 180 degree (Rsnob.1000)
;p8 : f2 channel - 180 degree shaped pulse for inversion (adiabatic)
;p16: homospoil/gradient pulse                       [1 msec]
;p21: 15N -  90 degree high power pulse
;d0 : incremented delay (2D) = in0/2-p21*4/3.1415
;d1 : relaxation delay
;d11: delay for disk I/O                             [30 msec]
;d12: delay for power switching                      [20 usec]
;d16: delay for homospoil/gradient recovery
;d21: internal delay
;dNH : 1/(2J)NH
;cnst4: = J(NH)
;cnst1: H(N) excitation frequency (in ppm)
;cnst2: H(N) excitation band width (in ppm)
;cnst3:  PC9 flip angle
;cnst41: Power change for PC9 pulse (dB)
;cnst42: Power change for REBURP pulse (dB)
;sp26: Reburp.1000
;sp25: Pc9_4_90.1000

;inf1: 1/SW(N) = 2 * DW(N)
;in0: 1/ SW(N) = 2 * DW(N)
;nd0: 1
;ns: 2 * n
;ds: 16
;aq: <= 50 msec
;td1: number of experiments
;FnMODE: States-TPPI, TPPI, States or QSEC
;cpd3: decoupling according to sequence defined by cpdprg3: garp4.p62
;pcpd3: f3 channel - 90 degree pulse for decoupling sequence
;          use pulse of >= 350 usec


;use gradient ratio:	gp 1 : gp 2
;			  11 :    7


;for z-only gradients:
;gpz1: 11%
;gpz2:  7%

;use gradient files:   
;gpnam1: SMSQ10.100
;gpnam2: SMSQ10.100


                                          ;preprocessor-flags-start
;LABEL_CN: for C-13 and N-15 labeled samples start experiment with
;             option -DLABEL_CN (eda: ZGOPTNS)
                                          ;preprocessor-flags-end




;$Id: sfhmqcf3gpph,v 1.10.6.2 2013/03/08 15:13:06 ber Exp $
