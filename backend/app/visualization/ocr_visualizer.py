from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from app.models.image_data import ImageData
from app.utils.exceptions import ImageProcessingError
from app.utils.logger import logger


class OCRVisualizer:
    
    # Visualize OCR results.

    @staticmethod
    def show(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Display a single OCR result.

        if image_data.ocr_results is None:

            logger.warning("OCR results unavailable for display.")
            return

        if (
            index < 0
            or
            index >= len(image_data.ocr_results)
        ):

            logger.warning("OCR result index out of range; no result shown.")
            return

        result = image_data.ocr_results[index]

        cell = image_data.valid_cells[index]

        image = cv2.cvtColor(

            cell["image"],

            cv2.COLOR_BGR2RGB,

        )

        plt.figure(figsize=(5, 5))

        plt.imshow(image)

        plt.title(

            f"Cell {result['id']}\n"

            f"{result.get('clean_text', result['text'])}\n"

            f"{result['confidence']:.2f}% "

            f"({result.get('confidence_level', 'Unknown')})"

        )

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def grid(
        image_data: ImageData,
        columns: int = 4,
    ) -> None:
        
        # Display OCR results in a grid.

        if image_data.ocr_results is None:

            logger.warning("OCR results unavailable for grid view.")
            return

        results = image_data.ocr_results

        rows = (

            len(results) + columns - 1

        ) // columns

        plt.figure(

            figsize=(

                columns * 4,

                rows * 4,

            )

        )

        for index, result in enumerate(results):

            plt.subplot(

                rows,

                columns,

                index + 1,

            )

            cell = image_data.valid_cells[index]

            image = cv2.cvtColor(

                cell["image"],

                cv2.COLOR_BGR2RGB,

            )

            plt.imshow(image)

            plt.title(

                f"{result.get('clean_text', result['text'])}\n"

                f"{result['confidence']:.0f}%"

            )

            plt.axis("off")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def comparison(
        image_data: ImageData,
        index: int,
    ) -> None:
        
        # Compare original cell with OCR output.

        if image_data.ocr_results is None:

            logger.warning("OCR results unavailable for comparison view.")
            return

        if index < 0 or index >= len(image_data.ocr_results):

            logger.warning("OCR result index out of range for comparison.")
            return

        result = image_data.ocr_results[index]

        cell = image_data.valid_cells[index]

        image = cv2.cvtColor(

            cell["image"],

            cv2.COLOR_BGR2RGB,

        )

        plt.figure(figsize=(9, 4))

        plt.subplot(1, 2, 1)

        plt.imshow(image)

        plt.title("Extracted Cell")

        plt.axis("off")

        plt.subplot(1, 2, 2)

        plt.axis("off")

        plt.text(

            0.05,

            0.90,

            f"Text : {result['text']}",

            fontsize=11,

        )

        plt.text(

            0.05,

            0.72,

            f"Clean : "

            f"{result.get('clean_text', '')}",

            fontsize=11,

        )

        plt.text(

            0.05,

            0.54,

            f"Confidence : "

            f"{result['confidence']:.2f}%",

            fontsize=11,

        )

        plt.text(

            0.05,

            0.36,

            f"Level : "

            f"{result.get('confidence_level', '')}",

            fontsize=11,

        )

        plt.title("OCR Result")

        plt.tight_layout()

        plt.show()

    @staticmethod
    def save_results(
        image_data: ImageData,
        output_directory: str | Path,
    ) -> None:
        
        # Save every OCR cell image.

        if image_data.ocr_results is None:

            logger.warning("OCR results unavailable for saving.")
            return

        output_directory = Path(
            output_directory
        )

        output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        for index, result in enumerate(

            image_data.ocr_results

        ):

            cell = image_data.valid_cells[index]

            filename = (

                f"ocr_"

                f"{result['id']:04d}.png"

            )

            cv2.imwrite(

                str(

                    output_directory /

                    filename

                ),

                cell["image"],

            )

        logger.info(
            "OCR images saved."
        )

    @staticmethod
    def print_summary(
        image_data: ImageData,
    ) -> None:
        
        # Print OCR summary.

        if image_data.ocr_statistics is None:

            print("No OCR statistics.")

            return

        print()

        print("=" * 55)

        print("OCR SUMMARY")

        print("=" * 55)

        for key, value in (

            image_data.ocr_statistics.items()

        ):

            print(

                f"{key:25}: {value}"

            )

        print()

    @staticmethod
    def information(
        image_data: ImageData,
    ) -> dict:
        
        # Return OCR information.

        if image_data.ocr_statistics is None:

            return {}

        return image_data.ocr_statistics