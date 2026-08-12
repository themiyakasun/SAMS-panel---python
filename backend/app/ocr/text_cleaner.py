from __future__ import annotations

import re

from app.models.image_data import ImageData
from app.utils.logger import logger


class TextCleaner:
    
    # Clean OCR text.

    CHARACTER_REPLACEMENTS = {

        "|": "I",
        "¦": "I",
        "—": "-",
        "_": " ",
        "~": "",
        "`": "",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",

    }

    @staticmethod
    def clean(
        image_data: ImageData,
    ) -> list:
        
        # Clean every OCR result.

        if image_data.ocr_results is None:

            return []

        logger.info(
            "Cleaning OCR text..."
        )

        cleaned_results = []

        for result in image_data.ocr_results:

            text = result["text"]

            cleaned = TextCleaner.clean_text(
                text
            )

            result["clean_text"] = cleaned

            cleaned_results.append(result)

        image_data.recognized_text = [

            r["clean_text"]

            for r in cleaned_results

        ]

        logger.info(
            "OCR text cleaned."
        )

        return cleaned_results

    @staticmethod
    def clean_text(
        text: str,
    ) -> str:
        
        # Clean a single OCR string.

        if not text:

            return ""

        text = text.strip()

        for old, new in (

            TextCleaner
            .CHARACTER_REPLACEMENTS
            .items()

        ):

            text = text.replace(
                old,
                new,
            )

        text = re.sub(

            r"\s+",

            " ",

            text,

        )

        text = re.sub(

            r"[^\w\s\-\/]",

            "",

            text,

        )

        return text.strip()

    @staticmethod
    def uppercase(
        text: str,
    ) -> str:
        
        # Convert to uppercase.

        return text.upper()

    @staticmethod
    def lowercase(
        text: str,
    ) -> str:
        
        # Convert to lowercase.

        return text.lower()

    @staticmethod
    def remove_digits(
        text: str,
    ) -> str:
        
        # Remove numeric characters.

        return re.sub(

            r"\d",

            "",

            text,

        )

    @staticmethod
    def digits_only(
        text: str,
    ) -> str:
        
        # Keep only digits.

        return "".join(

            character

            for character in text

            if character.isdigit()

        )

    @staticmethod
    def letters_only(
        text: str,
    ) -> str:
        
        # Keep alphabetic characters.

        return "".join(

            character

            for character in text

            if character.isalpha()

        )

    @staticmethod
    def remove_extra_spaces(
        text: str,
    ) -> str:
        
        # Remove multiple spaces.

        return re.sub(

            r"\s+",

            " ",

            text,

        ).strip()

    @staticmethod
    def normalize_student_id(
        text: str,
    ) -> str:
        
        # Normalize student ID.

        return TextCleaner.digits_only(
            text
        )

    @staticmethod
    def normalize_name(
        text: str,
    ) -> str:
        
        # Normalize student name.

        text = TextCleaner.clean_text(
            text
        )

        text = TextCleaner.uppercase(
            text
        )

        return text

    @staticmethod
    def statistics(
        image_data: ImageData,
    ) -> dict:
        
        # Cleaning statistics.

        if image_data.ocr_results is None:

            return {

                "Processed": 0

            }

        total = len(
            image_data.ocr_results
        )

        empty = sum(

            1

            for result in image_data.ocr_results

            if result["clean_text"] == ""

        )

        return {

            "Processed": total,

            "Empty Results": empty,

            "Valid Results": total - empty,

        }

    @staticmethod
    def reset(
        image_data: ImageData,
    ) -> None:
        
        # Reset cleaned text.

        if image_data.ocr_results:

            for result in image_data.ocr_results:

                result.pop(
                    "clean_text",
                    None,
                )

        logger.info(
            "Text cleaner reset."
        )