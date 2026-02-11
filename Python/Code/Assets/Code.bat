@echo off
setlocal enabledelayedexpansion
title Double Line Program
color 0A

rem Initialize variables
set answer=
set var0=NONE
set var1=NONE
set var2=NONE
set var3=NONE
set var4=NONE
set var5=NONE
set var6=NONE
set var7=NONE
set var8=NONE
set var9=NONE
set var10=NONE
set var11=NONE
set var12=NONE
set var13=NONE
set var14=NONE
set var15=NONE
set var16=NONE
set var17=NONE
set var18=NONE
set var19=NONE
set var20=NONE
set var21=NONE
set var22=NONE
set var23=NONE
set var24=NONE
set var25=NONE
set var26=NONE
set var27=NONE
set var28=NONE
set var29=NONE
set var30=NONE
set var31=NONE
set var32=NONE
set var33=NONE
set var34=NONE
set var35=NONE
set var36=NONE
set var37=NONE
set var38=NONE
set var39=NONE
set var40=NONE
set var41=NONE
set var42=NONE
set var43=NONE
set var44=NONE
set var45=NONE
set var46=NONE
set var47=NONE
set var48=NONE
set var49=NONE
set var50=NONE
set var51=NONE
set var52=NONE
set var53=NONE
set var54=NONE
set var55=NONE
set var56=NONE
set var57=NONE
set var58=NONE
set var59=NONE
set var60=NONE
set var61=NONE
set var62=NONE
set var63=NONE
set var64=NONE
set var65=NONE
set var66=NONE
set var67=NONE
set var68=NONE
set var69=NONE
set var70=NONE
set var71=NONE
set var72=NONE
set var73=NONE
set var74=NONE
set var75=NONE
set var76=NONE
set var77=NONE
set var78=NONE
set var79=NONE
set var80=NONE
set var81=NONE
set var82=NONE
set var83=NONE
set var84=NONE
set var85=NONE
set var86=NONE
set var87=NONE
set var88=NONE
set var89=NONE
set var90=NONE
set var91=NONE
set var92=NONE
set var93=NONE
set var94=NONE
set var95=NONE
set var96=NONE
set var97=NONE
set var98=NONE
set var99=NONE

goto :main

:main
set var1=0
set loopCounter=0
set loopMax=3
:loopFor
if !loopCounter! GEQ !loopMax! goto :endloop
set /a var1=!var1! + 1
echo Outer loop: !var1!
set var2=0
set loopCounter=0
set loopMax=3
:loopFor
if !loopCounter! GEQ !loopMax! goto :endloop
set /a var2=!var2! + 1
echo   Inner loop: !var2!
set /a loopCounter+=1
goto loopFor
rem Unsupported: endLoop
set /a loopCounter+=1
goto loopFor
rem Unsupported: endLoop

:endloop
endlocal
exit
