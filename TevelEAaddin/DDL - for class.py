import win32com.client
from All import *
#
def create_ddl_function(repository):
    cur_diagram = repository.GetCurrentDiagram() # current diagram
    if cur_diagram:
        col_object = cur_diagram.SelectedObjects # the selected objects in the diagram
        if col_object.Count != 0:
            sel_object = col_object.GetAt(0) # get the first selected object
            sel_element = repository.GetElementByID(sel_object.ElementID) # get the object by the id
            create_ddl_script(repository, sel_element) # call the function to create DDL script based on the selected element
        else:
            print("Please, select some object from the diagram.") # if not selected object
    else:
        print("Please, select diagram.") # if not selected diagram
#
def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    create_ddl_function(repository)


if __name__ == "__main__":
    main()
