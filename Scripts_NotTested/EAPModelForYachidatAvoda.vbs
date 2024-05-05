Option Explicit
'EAPModelForYachidatAvoda
!INC Local Scripts.EAConstants-VBScript

' Function to create EAP hierarchy
Sub CreateEAPHierarchy(selPackage, repository, listPackageGUIDs, listPackageNames)
    If selPackage.ParentID = 0 Then
        Exit Sub
    End If
    
    Dim parentPackage
    Set parentPackage = repository.GetPackageByID(selPackage.ParentID)
    listPackageGUIDs.Add parentPackage.PackageGUID
    listPackageNames.Add parentPackage.Name
    MsgBox listPackageNames.Count
    Call CreateEAPHierarchy(parentPackage, repository, listPackageGUIDs, listPackageNames)
End Sub

' Function to check if package exists
Function IfPackageExist(repository, packageName, listPackageGUIDs)
    Dim curGUID
    For Each curGUID In listPackageGUIDs
        Dim curPackage
        Set curPackage = repository.GetPackageByGuid(curGUID)
        If curPackage.Name = packageName Then
            IfPackageExist = Array(True, curPackage)
            Exit Function
        End If
    Next
    
    IfPackageExist = Array(False, Nothing)
End Function

' Function to create EAP model
Sub CreateEAPModel(projectPath, listXmiPackage, repository, myProject)
    On Error Resume Next
    
    repository.OpenFile projectPath
    
    Dim models
    Set models = repository.Models
    models.DeleteAt 0, True
    
    Dim rootPackageName
    rootPackageName = listXmiPackage(0)(2)(UBound(listXmiPackage(0)(2)))
    Dim root
    Set root = models.AddNew(rootPackageName, "")
    root.Update
    
    Dim curPackage
    Set curPackage = root
    Dim listPackageGUIDs
    Set listPackageGUIDs = CreateObject("System.Collections.ArrayList")
    listPackageGUIDs.Add curPackage.PackageGUID
    
    Dim xmiPackage
    For Each xmiPackage In listXmiPackage
        Dim packageNames
        packageNames = xmiPackage(2)
        
        Dim packageIdx
        For packageIdx = UBound(packageNames) To 0 Step -1
            If packageNames(packageIdx) = rootPackageName Then
                ' Skip processing if the package name matches the root package name
                Exit For
            End If
            
            Dim isExist
            Dim tmpPackage
            Dim result
            result = IfPackageExist(repository, packageNames(packageIdx), listPackageGUIDs)
            isExist = result(0)
            Set tmpPackage = result(1)
            
            If Not isExist Then
                Set curPackage = curPackage.Packages.AddNew(packageNames(packageIdx), "")
                curPackage.Update
                curPackage.Packages.Refresh
                listPackageGUIDs.Add curPackage.PackageGUID
            Else
                Set curPackage = tmpPackage
            End If
        Next
        
        ' Import XMI file to current package
        myProject.ImportPackageXMI curPackage.PackageGUID, xmiPackage(0), 1, 1
    Next
    
    repository.RefreshModelView 0
    models.Refresh
    
    MsgBox "EAP model created and XMI files imported successfully.", vbInformation, "Info"

    On Error GoTo 0
End Sub


' Function to create diagram EAP
Sub CreateDiagramEAP()
    On Error Resume Next
    
    ' Connect to Enterprise Architect
    Repository.EnsureOutputVisible "Script"

    ' Get selected diagram
    Dim curDiagram
    Set curDiagram = repository.GetCurrentDiagram()

    If Not curDiagram Is Nothing Then
        Dim selPackage
        Set selPackage = repository.GetTreeSelectedPackage()

        ' Check if any package is selected
        If selPackage Is Nothing Then
            MsgBox "Please select a package.", vbExclamation, "Error"
            Exit Sub
        End If
        
        Dim flagIfPackageExist
        flagIfPackageExist = False
        
        Dim listPackageGUIDs
        Set listPackageGUIDs = CreateObject("System.Collections.ArrayList")
        
        Dim listXmiPackage
        Set listXmiPackage = CreateObject("System.Collections.ArrayList")
        
		Dim listPackageNames
        Set listPackageNames = CreateObject("System.Collections.ArrayList")
        
        ' Loop through diagram objects
        Dim curObject
        For Each curObject In curDiagram.DiagramObjects
            Dim selElement
            Set selElement = repository.GetElementByID(curObject.ElementID)
			
            If selElement.Type = "Package" Then
				
                flagIfPackageExist = True
                
                Dim xmiName
                xmiName = selPackage.Name & "_" & selElement.Name
                Dim fileName
                fileName = "C:\Temp\" & xmiName & ".xmi"
                
                Dim firstPackageID
                firstPackageID = selElement.PackageID
                Set selPackage = repository.GetPackageByID(firstPackageID)
                listPackageGUIDs.Add selPackage.PackageGUID
                listPackageNames.Add selPackage.Name
				continueProcess=MsgBox("listPackageNames.Count")
				If continueProcess = vbNo Then
						Exit Sub
				End If
                ' Create the list of its parent packages GUIDs
                Call CreateEAPHierarchy(selPackage, repository, listPackageGUIDs, listPackageNames)
                
                ' Create current XMI package
                If Not objFSO.FileExists(fileName) Then
                    ' Obtain the Project object
                    Dim myProject
                    Set myProject = repository.GetProjectInterface()
                    ' Call ExportPackageXMI from the Project object
                    myProject.ExportPackageXMI selElement.ElementGUID, 2, 1, -1, 0, 0, fileName
                End If
                
                ' Store information for further processing
                listXmiPackage.Add Array(fileName, listPackageGUIDs.ToArray(), listPackageNames.ToArray())
            End If
        Next
        
        listPackageGUIDs.Clear
        listPackageNames.Clear
        
        If flagIfPackageExist Then
            repository.CreateModel 0, "C:/Temp/" & curDiagram.Name & ".eap", 1
            MsgBox "EAP model created successfully.", vbInformation, "Info"
            myProject = repository.GetProjectInterface()
            ' Further process the EAP model
            Call CreateEAPModel("C:/Temp/" & curDiagram.Name & ".eap", listXmiPackage, repository, myProject)
        Else
            MsgBox "No packages are found in the selected diagram.", vbExclamation, "Error"
        End If
    Else
        MsgBox "Please select a diagram.", vbExclamation, "Error"
    End If
    
    On Error GoTo 0
End Sub

' Main function
Sub Main()
    Call CreateDiagramEAP()
End Sub

' Call the main function
Call Main