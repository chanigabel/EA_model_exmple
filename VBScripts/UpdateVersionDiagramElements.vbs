'UpdateVersionDiagramElements
'The script, written by Chany Jacobs, 
'This script update Version of Diagram Elements.
'To run you need to open diagram.
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

' Function to handle updating and version dialog
Sub UpdateVersionDialog(repository)
    Dim dialogResult
    Dim selDiagram
    Dim Version_
    Dim flag

    If repository.IsSecurityEnabled Then
        dialogResult = MsgBox("This option opens the Update and Version dialog box which enables updating a and a version of the selected diagram's elements which are not locked." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update and Version of Diagram Elements")
    Else
        dialogResult = MsgBox("This option opens the Update and Version dialog box which enables updating a and a version of the selected diagram's elements." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update and Version of Diagram Elements")
    End If

    If dialogResult = vbYes Then
        Set selDiagram = repository.GetCurrentDiagram()
        If Not selDiagram Is Nothing Then
            Version_ = InputBox("Enter the version:", "Update and Version")
            If Version_ <> "" Then
                flag = 0
                UpdateVersion repository, selDiagram, Version_, flag
            Else
                MsgBox "version cannot be empty.", vbExclamation, "Error"
            End If
        Else
            MsgBox "This script requires a diagram to be selected.", vbExclamation, "Error"
        End If
    End If
End Sub

' Function to update and version
Sub UpdateVersion(repository, selectedDiagram, Version_, flag)
    Dim curObject
    Dim curElement

    For Each curObject In selectedDiagram.DiagramObjects
        Set curElement = repository.GetElementByID(curObject.ElementID)
        If repository.IsSecurityEnabled Then
            If Not IsElementLocked(curElement.ElementGUID, repository) Then
                curElement.ApplyUserLock
                curElement.Version = Version_
                curElement.Update
            End If
        Else
            curElement.Version = Version_
            curElement.Update
        End If
    Next

    repository.RefreshModelView selectedDiagram.DiagramID
    MsgBox "Diagram elements updated successfully!", vbInformation + vbOKOnly, "Info"
End Sub

' Main function
Sub Main()
	Repository.EnsureOutputVisible "Script"
    UpdateVersionDialog repository
End Sub

' Call the main function
Main
