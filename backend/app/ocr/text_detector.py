from __future__ import annotations

import cv2
import numpy as np

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class TextDetector:
    
    # Detect whether cells contain readable text.

    MIN_FOREGROUND_RATIO = 0.01
    MAX_FOREGROUND_RATIO = 0.95

    @staticmethod
    def detect(image_data: ImageData) -> list:
        
        # Detect text in every validated cell.

        logger.info(
            "Detecting text regions..."
        )

        if image_data.valid_cells is None:

            raise ImageProcessingError(
                "Validated cells unavailable."
            )

        detected = []

        for cell in image_data.valid_cells:

            image = cell["image"]

            has_text = TextDetector.has_text(
                image
            )

            cell["has_text"] = has_text

            if has_text:

                detected.append(cell)

        logger.info(
            "%d cells contain text.",
            len(detected),
        )

        return detected

    @staticmethod
    def has_text(
        image: np.ndarray,
    ) -> bool:
        
        # Determine whether an image contains text.

        if image is None:

            return False

        if image.size == 0:

            return False

        if len(image.shape) == 3:

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY,
            )

        else:

            gray = image.copy()

        _, binary = cv2.threshold(

            gray,

            0,

            255,

            cv2.THRESH_BINARY_INV
            +
            cv2.THRESH_OTSU,

        )

        foreground = cv2.countNonZero(
            binary
        )

        total = binary.shape[0] * binary.shape[1]

        ratio = foreground / total

        return (

            TextDetector.MIN_FOREGROUND_RATIO

            <= ratio

            <=

            TextDetector.MAX_FOREGROUND_RATIO

        )

    @staticmethod
    def foreground_ratio(
        image: np.ndarray,
    ) -> float:
        
        # Calculate foreground pixel ratio.

        if len(image.shape) == 3:

            gray = cv2.cvtColor(

                image,

                cv2.COLOR_BGR2GRAY,

            )

        else:

            gray = image.copy()

        _, binary = cv2.threshold(

            gray,

            0,

            255,

            cv2.THRESH_BINARY_INV
            +
            cv2.THRESH_OTSU,

        )

        foreground = cv2.countNonZero(
            binary
        )

        total = binary.shape[0] * binary.shape[1]

        return round(

            foreground / total,

            4,

        )

    @staticmethod
    def empty_cells(
        image_data: ImageData,
    ) -> list:
        
        # Return cells without text.

        if image_data.valid_cells is None:

            return []

        return [

            cell

            for cell in image_data.valid_cells

            if not cell.get(
                "has_text",
                False,
            )

        ]

    @staticmethod
    def text_cells(
        image_data: ImageData,
    ) -> list:
        
        # Return cells containing text.

        if image_data.valid_cells is None:

            return []

        return [

            cell

            for cell in image_data.valid_cells

            if cell.get(
                "has_text",
                False,
            )

        ]

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Detection statistics.

        if image_data.valid_cells is None:

            return {

                "Total Cells": 0,
                "Cells with Text": 0,
                "Empty Cells": 0,

            }

        total = len(
            image_data.valid_cells
        )

        detected = len(

            TextDetector.text_cells(
                image_data
            )

        )

        return {

            "Total Cells": total,

            "Cells with Text": detected,

            "Empty Cells": total - detected,

            "Detection Rate (%)": round(

                detected / total * 100,

                2,

            ) if total else 0,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset text detection.

        if image_data.valid_cells:

            for cell in image_data.valid_cells:

                cell.pop(
                    "has_text",
                    None,
                )

        logger.info(
            "Text detector reset."
        )