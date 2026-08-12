from pathlib import Path
import csv

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class TextVisualizer:
    
    # Visualize OCR text results.

    @staticmethod
    def print_results(
        image_data: ImageData,
    ) -> None:
        
        # Print OCR results as a table.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        print()

        print("=" * 100)

        print(
            f"{'Cell':<8}"
            f"{'Row':<8}"
            f"{'Col':<8}"
            f"{'Confidence':<15}"
            f"{'Level':<12}"
            f"{'Recognized Text'}"
        )

        print("=" * 100)

        for result in image_data.ocr_results:

            print(

                f"{result['id']:<8}"

                f"{result['row']:<8}"

                f"{result['column']:<8}"

                f"{result['confidence']:<15.2f}"

                f"{result.get('confidence_level',''):<12}"

                f"{result.get('clean_text', result['text'])}"

            )

        print("=" * 100)

    @staticmethod
    def print_text_only(
        image_data: ImageData,
    ) -> None:
        
        # Print recognized text only.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        print()

        print("Recognized Text")

        print("-" * 40)

        for result in image_data.ocr_results:

            print(

                result.get(
                    "clean_text",
                    result["text"],
                )

            )

    @staticmethod
    def export_csv(
        image_data: ImageData,
        output_file: str | Path,
    ) -> None:
        
        # Export OCR results to CSV.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as csv_file:

            writer = csv.writer(csv_file)

            writer.writerow(

                [

                    "Cell ID",

                    "Row",

                    "Column",

                    "Text",

                    "Clean Text",

                    "Confidence",

                    "Confidence Level",

                ]

            )

            for result in image_data.ocr_results:

                writer.writerow(

                    [

                        result["id"],

                        result["row"],

                        result["column"],

                        result["text"],

                        result.get(
                            "clean_text",
                            "",
                        ),

                        result["confidence"],

                        result.get(
                            "confidence_level",
                            "",
                        ),

                    ]

                )

        logger.info(
            "OCR results exported to CSV."
        )

    @staticmethod
    def export_text(
        image_data: ImageData,
        output_file: str | Path,
    ) -> None:
        
        # Export recognized text.

        if image_data.ocr_results is None:

            raise ImageProcessingError(
                "OCR results unavailable."
            )

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(

            output_file,

            "w",

            encoding="utf-8",

        ) as file:

            for result in image_data.ocr_results:

                file.write(

                    result.get(
                        "clean_text",
                        result["text"],
                    )

                    + "\n"

                )

        logger.info(
            "OCR text exported."
        )

    @staticmethod
    def summary(
        image_data: ImageData,
    ) -> dict:
        
        # Return OCR summary.

        if image_data.ocr_results is None:

            return {}

        total = len(image_data.ocr_results)

        recognized = sum(

            1

            for result in image_data.ocr_results

            if result.get(
                "clean_text",
                result["text"],
            ).strip()

        )

        return {

            "Total Results": total,

            "Recognized": recognized,

            "Empty": total - recognized,

        }

    @staticmethod
    def print_summary(
        image_data: ImageData,
    ) -> None:
        
        # Print OCR summary.

        summary = TextVisualizer.summary(
            image_data
        )

        print()

        print("=" * 40)

        print("TEXT SUMMARY")

        print("=" * 40)

        for key, value in summary.items():

            print(

                f"{key:20}: {value}"

            )

        print()