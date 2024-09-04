// WSH script to interact with Enterprise Architect

function deleteTagValues(repository, element, tagsToDelete) {
    try {
        var propertyIdsToDelete = [];
        
        for (var i = 0; i < element.TaggedValues.Count; i++) {
            var taggedValue = element.TaggedValues.Item(i);
            var tagInfo = taggedValue.Name + ": " + taggedValue.Value;
            if (tagsToDelete.indexOf(tagInfo) > -1) {
                propertyIdsToDelete.push(taggedValue.PropertyID);
            }
        }

        if (propertyIdsToDelete.length > 0) {
            var ids = propertyIdsToDelete.join(", ");
            var sql = "DELETE FROM t_objectproperties WHERE PropertyID IN (" + ids + ")";
            repository.Execute(sql);
            element.Update();
            repository.RefreshModelView(0);
        }
    } catch (e) {
        WScript.Echo("Failed to delete tag values: " + e.message);
    }
}

function showChecklist(tagInfo, elementName, packageName) {
    var selectedTags = [];
    var input = WScript.StdIn;
    WScript.Echo("Which tag values from '" + elementName + "' in package '" + packageName + "' do you want to delete?");
    
    for (var i = 0; i < tagInfo.length; i++) {
        WScript.Echo("[" + i + "] " + tagInfo[i]);
    }
    WScript.Echo("Enter the indices of the tags to delete, separated by commas:");

    var indices = input.ReadLine().split(",");
    for (var j = 0; j < indices.length; j++) {
        var index = parseInt(indices[j].trim());
        if (!isNaN(index) && index >= 0 && index < tagInfo.length) {
            selectedTags.push(tagInfo[index]);
        }
    }

    return selectedTags;
}

function processPackage(repository, package) {
    for (var i = 0; i < package.Elements.Count; i++) {
        var element = package.Elements.Item(i);
        if (element.Type === "Requirement" && element.TaggedValues.Count > 0) {
            var tagInfo = [];
            for (var j = 0; j < element.TaggedValues.Count; j++) {
                var taggedValue = element.TaggedValues.Item(j);
                tagInfo.push(taggedValue.Name + ": " + taggedValue.Value);
            }

            if (tagInfo.length > 0) {
                var selectedTags = showChecklist(tagInfo, element.Name, package.Name);
                if (selectedTags.length === 0) {
                    WScript.Echo("Operation has been canceled.");
                    return;
                }
                deleteTagValues(repository, element, selectedTags);
            }
        }
    }

    for (var k = 0; k < package.Packages.Count; k++) {
        processPackage(repository, package.Packages.Item(k));
    }
}

function main() {
    try {
        var ea = new ActiveXObject("EA.App");
        var repository = ea.Repository;
    } catch (e) {
        WScript.Echo("Could not connect to EA: " + e.message);
        return;
    }

    var selectedPackage = repository.GetTreeSelectedPackage();
    if (!selectedPackage) {
        WScript.Echo("No package selected.");
        return;
    }

    processPackage(repository, selectedPackage);
    WScript.Echo("Tag values deletion process completed.");
}

main();
