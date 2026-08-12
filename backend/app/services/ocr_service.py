from __future__ import annotations

from app.models.image_data import ImageData

from app.ocr.confidence_analyzer import (
    ConfidenceAnalyzer,
)
from app.ocr.ocr_engine import OCREngine
from app.ocr.ocr_statistics import (
    OCRStatistics,
)
from app.ocr.text_cleaner import TextCleaner
from app.ocr.text_detector import TextDetector

from app.utils.exceptions import (
    ImageProcessingError,
)
from app.utils.logger import logger


class OCRService:
    
    # OCR processing service.

    @staticmethod
    def process(
        image_data: ImageData,
    ) -> list:
        
        # Execute the complete OCR pipeline.

        logger.info(
            "Starting OCR pipeline..."
        )

        TextDetector.detect(
            image_data
        )

        OCREngine.recognize(
            image_data
        )

        TextCleaner.clean(
            image_data
        )

        ConfidenceAnalyzer.analyze(
            image_data
        )

        OCRStatistics.calculate(
            image_data
        )

        logger.info(
            "OCR pipeline completed."
        )

        return image_data.ocr_results

    @staticmethod
    def detect_text(
        image_data: ImageData,
    ) -> list:
        
        # Detect cells containing text.

        return TextDetector.detect(
            image_data
        )

    @staticmethod
    def recognize(
        image_data: ImageData,
    ) -> list:
        
        # Execute OCR only.

        return OCREngine.recognize(
            image_data
        )

    @staticmethod
    def clean(
        image_data: ImageData,
    ) -> list:
        
        # Clean OCR text.

        return TextCleaner.clean(
            image_data
        )

    @staticmethod
    def analyze(
        image_data: ImageData,
    ) -> dict:
        
        # Analyze OCR confidence.

        return ConfidenceAnalyzer.analyze(
            image_data
        )

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return OCR statistics.

        return OCRStatistics.calculate(
            image_data
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return OCR summary.

        return OCRStatistics.summary(
            image_data
        )

    @staticmethod
    def count(
        image_data: ImageData,
    ) -> int:
        
        # Number of OCR results.

        if image_data.ocr_results is None:

            return 0

        return len(
            image_data.ocr_results
        )

    @staticmethod
    def get_result(
        image_data: ImageData,
        index: int,
    ):
        
        # Return a single OCR result.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        if (
            index < 0
            or
            index >= len(
                image_data.ocr_results
            )
        ):

            raise IndexError(
                "OCR result index out of range."
            )

        return image_data.ocr_results[
            index
        ]

    @staticmethod
    def text_only(
        image_data: ImageData,
    ) -> list:
        
        # Return recognized text only.

        if image_data.ocr_results is None:

            return []

        return [

            result.get(
                "clean_text",
                result.get(
                    "text",
                    "",
                ),
            )

            for result in image_data.ocr_results

        ]

    @staticmethod
    def review_required(
        image_data: ImageData,
        threshold: float = 60.0,
    ) -> list:
        
        # Return low-confidence OCR results.

        return ConfidenceAnalyzer.needs_review(
            image_data,
            threshold,
        )

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset OCR pipeline.

        OCREngine.reset(
            image_data
        )

        TextDetector.reset(
            image_data
        )

        TextCleaner.reset(
            image_data
        )

        ConfidenceAnalyzer.reset(
            image_data
        )

        OCRStatistics.reset(
            image_data
        )

        logger.info(
            "OCR service reset."
        )

    @staticmethod
    def validate_pipeline(
        image_data: ImageData,
    ) -> bool:
        
        # Verify OCR pipeline output.

        if image_data.ocr_results is None:

            return False

        if len(
            image_data.ocr_results
        ) == 0:

            return False

        return True