'RemoveOrAddSuffixDiagramClassElementsNames
'The script, written by Chany Jacobs, 
'This script opens the Add/Remove Suffix dialog box which enables to add/remove 
'suffix to/from element names of the selected diagram which are not locked 
'and them type is class or interface.
'To run you need to open diagram.
'Tested and worked on 01-05-24
Option Explicit

' Function to delete suffix from element names
Sub DeleteSuffix(selectedDiagram, repository, suffix)
    Dim numLockedElements, numAffectedElements
    numLockedElements = 0
    numAffectedElements = 0

    Dim curObject, curElement
    For Each curObject In selectedDiagram.DiagramObjects
        Set curElement = repository.GetElementByID(curObject.ElementID)
        If curElement.Type = "Class" Or curElement.Type = "Interface" Then
            If repository.IsSecurityEnabled Then
                If curElement.Locked Then
                    numLockedElements = numLockedElements + 1
                Else
                    curElement.ApplyUserLock
                    If Right(curElement.Name, Len(suffix)) = suffix Then
                        curElement.Name = Left(curElement.Name, Len(curElement.Name) - Len(suffix))
                    End If
                    curElement.Update
                    numAffectedElements = numAffectedElements + 1
                End If
            Else
                If Right(curElement.Name, Len(suffix)) = suffix Then
                    curElement.Name = Left(curElement.Name, Len(curElement.Name) - Len(suffix))
                End If
                curElement.Update
                numAffectedElements = numAffectedElements + 1
            End If
        End If
    Next

    If repository.IsSecurityEnabled Then
        MsgBox numLockedElements & " elements were locked before. " & numAffectedElements & " elements were locked and affected by you.", vbInformation, "Info"
    Else
        MsgBox "Elements updated successfully!", vbInformation, "Info"
    End If
End Sub

' Function to add suffix to element names
Sub AddSuffix(selectedDiagram, repository, suffix)
    Dim numLockedElements, numAffectedElements
    numLockedElements = 0
    numAffectedElements = 0

    Dim curObject, curElement
    For Each curObject In selectedDiagram.DiagramObjects
        Set curElement = repository.GetElementByID(curObject.ElementID)
        If curElement.Type = "Class" Or curElement.Type = "Interface" Then
            If repository.IsSecurityEnabled Then
                If curElement.Locked Then
                    numLockedElements = numLockedElements + 1
                Else
                    curElement.ApplyUserLock
                    curElement.Name = curElement.Name & suffix
                    curElement.Update
                    numAffectedElements = numAffectedElements + 1
                End If
            Else
                curElement.Name = curElement.Name & suffix
                curElement.Update
                numAffectedElements = numAffectedElements + 1
            End If
        End If
    Next

    If repository.IsSecurityEnabled Then
        MsgBox numLockedElements & " elements were locked before. " & numAffectedElements & " elements were locked and affected by you.", vbInformation, "Info"
    Else
        MsgBox "Elements updated successfully!", vbInformation, "Info"
    End If
End Sub

' Function to handle update suffix dialog
Sub UpdateSuffixDialog(repository, flag)
    Dim dialogResult, selectedDiagram, suffix

    If repository.IsSecurityEnabled Then
        dialogResult = MsgBox("This option opens the Add/Remove Suffix dialog box which enables to add/remove suffix to/from class and interface element names of the selected diagram which are not locked." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Add/Remove Suffix to/from element names")
    Else
        dialogResult = MsgBox("This option opens the Add/Remove Suffix dialog box which enables to add/remove suffix to/from class and interface element names of the selected diagram." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Add/Remove Suffix to/from element names")
    End If

    If dialogResult = vbYes Then
        Set selectedDiagram = repository.GetCurrentDiagram ()
        If Not selectedDiagram Is Nothing Then
			suffix = InputBox("Enter the suffix to be added to/removed from the class and interface names:", "Suffix")
			If suffix <> "" Then
				If flag = 0 Then
					AddSuffix selectedDiagram, repository, suffix
				Else
					DeleteSuffix selectedDiagram, repository, suffix
				End If
			Else
				MsgBox "Suffix cannot be empty.", vbExclamation, "Error"
			End If
        Else
            MsgBox "This script requires a diagram to be selected.", vbExclamation, "Error"
        End If
    End If
End Sub

' Main function
Sub Main()
    Dim flag
    Repository.EnsureOutputVisible "Script"
    flag = InputBox("Enter 0 to add suffix or 1 to remove suffix:", "Flag")
    If flag = "" Then
        MsgBox "Process cancelled."
    ElseIf IsNumeric(flag) Then
        If flag = 0 Or flag = 1 Then
            UpdateSuffixDialog repository, CInt(flag)
        Else
            MsgBox "Invalid flag value. Please enter 0 or 1.", vbExclamation, "Error"
        End If
    Else
        MsgBox "Invalid flag value. Please enter 0 or 1.", vbExclamation, "Error"
    End If
End Sub

' Call the main function
Main
