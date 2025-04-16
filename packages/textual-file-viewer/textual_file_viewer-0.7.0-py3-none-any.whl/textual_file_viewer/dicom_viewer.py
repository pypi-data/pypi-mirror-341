import datetime
from pathlib import Path
from typing import cast

import dateutil.parser
import numpy as np
import pydicom
from pydicom.errors import InvalidDicomError
from pydicom.pixel_data_handlers import util
from textual.app import ComposeResult
from textual.widgets import Static, TabPane, TabbedContent

from textual_file_viewer.dicom_tree import DicomTree
from textual_file_viewer.image_viewer import ImageViewer

SUPPORTED_PHOTOMETRIC_INTERPRETATIONS = {'MONOCHROME1', 'MONOCHROME2', 'YBR_FULL_422'}


def create_top_left_text(dataset: pydicom.Dataset) -> list[str]:
    return [
        str(dataset.PatientName),
        str(dataset.PatientID),
        dateutil.parser.parse(dataset.PatientBirthDate).strftime("%d-%b-%Y"),
        str(dataset.StudyDescription),
        str(dataset.SeriesDescription),
    ]


def create_top_right_text(dataset: pydicom.Dataset) -> list[str]:
    study_time = datetime.datetime.strptime(dataset.StudyTime, "%H%M%S")
    return [
        str(dataset.InstitutionName),
        str(dataset.ManufacturerModelName),
        f'{dateutil.parser.parse(dataset.StudyDate).strftime("%d-%b-%Y")} {study_time.strftime("%H:%M:%S")}']


def create_bottom_left_text(dataset: pydicom.Dataset) -> list[str]:
    return [
        f'ST: {dataset.get("SliceThickness", 0.0)} mm, SL: {dataset.get("SliceLocation", 0.0):.3f}',
        str(dataset.Modality),
        f'Series: {dataset.SeriesNumber}',
    ]


def create_bottom_right_text(dataset: pydicom.Dataset) -> list[str]:
    return [f'{dataset.Rows} x {dataset.Columns}',
            f'{dataset.PixelSpacing[0]:.3f} mm x {dataset.PixelSpacing[1]:.3f} mm', ]


class DicomViewer(Static):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with TabbedContent(id='dicom_viewer'):
            with TabPane('Image', id='tab_image'):
                yield ImageViewer()
            with TabPane('Tags', id='tab_tags'):
                yield DicomTree(id='dicom_tree')

    def load_dicom(self, filename: Path) -> None:
        try:
            dataset = cast(pydicom.Dataset, pydicom.dcmread(filename))
        except InvalidDicomError:
            return

        self.query_one(DicomTree).set_dataset(dataset)

        if 'PhotometricInterpretation' not in dataset:
            self.notify(title='Unable to show image.',
                        message='DICOM dataset has no "PhotometricInterpretation" tag.')
            return

        if dataset.PhotometricInterpretation not in SUPPORTED_PHOTOMETRIC_INTERPRETATIONS:
            self.notify(message=f'Only {" ".join(SUPPORTED_PHOTOMETRIC_INTERPRETATIONS)} are supported',
                        title='No image view',
                        severity='warning')
            return

        np_array = dataset.pixel_array

        match dataset.PhotometricInterpretation:
            case 'MONOCHROME1':
                # minimum is white, maximum is black
                # (https://dicom.innolitics.com/ciods/ct-image/image-pixel/00280004)
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(np_array, dataset)
                minimum, maximum = np.amin(np_array), np.amax(np_array)
                np_array = (maximum - np_array) * 255.0 / (maximum - minimum)
            case 'MONOCHROME2':
                center, width = dataset.WindowCenter, dataset.WindowWidth
                minimum, maximum = center - width / 2, center + width / 2
                np_array[np_array < minimum] = minimum
                np_array[np_array > maximum] = maximum
                np_array = (np_array - minimum) * 255.0 / (maximum - minimum)
            case 'YBR_FULL_422':
                np_array = util.convert_color_space(np_array, 'YBR_FULL', 'RGB')
            case _:
                pass

        image_viewer = self.query_one(ImageViewer)

        try:
            image_viewer.text_top_left = '\n'.join(create_top_left_text(dataset))
        except (ValueError, AttributeError):
            pass

        try:
            image_viewer.text_top_right = '\n'.join(create_top_right_text(dataset))
        except (ValueError, AttributeError):
            pass

        try:
            image_viewer.text_bottom_left = '\n'.join(create_bottom_left_text(dataset))
        except (ValueError, AttributeError):
            pass

        try:
            image_viewer.text_bottom_right = '\n'.join(create_bottom_right_text(dataset))
        except (ValueError, AttributeError):
            pass

        self.query_one(ImageViewer).set_array(np_array)
