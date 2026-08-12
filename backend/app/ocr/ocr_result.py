from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OCRResult:
    
    # Represents the OCR output of a single cell.

    cell_id: int

    row: int

    column: int

    text: str = ""

    clean_text: str = ""

    confidence: float = 0.0

    confidence_level: str = "Low"

    has_text: bool = False

    metadata: dict = field(
        default_factory=dict
    )

    @property
    def is_empty(self) -> bool:
        
        # True if no text was recognized.

        return self.clean_text == ""

    @property
    def is_high_confidence(self) -> bool:
        
        # High confidence result.

        return self.confidence_level == "High"

    @property
    def is_medium_confidence(self) -> bool:
        
        # Medium confidence result.

        return self.confidence_level == "Medium"

    @property
    def is_low_confidence(self) -> bool:
        
        # Low confidence result.

        return self.confidence_level == "Low"

    def to_dict(self) -> dict:
        
        # Convert to dictionary.

        return {

            "cell_id": self.cell_id,

            "row": self.row,

            "column": self.column,

            "text": self.text,

            "clean_text": self.clean_text,

            "confidence": self.confidence,

            "confidence_level": self.confidence_level,

            "has_text": self.has_text,

            "metadata": self.metadata,

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "OCRResult":
        
        # Create OCRResult from dictionary.

        return cls(

            cell_id=data.get(
                "cell_id",
                data.get("id", 0),
            ),

            row=data.get(
                "row",
                0,
            ),

            column=data.get(
                "column",
                0,
            ),

            text=data.get(
                "text",
                "",
            ),

            clean_text=data.get(
                "clean_text",
                "",
            ),

            confidence=float(
                data.get(
                    "confidence",
                    0.0,
                )
            ),

            confidence_level=data.get(
                "confidence_level",
                "Low",
            ),

            has_text=data.get(
                "has_text",
                False,
            ),

            metadata=data.get(
                "metadata",
                {},
            ),

        )

    def __str__(self) -> str:
        
        # String representation.

        return (

            f"OCRResult("

            f"cell={self.cell_id}, "

            f"row={self.row}, "

            f"column={self.column}, "

            f"text='{self.clean_text}', "

            f"confidence={self.confidence:.2f}, "

            f"level='{self.confidence_level}')"

        )

    def __repr__(self) -> str:
        
        # Developer representation.

        return self.__str__()