import copy
from pathlib import Path

import cv2
import pytesseract
from napari.utils import notifications
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
        self.prediction_tesseract = None

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

        self.btn_crop_roi = QPushButton("Extract Information")
        self.files_group.glayout.addWidget(self.btn_crop_roi, 2, 0, 1, 1)

        self.files_group = VHGroup("Output", orientation="G")
        self.widget_layout.addWidget(self.files_group.gbox)

        # self.output = QLineEdit()
        # self.output.setText(self.prediction_tesseract)
        # self.files_group.glayout.addWidget(self.output, 0, 0, 1, 1)

    def add_connections(self):
        """
        Connects GUI elements to functions to be executed when GUI elements are activated
        """
        self.btn_import_image.clicked.connect(self.on_click_select_image)
        self.btn_roi.clicked.connect(self.on_click_select_roi)
        self.btn_crop_roi.clicked.connect(self.on_click_crop_roi)

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

    def on_click_select_roi(self):
        """
        Interactively select region of interest
        Called: button "Select ROI"
        """
        self.roi_shape = []
        self.viewer.add_shapes(edge_color="red", name="ROI", edge_width=4)

    def on_click_crop_roi(self):
        self.roi_shape = self.viewer.layers["ROI"].data
        self.img = cv2.imread(self.image_path)
        self.ic = copy.deepcopy(self.img)

        self.cropped_ic_y0 = int(self.roi_shape[0][0][0])
        self.cropped_ic_x0 = int(self.roi_shape[0][0][1])
        self.cropped_ic_y1 = int(self.roi_shape[0][1][0])
        self.cropped_ic_x1 = int(self.roi_shape[0][1][1])
        self.cropped_ic_y2 = int(self.roi_shape[0][2][0])
        self.cropped_ic_x2 = int(self.roi_shape[0][2][1])
        self.cropped_ic_y3 = int(self.roi_shape[0][3][0])
        self.cropped_ic_x3 = int(self.roi_shape[0][3][1])

        self.cropped = self.ic[
            self.cropped_ic_y0 : self.cropped_ic_y2,
            self.cropped_ic_x0 : self.cropped_ic_x2,
        ]
        # cv2.imwrite("cropped_image.png", self.cropped)
        self.tesseract_configuration = "--psm 6"
        self.prediction_tesseract = pytesseract.image_to_string(
            self.cropped, config=self.tesseract_configuration
        )
        notifications.show_info(str(self.prediction_tesseract))

        return self.prediction_tesseract

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
