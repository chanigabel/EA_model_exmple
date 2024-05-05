Option Explicit

!INC Local Scripts.EAConstants-VBScript

Sub ChangeStereotype(repository, stereotypeName)
    Dim selDiagram
    Set selDiagram = repository.GetCurrentDiagram()
    
    If selDiagram Is Nothing Then
        MsgBox "Please select a diagram."
        Exit Sub
    End If
    
    Dim lockedClassesCount
    lockedClassesCount = 0
    
    Dim diagramObject, element
    For Each diagramObject In selDiagram.DiagramObjects
        Set element = repository.GetElementByID(diagramObject.ElementID)
        If element.Type = "Class" Then
            If repository.IsSecurityEnabled And IsElementLocked(element.ElementGUID, repository) Then
                lockedClassesCount = lockedClassesCount + 1
            Else
                element.StereotypeEx = stereotypeName
                element.Stereotype = stereotypeName
                element.Update
            End If
        End If
    Next
    
    If lockedClassesCount > 0 Then
        MsgBox lockedClassesCount & " classes were locked and your changes did not affect them.", vbExclamation, "Tevel Addins: Change classes stereotype"
    Else
        MsgBox "It's done!", vbInformation, "Tevel Addins: Change classes stereotype"
    End If
End Sub

Sub OnSelectionChanged(repository, root, comboStereotypes)
    Dim selectedStereotype
    selectedStereotype = comboStereotypes.Value
    ChangeStereotype repository, selectedStereotype
    root.Quit
End Sub

Sub Main()
    Repository.EnsureOutputVisible "Script"
    Dim dialogResult
    If repository.IsSecurityEnabled Then
        dialogResult = MsgBox("This option changes stereotype of all diagram's classes. All diagram's classes have to be released prior and will be locked after." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Change classes stereotype")
    Else
        dialogResult = MsgBox("This option changes stereotype of all diagram's classes." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Change classes stereotype")
    End If
    
    If dialogResult = vbYes Then
        Dim root
        Set root = CreateObject("Scripting.FileSystemObject").GetFolder(".")
        Dim selectedStereotype
        selectedStereotype = FileDialog("Please select the file containing the stereotype name.")
        If selectedStereotype <> "" Then
            ChangeStereotype repository, selectedStereotype
        End If
    End If
End Sub

Main
