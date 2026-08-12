from __future__ import annotations

import statistics

from app.models.image_data import ImageData
from app.utils.logger import logger


class ConfidenceAnalyzer:
    
    # Analyze OCR confidence values.

    HIGH_THRESHOLD = 85.0
    MEDIUM_THRESHOLD = 60.0

    @staticmethod
    def analyze(
        image_data: ImageData,
    ) -> dict:
        
        # Analyze OCR confidence.

        if image_data.ocr_results is None:

            return {}

        logger.info(
            "Analyzing OCR confidence..."
        )

        confidences = []

        high = 0
        medium = 0
        low = 0

        for result in image_data.ocr_results:

            confidence = float(
                result.get(
                    "confidence",
                    0.0,
                )
            )

            if confidence <= 1.0:
                confidence = confidence * 100.0
                result["confidence"] = confidence

            confidences.append(
                confidence
            )

            level = ConfidenceAnalyzer.level(
                confidence
            )

            result["confidence_level"] = level

            if level == "High":

                high += 1

            elif level == "Medium":

                medium += 1

            else:

                low += 1

        if not confidences:
            summary = {
                "Average Confidence": 0.0,
                "Minimum Confidence": 0.0,
                "Maximum Confidence": 0.0,
                "High Confidence": 0,
                "Medium Confidence": 0,
                "Low Confidence": 0,
            }
        else:
            summary = {
                "Average Confidence":
                    round(
                        statistics.mean(
                            confidences
                        ),
                        2,
                    ),
                "Minimum Confidence":
                    round(
                        min(confidences),
                        2,
                    ),
                "Maximum Confidence":
                    round(
                        max(confidences),
                        2,
                    ),
                "High Confidence":
                    high,
                "Medium Confidence":
                    medium,
                "Low Confidence":
                    low,
            }

        image_data.ocr_statistics = summary

        logger.info(
            "Confidence analysis completed."
        )

        return summary

    @staticmethod
    def level(
        confidence: float,
    ) -> str:
        
        # Classify confidence level.

        if confidence <= 1.0:
            confidence = confidence * 100.0

        if confidence >= ConfidenceAnalyzer.HIGH_THRESHOLD:

            return "High"

        if confidence >= ConfidenceAnalyzer.MEDIUM_THRESHOLD:

            return "Medium"

        return "Low"

    @staticmethod
    def high_confidence(
        image_data: ImageData,
    ) -> list:
        
        # Return high confidence results.

        if image_data.ocr_results is None:

            return []

        return [

            result

            for result in image_data.ocr_results

            if result.get(
                "confidence_level"
            ) == "High"

        ]

    @staticmethod
    def medium_confidence(
        image_data: ImageData,
    ) -> list:
        
        # Return medium confidence results.

        if image_data.ocr_results is None:

            return []

        return [

            result

            for result in image_data.ocr_results

            if result.get(
                "confidence_level"
            ) == "Medium"

        ]

    @staticmethod
    def low_confidence(
        image_data: ImageData,
    ) -> list:
        
        # Return low confidence results.

        if image_data.ocr_results is None:

            return []

        return [

            result

            for result in image_data.ocr_results

            if result.get(
                "confidence_level"
            ) == "Low"

        ]

    @staticmethod
    def average(
        image_data: ImageData,
    ) -> float:
        
        # Average OCR confidence.

        if image_data.ocr_results is None:

            return 0.0

        values = [

            result.get(
                "confidence",
                0.0,
            )

            for result in image_data.ocr_results

        ]

        if not values:

            return 0.0

        return round(

            statistics.mean(
                values
            ),

            2,

        )

    @staticmethod
    def needs_review(
        image_data: ImageData,
        threshold: float = 60.0,
    ) -> list:
        
        # Return OCR results requiring manual review.

        if image_data.ocr_results is None:

            return []

        return [

            result

            for result in image_data.ocr_results

            if result.get(
                "confidence",
                0.0,
            ) < threshold

        ]

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Return confidence statistics.

        if image_data.ocr_statistics is None:

            return ConfidenceAnalyzer.analyze(
                image_data
            )

        return image_data.ocr_statistics

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset confidence analysis.

        if image_data.ocr_results:

            for result in image_data.ocr_results:

                result.pop(
                    "confidence_level",
                    None,
                )

        image_data.ocr_statistics = None

        logger.info(
            "Confidence analyzer reset."
        )