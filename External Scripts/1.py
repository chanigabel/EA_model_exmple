//The Add-in, written by Chany Jacobs, last modified - 25/07/24, 

using System;
using System.Linq;
using System.Collections.Generic;
using System.Windows.Forms;
using EA;
using ACTLEAaddin;

namespace MyAddin
{
    public class MyAddinClass : EAAddinBase
    {
        private new const string menuHeader = "-&ACTLAddin";
        private const string menuMoveElement = "&Move Element";

        public override string EA_Connect(EA.Repository Repository)
        {
            return base.EA_Connect(Repository);
        }

        public override object EA_GetMenuItems(EA.Repository repository, string location, string menuName)
        {
            switch (menuName)
            {
                case "":
                    return menuHeader;
                case menuHeader:
                    return new string[] { menuMoveElement };
                default:
                    return string.Empty;
            }
        }

        public override void EA_MenuClick(EA.Repository repository, string location, string menuName, string itemName)
        {
            if (itemName == menuMoveElement)
            {
                MoveElementToPackage(repository);
            }
        }

        private void MoveElementToPackage(EA.Repository repository)
        {
            EA.Element selectedElement = repository.GetTreeSelectedObject() as EA.Element;
            if (selectedElement == null)
            {
                MessageBox.Show("No element selected.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            int elementId = selectedElement.ElementID;
            var packages = GetPackages(repository);
            string selectedPackageId = ShowPackageSelectionDialog(packages);

            if (string.IsNullOrEmpty(selectedPackageId))
            {
                MessageBox.Show("No package selected.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                repository.Execute($"UPDATE t_object SET Package_ID = {selectedPackageId} WHERE Object_ID = {elementId}");
                repository.RefreshModelView(0);
                MessageBox.Show("Element moved successfully.");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to move element: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private List<EA.Package> GetPackages(Repository repository)
        {
            var packages = new List<EA.Package>();
            foreach (EA.Package package in repository.Models)
            {
                packages.Add(package);
                packages.AddRange(GetSubPackages(package));
            }
            return packages;
        }

        private List<EA.Package> GetSubPackages(EA.Package parentPackage)
        {
            var subPackages = new List<EA.Package>();
            foreach (EA.Package subPackage in parentPackage.Packages)
            {
                subPackages.Add(subPackage);
                subPackages.AddRange(GetSubPackages(subPackage));
            }
            return subPackages;
        }

        private string ShowPackageSelectionDialog(List<EA.Package> packages)
        {
            var form = new PackageSelectionForm(packages);
            form.ShowDialog();
            return form.SelectedPackageId;
        }

        public override void EA_Disconnect()
        {
            GC.Collect();
            GC.WaitForPendingFinalizers();
        }
    }

    public class PackageSelectionForm : Form
    {
        public string SelectedPackageId { get; private set; }

        private TreeView tree;
        private Button selectButton;

        public PackageSelectionForm(List<EA.Package> packages)
        {
            Text = "Select Target Package";

            tree = new TreeView();
            tree.Dock = DockStyle.Fill;
            tree.Nodes.AddRange(CreateTreeNodes(packages));

            selectButton = new Button
            {
                Text = "Select",
                Dock = DockStyle.Bottom
            };
            selectButton.Click += OnSelectButtonClick;

            Controls.Add(tree);
            Controls.Add(selectButton);
        }

        private TreeNode[] CreateTreeNodes(List<EA.Package> packages)
        {
            var nodes = new List<TreeNode>();
            foreach (var package in packages.Where(p => p.ParentID == 0))
            {
                var node = new TreeNode(package.Name) { Tag = package.PackageID };
                nodes.Add(node);
                AddSubNodes(node, packages);
            }
            return nodes.ToArray();
        }

        private void AddSubNodes(TreeNode parentNode, List<EA.Package> packages)
        {
            foreach (var package in packages.Where(p => p.ParentID == (int)parentNode.Tag))
            {
                var node = new TreeNode(package.Name) { Tag = package.PackageID };
                parentNode.Nodes.Add(node);
                AddSubNodes(node, packages);
            }
        }

        private void OnSelectButtonClick(object sender, EventArgs e)
        {
            var selectedNode = tree.SelectedNode;
            if (selectedNode != null)
            {
                SelectedPackageId = selectedNode.Tag.ToString();
                DialogResult = DialogResult.OK;
                Close();
            }
            else
            {
                MessageBox.Show("No package selected.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
