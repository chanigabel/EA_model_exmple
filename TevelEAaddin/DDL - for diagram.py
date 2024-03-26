import win32com.client
from All import *


def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    create_diagram_ddl_function(repository)


if __name__ == "__main__":
    main()
