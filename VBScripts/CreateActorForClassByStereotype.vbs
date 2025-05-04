' The script, written by Chany Jacobs, 
' is designed to create to all the classes in specific stereotype in selected package - Actors 
' that connect to the class in realisation with the same name.
' Tested and worked on 01-05-24
Option Explicit
!INC Local Scripts.EAConstants-VBScript

Function actorExists(repository, stereotypeName)
    Dim sqlQuery
    sqlQuery = "SELECT e.Name FROM(( t_object e INNER JOIN t_connector c ON e.Object_ID = c.Start_Object_ID ) INNER JOIN t_object s ON c.End_Object_ID = s.Object_ID ) WHERE e.Object_Type='Actor' AND s.Stereotype = '" & stereotypeName & "' AND (c.Connector_Type = 'Realisation' OR c.Connector_Type ='Generalization')"

    Dim result
    result = repository.SQLQuery(sqlQuery)
    actorExists = result
End Function

' Function to create and add actors with a specific stereotype and realization connection
Sub createAndAddActors(repository, package, stereotypeName)
    Dim numActors
    numActors = 0
    If Not package Is Nothing Then
        Dim actorExistsResult
        actorExistsResult = actorExists(repository, stereotypeName)
		
		Dim xmlDoc
		Set xmlDoc = CreateObject("MSXML2.DOMDocument")
		xmlDoc.LoadXml(actorExistsResult)

		Dim rowNodes
		Set rowNodes = xmlDoc.SelectNodes("//Row/Name")

        Dim element
        For Each element In package.Elements
		
			Dim flag
			flag = False
			Dim row
			For Each row In rowNodes
				If row.text = element.Name Then
					flag = True
					Exit For
				End If
			Next
			
            If element.Stereotype = stereotypeName And (element.Type = "Class" Or element.Type = "Component") And Not flag Then
                Dim newActor
                Set newActor = package.Elements.AddNew(element.Name, "Actor")
                newActor.Update
                
                Dim connector
                Set connector = package.Connectors.AddNew("", "Realisation")
                connector.ClientID= newActor.ElementID
                connector.SupplierID = element.ElementID
                connector.Update
                
                numActors = numActors + 1
            End If
        Next
        
        Session.Output numActors & " Actors created and added successfully in package: " & package.Name
        
        Dim subPackage
        For Each subPackage In package.Packages
            createAndAddActors repository, subPackage, stereotypeName
        Next
    End If
End Sub

' Main function
Sub main()
    Repository.EnsureOutputVisible "Script"
    Dim package
    Set package = Repository.GetTreeSelectedPackage()
    
	If Not package Is Nothing Then
        Dim stereotypeName
        stereotypeName = InputBox("Please enter the stereotype (press Cancel to cancel): ", "Enter Stereotype", "Subsystem")
        
        If stereotypeName = "" Then
            MsgBox "Process cancelled."
        Else
            Dim continueProcess
            continueProcess = MsgBox("This operation may make changes to your model. Are you sure you want to continue?", vbYesNo + vbQuestion, "Warning")
            
            If continueProcess = vbYes Then
                createAndAddActors repository, package, stereotypeName
            Else
                MsgBox "Process cancelled."
            End If
        End If
    Else
        MsgBox "This script requires a package to be selected."
    End If
End Sub

' Call the main function
main
