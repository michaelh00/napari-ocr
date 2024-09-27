from pathlib import Path

from napari_guitils.gui_structures import VHGroup
from qtpy.QtWidgets import (
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class NapariOCRWidget(QWidget):

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.image_path = None

        self.widget_layout = QVBoxLayout()
        self.setLayout(self.widget_layout)

        self.create_tab()
        self.add_connections()

    def create_tab(self):
        """Generates the elements of the tab"""
        # generates and adds VHGroup to widget
        self.files_group = VHGroup("Actions", orientation="G")
        self.widget_layout.addWidget(self.files_group.gbox)

        # generates and adds Button to VHGroup
        self.btn_import_image = QPushButton("Select Image")
        self.files_group.glayout.addWidget(self.btn_import_image, 0, 0, 1, 1)

        self.btn_roi = QPushButton("Select ROI")
        self.files_group.glayout.addWidget(self.btn_roi, 1, 0, 1, 1)

    def add_connections(self):
        """
        Connects GUI elements to functions to be executed when GUI elements are activated
        """
        self.btn_import_image.clicked.connect(self.on_click_select_image)
        self.btn_roi.clicked.connect(self.on_click_select_roi)

    def on_click_select_image(self):
        """
        Interactively select image file
        Called: button "Select image"
        """
        image_path = QFileDialog.getOpenFileName(
            self, directory="src/napari_ocr/_data/"
        )[0]
        if image_path == "":
            return
        image_path = Path(image_path)
        if image_path.parent.suffix == ".png":
            image_path = image_path.parent
        self.set_paths(image_path)
        self.on_select_file()
        # self._on_click_add_main_roi()

    def on_click_select_roi(self):
        """
        Interactively select region of interest
        Called: button "Select ROI"
        """

    ### Helper functions
    def on_select_file(self):
        """
        Helper function used in:
        "on_click_select_image"
        """
        success = self.open_file()
        if not success:
            return False

    def set_paths(self, image_path):
        """
        Update image paths
        Helper function used in:
        "on_click_select_image"
        """

        self.image_path = Path(image_path)
        # self.image_path_display.setText(self.image_path.as_posix())

    def open_file(self):
        """
        Open file in napari
        Helper function used in:
        "on_select_file" (Helper function)
        """
        # clear existing layers.
        while len(self.viewer.layers) > 0:
            self.viewer.layers.clear()

        # if file list is empty stop here
        if self.image_path is None:
            return False

        # open image
        self.viewer.open(self.image_path)
        return True
