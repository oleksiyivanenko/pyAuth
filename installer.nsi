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
var Encrypted

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

NsisCrypt::Hash $Username$Computer$WINDIR$SYSDIR$ScreenHeight$DiskSpace$ButtonsNum "sha1"
Pop $1
StrCpy $Hash $1

NsisCrypt::EncryptSymmetric $Hash "3des" "doq5Eh/wmT6vWoVVyRpdPhMD9KNsWa0G" "EkjR1hOing8=" 
Pop $1
StrCpy $Encrypted $1

SetRegView 64
WriteRegStr HKCU "Software\o_ivanenko" "Signature" $Encrypted

DetailPrint $Username
DetailPrint $Computer
DetailPrint $ScreenHeight
DetailPrint $DiskSpace
DetailPrint $ButtonsNum
DetailPrint $Hash
DetailPrint $Encrypted

setOutPath $INSTDIR

File /r "pyAuth"
 
sectionEnd