Option Explicit
'AddOrUpdateAttributeDB2ColumnNameTagValue
' The script, adapted to VBScript by Chany Jacobs, is designed to add or update DB2ColumnName Tag Value 
' of classes' attributes of the selected diagram.
' Tested and worked on 04-30-2024
!INC Local Scripts.EAConstants-VBScript

Function createUppercaseTableName(tableName)
    Dim substr, i, char
    substr = ""
    For i = 1 To Len(tableName)
        char = Mid(tableName, i, 1)
        If IsUpperCase(char) Then
            If Len(substr) > 0 And Right(substr, 1) <> "" Then
                substr = substr & ""
            End If
            substr = substr & char
        Else
            substr = substr & UCase(char)
        End If
    Next
    createUppercaseTableName = substr
End Function



Function IsUpperCase(s)
    IsUpperCase = s = UCase(s)
End Function

Sub addOrUpdateTaggedValue(element, tagName, tagValue)
    Dim taggedValue, flag
    flag = False
    For Each taggedValue In element.TaggedValues
        If taggedValue.Name = tagName Then
            taggedValue.Value = tagValue
            taggedValue.Update
            flag = True
            Exit For
        End If
    Next

    If Not flag Then
        Dim newTag
        Set newTag = element.TaggedValues.AddNew(tagName, "String")
        newTag.Value = tagValue
        newTag.Update
    End If
End Sub

Sub addOrUpdateAttrTagValueDB2ColumnName(repository, dbName)
    Dim diagram, dialogResult, numLockedElements, numAddUpdateElements, diagramObject, element, attribute, newTagValue
    Set diagram = repository.GetCurrentDiagram()
    If diagram Is Nothing Then
        MsgBox "Please select a Diagram", vbExclamation, "Warning"
        Exit Sub
    End If

    dialogResult = MsgBox("This option adds or updates DB2ColumnName Tag Value of classes' attributes of the selected diagram. All diagram's classes have to be released prior and will be locked after." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Confirmation")
    If dialogResult <> vbYes Then Exit Sub

    numLockedElements = 0
    numAddUpdateElements = 0

    For Each diagramObject In diagram.DiagramObjects
        Set element = repository.GetElementByID(diagramObject.ElementID)
        If Not element Is Nothing Then
            If Not element.Locked Then
                numAddUpdateElements = numAddUpdateElements + 1
                element.ApplyUserLock
            
                For Each attribute In element.Attributes
                    newTagValue = createUppercaseTableName(attribute.Name)
                    addOrUpdateTaggedValue attribute, dbName, newTagValue
                Next
            Else
                numLockedElements = numLockedElements + 1
            End If
        End If
    Next

    If repository.IsSecurityEnabled Then
        MsgBox numLockedElements & " elements were locked before. " & numAddUpdateElements & " elements were locked and affected by you.", vbInformation, "Information"
    Else
        MsgBox "All eligible elements have been processed.", vbInformation, "Information"
    End If
End Sub

Sub Main()
    Repository.EnsureOutputVisible "Script"
    addOrUpdateAttrTagValueDB2ColumnName repository, "DB2ColumnName"
End Sub

Main
