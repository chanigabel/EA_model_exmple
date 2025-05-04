'UserLockApplyAndRelease
'The script, adapted to VBScript by Chany Jacobs,
'Tested and worked on 04-30-2024
Option Explicit

!INC Local Scripts.EAConstants-VBScript

' Function to lock or unlock elements in a diagram
Sub LockElements(selectedDiagram, repository, action, lockedElements)
    lockedElements.RemoveAll

    Dim curObject, curElement
    For Each curObject In selectedDiagram.DiagramObjects
        Set curElement = repository.GetElementByID(curObject.ElementID)
        If Not curElement Is Nothing Then
            If action = "Lock" Then
                ' Check if the element is already locked
				If curElement.Locked Then
				Else

                    ' Apply user lock to the selected element
                    curElement.Locked = True
                    If repository.IsSecurityEnabled Then
                        curElement.ApplyUserLock
                    End If
                End If
            ElseIf action = "Unlock" Then
                ' Check if the element is locked
                If Not curElement.Locked Then
                    lockedElements.Add curElement.Name
                    ' Skip updating the unlocked element
                Else
                    ' Remove user lock from the selected element
                    curElement.Locked = False
                    If repository.IsSecurityEnabled Then
                        curElement.ApplyUserLock
                    End If
                End If
            End If
        End If
    Next

    If lockedElements.Count > 0 Then
        If action = "Lock" Then
            MsgBox lockedElements.Count & " elements are already locked.", vbInformation, "Locked Elements"
        ElseIf action = "Unlock" Then
            MsgBox lockedElements.Count & " elements are already unlocked.", vbInformation, "Unlocked Elements"
        End If
    Else
        If action = "Lock" Then
            MsgBox "All eligible elements have been locked.", vbInformation, "Done"
        ElseIf action = "Unlock" Then
            MsgBox "All eligible elements have been unlocked.", vbInformation, "Done"
        End If
    End If
End Sub

' Function to handle locking or unlocking elements dialog
Sub LockElementsDialog(repository)
    Dim dialogResult, selectedDiagram, action, lockedElements

    If repository.IsSecurityEnabled Then
        dialogResult = MsgBox("This option locks or unlocks elements in the selected diagram." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Lock or Unlock Elements")
    Else
        dialogResult = MsgBox("This option locks or unlocks elements in the selected diagram." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Lock or Unlock Elements")
    End If

    If dialogResult = vbYes Then
        Set selectedDiagram = repository.GetCurrentDiagram()
        If Not selectedDiagram Is Nothing Then
            ' Prompt user to select action
            action = MsgBox("Select action:" & vbCrLf & "1. Lock - yes" & vbCrLf & "2. Unlock - no", vbQuestion + vbYesNoCancel, "Action Selection")
            If action = vbCancel Then
                MsgBox "Script cancelled.", vbInformation, "Cancelled"
                Exit Sub ' Cancel the script if user cancels action selection
            ElseIf action = vbYes Then
                action = "Lock"
            ElseIf action = vbNo Then
                action = "Unlock"
            Else
                MsgBox "Invalid action. Please select either 'Lock' or 'Unlock'.", vbExclamation, "Error"
                Exit Sub
            End If

            ' Create a dictionary to store locked elements
			Set lockedElements = CreateObject("Scripting.Dictionary")

			' Perform action based on user selection
			LockElements selectedDiagram, repository, action, lockedElements

        Else
            MsgBox "This script requires a diagram to be selected.", vbExclamation, "Error"
        End If
    Else
        MsgBox "Script cancelled.", vbInformation, "Cancelled"
    End If
End Sub

' Main function
Sub Main()
    Repository.EnsureOutputVisible "Script"
    LockElementsDialog Repository
End Sub

' Call the main function
Main
