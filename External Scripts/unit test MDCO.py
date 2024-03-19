import unittest
from unittest.mock import MagicMock
from io import StringIO
from MasterDocumentConnectorsOperations import *

class TestDocumentationFunctions(unittest.TestCase):

    def setUp(self):
        self.ea = MagicMock()
        self.repository = MagicMock()
        self.ea.Repository = self.repository
        self.documents_package = MagicMock()
        self.repository.GetTreeSelectedPackage.return_value = self.documents_package

    def test_add_model_document_for_diagram(self):
        # Mocking required objects
        repository = self.repository
        master_document = MagicMock()
        diagram = MagicMock()
        name = "TestDocument"
        treepos = 1
        template = "TestTemplate"

        # Call the function
        add_model_document_for_diagram(repository, master_document, diagram, name, treepos, template)

        # Assertions
        self.assertTrue(repository.ReloadDiagram.called)
        self.assertTrue(diagram.DiagramObjects.AddNew.called)
        self.assertTrue(master_document.Elements.AddNew.called)
        self.assertTrue(diagram.DiagramObjects.AddNew.called)

    def test_add_master_document_with_details(self):
        # Mocking required objects
        repository = self.repository
        package_GUID = "test_GUID"
        document_name = "Test Document"
        document_version = "1.0"
        document_alias = "Alias"
        diagram_name = "Test Diagram"

        # Call the function
        result = add_master_document_with_details(repository, package_GUID, document_name, document_version, document_alias, diagram_name)

        # Assertions
        self.assertTrue(repository.GetPackageByGuid.called)
        self.assertTrue(result.Update.called)
        self.assertEqual(result.Alias, document_alias)
        self.assertEqual(result.Version, document_version)
        self.assertEqual(result.Element.Stereotype, "master document")
        self.assertTrue(result.Element.TaggedValues.AddNew.called)

    def test_make_master_document(self):
        # Mocking required objects
        repository = self.repository
        package_GUID = "test_GUID"
        document_version = "1.0"
        document_alias = "Alias"
        document_diagram_name = "Test Diagram"
        with unittest.mock.patch('builtins.input', side_effect=[document_version, document_alias, document_diagram_name]):
            # Call the function
            result = make_master_document(repository, package_GUID)

            # Assertions
            self.assertTrue(result.Update.called)

    def test_create_diagram(self):
        # Mocking required objects
        repository = self.repository
        package_guid = "test_GUID"
        diagram_name = "Test Diagram"
        diagram_type = "Test Type"

        # Call the function
        result = create_diagram(repository, package_guid, diagram_name, diagram_type)

        # Assertions
        self.assertTrue(repository.GetPackageByGuid.called)
        self.assertTrue(result.Update.called)

    def test_create_document(self):
        # Mocking required objects
        repository = self.repository
        documents_package_GUID = "test_GUID"
        master_document = MagicMock()
        master_document.PackageGUID = documents_package_GUID

        # Call the function
        with unittest.mock.patch('builtins.input', side_effect=["1.0", "Alias", "Test Diagram"]):
            create_document(repository, documents_package_GUID)

            # Assertions
            self.assertTrue(master_document.Update.called)
            self.assertTrue(repository.RefreshModelView.called)
            self.assertTrue(repository.ShowInProjectView.called)

    def test_main(self):
        # Mocking required objects
        ea = self.ea
        repository = self.repository
        documents_package = self.documents_package
        package_GUID = "test_GUID"

        # Call the function
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            with unittest.mock.patch('sys.argv', ['script_name']):
                main()

                # Assertions
                self.assertTrue(repository.GetTreeSelectedPackage.called)
                self.assertIn("Select the Master Document", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
