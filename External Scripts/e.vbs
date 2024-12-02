Option Explicit

' Main entry point
Sub Main()
    Dim eaApp, repository, selectedPackage
    On Error Resume Next
    Set eaApp = CreateObject("EA.App")
    If Err.Number <> 0 Then
        MsgBox "Could not connect to EA: " & Err.Description, vbCritical, "Error"
        Exit Sub
    End If
    On Error GoTo 0

    Set repository = eaApp.Repository
    Set selectedPackage = repository.GetTreeSelectedPackage()

    If selectedPackage Is Nothing Then
        MsgBox "No package selected.", vbCritical, "Error"
        Exit Sub
    End If

    ProcessPackage repository, selectedPackage

    MsgBox "Tag values deletion process completed.", vbInformation, "Completed"
End Sub

' Process all elements in a package and its sub-packages
Sub ProcessPackage(repository, package)
    Dim element, subPackage, allSelectedTags, selectedTags

    Set allSelectedTags = CreateObject("Scripting.Dictionary")

    For Each element In package.Elements
        If element.Type = "Requirement" And element.TaggedValues.Count > 0 Then
            Set selectedTags = AskToDeleteTags(element, package.Name)
            If selectedTags.Count > 0 Then
                allSelectedTags.Add element.ElementGUID, selectedTags
            End If
        End If
    Next

    For Each subPackage In package.Packages
        ProcessPackage repository, subPackage
    Next

    If allSelectedTags.Count > 0 Then
        ConfirmAndDelete repository, allSelectedTags
    End If
End Sub

' Ask the user if they want to delete each tag for an element
Function AskToDeleteTags(element, packageName)
    Dim tag, tagInfo, response, selectedTags
    Set selectedTags = CreateObject("Scripting.Dictionary")

    For Each tag In element.TaggedValues
        tagInfo = tag.Name & ": " & tag.Value
        response = MsgBox("Do you want to delete the tag '" & tagInfo & "' from '" & element.Name & "' in package '" & packageName & "'?", vbYesNo, "Delete Tag?")
        If response = vbYes Then
            selectedTags.Add tagInfo, tag.PropertyID
        End If
    Next

    Set AskToDeleteTags = selectedTags
End Function

' Confirm and delete the selected tags
Sub ConfirmAndDelete(repository, allSelectedTags)
    Dim confirmMessage, elementGUID, tags, tag, tagIDs, sql, response

    confirmMessage = "You have selected the following tags to delete:" & vbCrLf & vbCrLf

    For Each elementGUID In allSelectedTags.Keys
        confirmMessage = confirmMessage & "From element '" & repository.GetElementByGuid(elementGUID).Name & "':" & vbCrLf
        Set tags = allSelectedTags(elementGUID)
        For Each tag In tags.Keys
            confirmMessage = confirmMessage & "  - " & tag & vbCrLf
        Next
        confirmMessage = confirmMessage & vbCrLf
    Next

    confirmMessage = confirmMessage & "Are you sure you want to delete these tags?"

    response = MsgBox(confirmMessage, vbYesNo, "Confirm Deletion")
    If response = vbYes Then
        For Each elementGUID In allSelectedTags.Keys
            Set tags = allSelectedTags(elementGUID)
            tagIDs = ""
            For Each tag In tags.Items
                tagIDs = tagIDs & tag & ","
            Next
            If Len(tagIDs) > 0 Then
                tagIDs = Left(tagIDs, Len(tagIDs) - 1) ' Remove trailing comma
                sql = "DELETE FROM t_objectproperties WHERE PropertyID IN (" & tagIDs & ")"
                repository.Execute sql
            End If
        Next
        repository.RefreshModelView 0
    Else
        MsgBox "Tag deletion operation cancelled.", vbInformation, "Cancelled"
    End If
End Sub

' Entry point
Main
