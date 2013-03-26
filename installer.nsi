!include nsDialogs.nsh
!include LogicLib.nsh

Name "pyAuth"
OutFile "pyAuth_x64.exe"

XPStyle on

Page custom nsDialogsPage
Page instfiles

Var Dialog
Var Label
Var Text
var BUTTON

installDir $PROGRAMFILES64

Function nsDialogsPage
	nsDialogs::Create 1018
	Pop $0

	${NSD_CreateLabel} 0 10 100% 10u "Where you want to install pyAuth?"
	Pop $Label

	${NSD_CreateLabel} 0 35 75% 12u $INSTDIR
	Pop $Text
#	GetFunctionAddress $0 OnChange
#	nsDialogs::OnChange $Text $0

	${NSD_CreateButton} 75% 35 25% 12u "Change folder"
	Pop $0
	GetFunctionAddress $0 OnClick
	nsDialogs::OnClick $BUTTON $0
#	GetFunctionAddress $0 OnChange
#	nsDialogs::OnChange $EDIT $0


#	${If} $Dialog == error
#		Abort
#	${EndIf}
#
#	${NSD_CreateLabel} 0 0 100% 12u "Hello, welcome to nsDialogs!"
#	Pop $Label

#	nsDialogs::SelectFolderDialog "Select install folder" $INSTDIR
#	Pop $INSTDIR

	nsDialogs::Show
#
FunctionEnd

#Function OnChange
#
#	Pop $0
#	${NSD_GetText} $INSTDIR $0
#	System::Call user32::GetWindowText(i$Text,t.r0,i${NSIS_MAX_STRLEN})
#	StrCpy $INSTDIR $0
#	MessageBox MB_OK $INSTDIR
#
#FunctionEnd

Function OnClick

	Pop $0 # HWND

	nsDialogs::SelectFolderDialog "Select install folder" $INSTDIR
	Pop $INSTDIR

FunctionEnd

section

DetailPrint "hello world"

setOutPath $INSTDIR

File /r "pyAuth"
 
sectionEnd