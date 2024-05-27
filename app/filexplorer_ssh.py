import paramiko
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir

class SSHExplorer(QWidget):
    def __init__(self, host, port, username, password, parent=None):
        super(SSHExplorer, self).__init__(parent)

        self.selected_item_path = None

        layout = QVBoxLayout()

        self.label = QLabel("Select a file or a folder:")
        layout.addWidget(self.label)

        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath('/')
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.tree_view.setModel(self.model)
        self.tree_view.setMinimumSize(500, 500)
        self.tree_view.setMaximumSize(1000, 800)
        layout.addWidget(self.tree_view)

        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(self.confirm_button)
        
        self.setLayout(layout)

        self.connect_to_ssh(host, port, username, password)

        self.setWindowTitle("SSH Explorer")
        self.setWindowIcon(QIcon('path_to_icon.png'))

    def connect_to_ssh(self, host, port, username, password):
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        self.tree_view.setRootIndex(self.model.index('/'))

    def confirm_selection(self):
        selected_indexes = self.tree_view.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            self.selected_item_path = self.model.filePath(selected_index)
            print(str(self.selected_item_path))
            QApplication.quit()
            return self.selected_item_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python ssh_explorer.py host port username password")
        sys.exit(1)
    host, port, username, password = sys.argv[1:]
    app = QApplication(sys.argv)
    window = SSHExplorer(host, int(port), username, password)
    window.show()
    sys.exit(app.exec_())