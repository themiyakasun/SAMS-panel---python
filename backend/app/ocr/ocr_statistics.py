from __future__ import annotations

import statistics

from app.models.image_data import ImageData
from app.utils.logger import logger


class OCRStatistics:

    @staticmethod
    def calculate(
        image_data: ImageData,
    ) -> dict:
        
        # Calculate OCR statistics.

        if image_data.ocr_results is None:

            stats = {

                "Total Cells": 0,
                "Recognized Cells": 0,
                "Empty Cells": 0,
                "Average Confidence": 0.0,
                "Minimum Confidence": 0.0,
                "Maximum Confidence": 0.0,
                "High Confidence": 0,
                "Medium Confidence": 0,
                "Low Confidence": 0,
                "Recognition Rate (%)": 0.0,

            }

            image_data.ocr_statistics = stats

            return stats

        total = len(image_data.ocr_results)

        recognized = 0

        confidences = []

        high = 0
        medium = 0
        low = 0

        for result in image_data.ocr_results:

            text = result.get(
                "clean_text",
                result.get("text", ""),
            ).strip()

            if text:

                recognized += 1

            confidence = float(
                result.get(
                    "confidence",
                    0.0,
                )
            )

            confidences.append(
                confidence
            )

            level = result.get(
                "confidence_level",
                "Low",
            )

            if level == "High":

                high += 1

            elif level == "Medium":

                medium += 1

            else:

                low += 1

        stats = {

            "Total Cells": total,

            "Recognized Cells": recognized,

            "Empty Cells":
                total - recognized,

            "Recognition Rate (%)":

                round(
                    recognized /
                    total * 100,
                    2,
                ) if total else 0.0,

            "Average Confidence":

                round(
                    statistics.mean(
                        confidences
                    ),
                    2,
                ) if confidences else 0.0,

            "Minimum Confidence":

                round(
                    min(confidences),
                    2,
                ) if confidences else 0.0,

            "Maximum Confidence":

                round(
                    max(confidences),
                    2,
                ) if confidences else 0.0,

            "Median Confidence":

                round(
                    statistics.median(
                        confidences
                    ),
                    2,
                ) if confidences else 0.0,

            "Confidence Std Dev":

                round(
                    statistics.pstdev(
                        confidences
                    ),
                    2,
                ) if len(confidences) > 1 else 0.0,

            "High Confidence":
                high,

            "Medium Confidence":
                medium,

            "Low Confidence":
                low,

        }

        image_data.ocr_statistics = stats

        logger.info(
            "OCR statistics calculated."
        )

        return stats

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> str:
        
        # Return formatted summary.

        stats = OCRStatistics.calculate(
            image_data
        )

        return (
            "\n"
            "========== OCR Statistics ==========\n"
            f"Total Cells           : {stats['Total Cells']}\n"
            f"Recognized Cells      : {stats['Recognized Cells']}\n"
            f"Empty Cells           : {stats['Empty Cells']}\n"
            f"Recognition Rate (%)  : {stats['Recognition Rate (%)']}\n"
            f"Average Confidence    : {stats['Average Confidence']}\n"
            f"Minimum Confidence    : {stats['Minimum Confidence']}\n"
            f"Maximum Confidence    : {stats['Maximum Confidence']}\n"
            f"Median Confidence     : {stats['Median Confidence']}\n"
            f"Confidence Std Dev    : {stats['Confidence Std Dev']}\n"
            f"High Confidence       : {stats['High Confidence']}\n"
            f"Medium Confidence     : {stats['Medium Confidence']}\n"
            f"Low Confidence        : {stats['Low Confidence']}\n"
        )

    @staticmethod
    def print(
        image_data: ImageData,
    ) -> None:
        
        # Print OCR statistics.

        print(
            OCRStatistics.summary(
                image_data
            )
        )

    @staticmethod
    def export(
        image_data: ImageData,
    ) -> dict:
        
        # Return cached statistics.

        if image_data.ocr_statistics is None:

            return OCRStatistics.calculate(
                image_data
            )

        return image_data.ocr_statistics

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset OCR statistics.

        image_data.ocr_statistics = None

        logger.info(
            "OCR statistics reset."
        )