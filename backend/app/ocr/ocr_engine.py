from __future__ import annotations

import cv2
import pytesseract

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class OCREngine:
    
    # OCR processing using Tesseract.

    DEFAULT_CONFIG = (
        "--oem 3 "
        "--psm 6"
    )

    @staticmethod
    def recognize(
        image_data: ImageData,
        config: str | None = None,
    ) -> list:
        
        # Perform OCR on every validated cell.

        logger.info(
            "Starting OCR..."
        )

        if image_data.valid_cells is None or len(image_data.valid_cells) == 0:
            raise ImageProcessingError(
                "OCR failed: 0 validated cells are available for text recognition. "
                "Ensure cell extraction and validation stages completed successfully."
            )

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        if not OCREngine.available():
            raise ImageProcessingError(
                "Tesseract OCR is not installed or could not be found in the system PATH or common directories. "
                "Please download and install Tesseract OCR (from https://github.com/UB-Mannheim/tesseract/wiki) "
                "and ensure the installation directory is added to your environment variables."
            )

        results = []

        for cell in image_data.valid_cells:

            if not cell.get("has_text", True):
                # Skip empty cells
                result = {
                    "id": cell["id"],
                    "row": cell["row"],
                    "column": cell["column"],
                    "text": "",
                    "confidence": 0.0,
                }
                cell["text"] = ""
                cell["confidence"] = 0.0
                results.append(result)
                continue

            image = cell["image"]

            try:
                text = pytesseract.image_to_string(
                    image,
                    config=config,
                ).strip()

                confidence = OCREngine.confidence(
                    image,
                    config,
                )
            except Exception as e:
                raise ImageProcessingError(
                    f"Tesseract OCR execution failed for cell {cell['id']}: {str(e)}"
                ) from e

            result = {

                "id": cell["id"],

                "row": cell["row"],

                "column": cell["column"],

                "text": text,

                "confidence": confidence,

            }

            cell["text"] = text

            cell["confidence"] = confidence

            results.append(result)

        image_data.ocr_results = results

        image_data.recognized_text = [

            r["text"]

            for r in results

        ]

        image_data.processing_history[
            "OCR"
        ] = len(results)

        image_data.set_stage(
            "OCR"
        )

        logger.info(
            "%d OCR results generated.",
            len(results),
        )

        return results

    @staticmethod
    def recognize_single(
        image,
        config: str | None = None,
    ) -> str:
        
        # OCR for a single image.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        if not OCREngine.available():
            return ""

        return pytesseract.image_to_string(
            image,
            config=config,
        ).strip()

    @staticmethod
    def confidence(
        image,
        config: str | None = None,
    ) -> float:
        
        # Calculate average OCR confidence.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        if not OCREngine.available():
            return 0.0

        data = pytesseract.image_to_data(

            image,

            config=config,

            output_type=
            pytesseract.Output.DICT,

        )

        scores = []

        for value in data["conf"]:

            try:

                score = float(value)

                if score >= 0:

                    scores.append(score)

            except ValueError:

                continue

        if not scores:

            return 0.0

        return round(

            sum(scores) / len(scores),

            2,

        )

    @staticmethod
    def recognize_with_data(
        image,
        config: str | None = None,
    ) -> dict:
        
        # Return OCR data dictionary.

        if config is None:

            config = OCREngine.DEFAULT_CONFIG

        if not OCREngine.available():
            return {}

        return pytesseract.image_to_data(

            image,

            config=config,

            output_type=
            pytesseract.Output.DICT,

        )

    @staticmethod
    def set_tesseract_path(
        executable: str,
    ) -> None:
        
        # Set Tesseract executable path.

        pytesseract.pytesseract.tesseract_cmd = (
            executable
        )

        logger.info(
            "Tesseract path configured."
        )

    @staticmethod
    def available(
    ) -> bool:
        
        # Check whether Tesseract is available. Auto-configures path on Windows.

        try:

            pytesseract.get_tesseract_version()

            return True

        except Exception:

            pass

        import shutil
        import os
        from pathlib import Path

        in_path = shutil.which("tesseract")

        if in_path:

            pytesseract.pytesseract.tesseract_cmd = in_path

            try:

                pytesseract.get_tesseract_version()

                return True

            except Exception:

                pass

        username = os.environ.get("USERNAME", "user")

        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe",
            f"C:\\Users\\{username}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe",
        ]

        for p_str in common_paths:

            p = Path(p_str)

            if p.exists():

                pytesseract.pytesseract.tesseract_cmd = str(p)

                try:

                    pytesseract.get_tesseract_version()

                    logger.info(f"Auto-configured Tesseract path: {p}")

                    return True

                except Exception:

                    pass

        return False

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset OCR results.

        image_data.ocr_results = None

        image_data.recognized_text = None

        image_data.processing_history.pop(

            "OCR",

            None,

        )

        logger.info(
            "OCR reset."
        )