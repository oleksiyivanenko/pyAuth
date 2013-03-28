!include "MUI2.nsh"
!include LogicLib.nsh

Name "pyAuth"
OutFile "pyAuth_x64.exe"

installDir $PROGRAMFILES64

!define MUI_ABORTWARNING

!define sysGetDiskFreeSpaceEx 'kernel32::GetDiskFreeSpaceExA(t, *l, *l, *l) i'

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

var Username
var Computer
var ScreenHeight
var DiskSpace
var ButtonsNum
var Hash

Function .onInit
System::Call "advapi32::GetUserName(t .s, *i ${NSIS_MAX_STRLEN} r1) i.r2"
Pop $Username

ReadRegStr $Computer HKLM "System\CurrentControlSet\Control\ComputerName\ActiveComputerName" "ComputerName"

System::Call "user32::GetSystemMetrics(i 1) i .s"
Pop $ScreenHeight

System::Call "user32::GetSystemMetrics(i 43) i .s"
Pop $ButtonsNum

FunctionEnd

function FreeDiskSpace
  System::Call '${sysGetDiskFreeSpaceEx}(r0,.,.s,)'
  Pop $DiskSpace
functionend

section

StrCpy $0 $INSTDIR
Call FreeDiskSpace

DcryptDll::MD5Hash 	"SS"   $Username$Computer$WINDIR$SYSDIR$ScreenHeight$DiskSpace$ButtonsNum "--End--"
Pop $0
Pop $R0
StrCpy $Hash $R0

SetRegView 64
WriteRegStr HKCU "Software\o_ivanenko" "Signature" $Hash

DetailPrint $Username
DetailPrint $Computer
DetailPrint $WINDIR
DetailPrint $SYSDIR
DetailPrint $ScreenHeight
DetailPrint $DiskSpace
DetailPrint $ButtonsNum
DetailPrint $Hash
DetailPrint $Username$Computer$WINDIR$SYSDIR$ScreenHeight$DiskSpace$ButtonsNum

setOutPath $INSTDIR

File /r "pyAuth"
 
sectionEnd