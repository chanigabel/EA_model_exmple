Option Explicit

!INC Local Scripts.EAConstants-VBScript

Sub ReleaseUserLock(repository)
    Dim dialogResult
    dialogResult = MsgBox("This option opens the Release User Lock dialog box which enables releasing User Locks that EA could not release by itself." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Release User Lock")

    If dialogResult = vbYes Then
        ' Open the Release User Lock form
        ReleaseUserLockForm(repository)
    Else
        MsgBox "Operation cancelled.", vbInformation, "Cancelled"
    End If
End Sub

Sub ReleaseUserLockForm(repository)
    Dim form, listViewLockedElement, btnSelectAll, btnClearAll, btnRelease
    Set form = CreateObject("Scripting.Dictionary")

    ' Create form components
    Set listViewLockedElement = CreateObject("System.Windows.Forms.ListView")
    Set btnSelectAll = CreateObject("System.Windows.Forms.Button")
    Set btnClearAll = CreateObject("System.Windows.Forms.Button")
    Set btnRelease = CreateObject("System.Windows.Forms.Button")

    ' Set up form properties
    form("Text") = "Release User Lock"
    form("Width") = 479
    form("Height") = 388

    ' Initialize form controls
    listViewLockedElement.CheckBoxes = True
    listViewLockedElement.Location = New-Object System.Drawing.Point(12, 12)
    listViewLockedElement.Name = "listViewLockedElement"
    listViewLockedElement.Size = New-Object System.Drawing.Size(456, 319)
    listViewLockedElement.View = [System.Windows.Forms.View]::List

    btnSelectAll.Location = New-Object System.Drawing.Point(90, 345)
    btnSelectAll.Name = "btnSelectAll"
    btnSelectAll.Size = New-Object System.Drawing.Size(75, 29)
    btnSelectAll.Text = "Select All"

    btnClearAll.Location = New-Object System.Drawing.Point(180, 345)
    btnClearAll.Name = "btnClearAll"
    btnClearAll.Size = New-Object System.Drawing.Size(75, 29)
    btnClearAll.Text = "Clear All"

    btnRelease.Location = New-Object System.Drawing.Point(269, 345)
    btnRelease.Name = "btnRelease"
    btnRelease.Size = New-Object System.Drawing.Size(139, 29)
    btnRelease.Text = "Release User Lock"

    ' Add form controls to the form
    form.Add("listViewLockedElement", listViewLockedElement)
    form.Add("btnSelectAll", btnSelectAll)
    form.Add("btnClearAll", btnClearAll)
    form.Add("btnRelease", btnRelease)

    ' Set up event handlers
    AddHandler btnRelease.Click, {BindFirstArgument = repository, Method = ReleaseButtonClick}

    ' Show the form
    ShowForm(form)
End Sub

Sub ReleaseButtonClick(repository, sender, e)
    Dim listViewLockedElement, item, query, index
    Set listViewLockedElement = sender.Parent.Controls("listViewLockedElement")

    ' Execute the SQL query to release locks for selected elements
    For Each item In listViewLockedElement.Items
        If item.Checked Then
            query = "DELETE FROM t_seclocks WHERE EntityID = '" & item.SubItems(1).Text & "'"
            repository.Execute(query)
        End If
    Next

    ' Refresh the model
    repository.Models.Refresh()

    MsgBox "User locks released successfully.", vbInformation, "Success"
End Sub

Sub ShowForm(form)
    Dim assembly, type, instance
    Set assembly = LoadAssembly("System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089")
    Set type = assembly.GetType("System.Windows.Forms.Form")
    Set instance = Activator.CreateInstance(type)

    instance.Text = form("Text")
    instance.Width = form("Width")
    instance.Height = form("Height")

    For Each key In form.Keys
        instance.Controls.Add form(key)
    Next

    instance.ShowDialog()
End Sub

Function LoadAssembly(assemblyName)
    Dim assembly, loader
    Set loader = CreateObject("System.Reflection.AssemblyName")
    loader.Name = assemblyName
    Set assembly = System.Reflection.Assembly.Load(loader)
    Set LoadAssembly = assembly
End Function

Repository.EnsureOutputVisible "Script"
ReleaseUserLock repository
