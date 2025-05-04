import win32com.client

def main():
    # Connect to EA
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
        print("EA is accessible.")
    except Exception as e:
        print("Error: Could not connect to EA:", str(e))
        return

    # Get the current diagram
    currentDiagram = repository.GetCurrentDiagram()
    if currentDiagram is None:
        print("No diagram is currently selected.")
        return

    print(f"Current diagram: {currentDiagram.Name}")

    # Iterate through all diagram objects to get connectors
    connectors = []
    for diagramObject in currentDiagram.DiagramObjects:
        element = repository.GetElementByID(diagramObject.ElementID)
        if element is not None:
            for connector in element.Connectors:
                connectors.append(connector)

    # Display the connectors
    if connectors:
        print(f"Found {len(connectors)} connectors in the diagram:")
        for connector in connectors:
            print(f"- Connector ID: {connector.ConnectorID}, Name: {connector.Name}, Type: {connector.Type}")
    else:
        print("No connectors found in the selected diagram.")

if __name__ == "__main__":
    main()
