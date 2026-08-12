import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.preprocessing.image_loader import ImageLoader

from app.services.perspective_service import PerspectiveService
from app.services.grayscale_service import GrayscaleService
from app.services.enhancement_service import EnhancementService
from app.services.threshold_service import ThresholdService
from app.services.table_service import TableService
from app.services.extraction_service import ExtractionService
from app.services.ocr_service import OCRService

from app.visualization.ocr_visualizer import OCRVisualizer
from app.visualization.text_visualizer import TextVisualizer


def main():

    image_path = Path(
        "data/images/1.jpeg"
    )

    print("\nLoading image...")

    image_data = ImageLoader.load(
        image_path
    )

    print("Perspective correction...")
    PerspectiveService.process(
        image_data
    )

    print("Grayscale conversion...")
    GrayscaleService.process(
        image_data
    )

    print("Image enhancement...")
    EnhancementService.process(
        image_data
    )

    print("Thresholding...")
    ThresholdService.process(
        image_data
    )

    print("Table detection...")
    TableService.process(
        image_data
    )

    print("Cell extraction...")
    ExtractionService.process(
        image_data
    )

    print("OCR processing...")
    OCRService.process(
        image_data
    )

    print("\nOCR Statistics")

    print(
        OCRService.summary(
            image_data
        )
    )

    print(
        "\nRecognized Results:"
    )

    TextVisualizer.print_results(
        image_data
    )

    print(
        "\nSummary:"
    )

    TextVisualizer.print_summary(
        image_data
    )

    print(
        "\nDisplaying first OCR result..."
    )

    OCRVisualizer.show(
        image_data,
        0,
    )

    print(
        "Displaying OCR grid..."
    )

    OCRVisualizer.grid(
        image_data
    )

    print(
        "Displaying OCR comparison..."
    )

    OCRVisualizer.comparison(
        image_data,
        0,
    )

    OCRVisualizer.print_summary(
        image_data
    )

    output_directory = Path(
        "results/ocr"
    )

    print(
        "\nExporting OCR results..."
    )

    OCRVisualizer.save_results(
        image_data,
        output_directory,
    )

    TextVisualizer.export_csv(
        image_data,
        output_directory /
        "ocr_results.csv",
    )

    TextVisualizer.export_text(
        image_data,
        output_directory /
        "recognized_text.txt",
    )

    print(
        "\nPhase 9 completed successfully."
    )


if __name__ == "__main__":

    main()