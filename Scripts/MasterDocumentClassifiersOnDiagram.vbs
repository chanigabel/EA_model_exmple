'MasterDocumentClassifiersOnDiagram
'The script, written by Chany Jacobs, 
'This script updates the Version and Phase of Diagram Elements.
'To run, you need to open a diagram.
'Tested and worked on 04-30-2024.

Option Explicit

' Function to check if an element is locked
Function IsElementLocked(elementGUID, repository)
    Dim squery
    Dim result
    Dim xmlDoc
    Dim user

    squery = "SELECT UserID FROM t_seclocks WHERE EntityID='" & elementGUID & "'"
    result = repository.SQLQuery(squery)
    
    Set xmlDoc = CreateObject("MSXML2.DOMDocument")
    xmlDoc.LoadXml(result)
    
    Set user = xmlDoc.SelectSingleNode("//UserID")

    If Not user Is Nothing Then
        IsElementLocked = True
    Else
        IsElementLocked = False
    End If
End Function

' Function to handle updating the Version and Phase dialog
Sub UpdateVersionAndPhaseDialog(repository)
    Dim dialogResult
    Dim selDiagram
    Dim Version_
    Dim Phase_

    If repository.IsSecurityEnabled Then
        dialogResult = MsgBox("This option opens the Update Version and Phase dialog box which enables updating the Version and Phase of the selected diagram's elements which are not locked." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update Version and Phase of Diagram Elements")
    Else
        dialogResult = MsgBox("This option opens the Update Version and Phase dialog box which enables updating the Version and Phase of the selected diagram's elements." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update Version and Phase of Diagram Elements")
    End If

    If dialogResult = vbYes Then
        Set selDiagram = repository.GetCurrentDiagram()
        If Not selDiagram Is Nothing Then
            Version_ = InputBox("Enter the version:", "Update Version and Phase")
            Phase_ = InputBox("Enter the phase:", "Update Version and Phase")
            If Version_ <> "" And Phase_ <> "" Then
                UpdateVersionAndPhase repository, selDiagram, Version_, Phase_
            Else
                MsgBox "Version and Phase cannot be empty.", vbExclamation, "Error"
            End If
        Else
            MsgBox "This script requires a diagram to be selected.", vbExclamation, "Error"
        End If
    End If
End Sub

' Function to update the Version and Phase
Sub UpdateVersionAndPhase(repository, selectedDiagram, Version_, Phase_)
    Dim curObject
    Dim curElement

    For Each curObject In selectedDiagram.DiagramObjects
        Set curElement = repository.GetElementByID(curObject.ElementID)
        If repository.IsSecurityEnabled Then
            If Not IsElementLocked(curElement.ElementGUID, repository) Then
                curElement.ApplyUserLock
                curElement.Version = Version_
                curElement.Phase = Phase_
                curElement.Update
            End If
        Else
            curElement.Version = Version_
            curElement.Phase = Phase_
            curElement.Update
        End If
    Next

    repository.RefreshModelView selectedDiagram.DiagramID
    MsgBox "Diagram elements updated successfully!", vbInformation + vbOKOnly, "Info"
End Sub

' Main function
Sub Main()
	Repository.EnsureOutputVisible "Script"
    UpdateVersionAndPhaseDialog repository
End Sub

' Call the main function
Main
