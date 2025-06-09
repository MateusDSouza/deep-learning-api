from pydantic import BaseModel, Field, field_validator
from core.settings import languages


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=512)
    base_language: str
    final_language: str

    @field_validator("base_language", "final_language")
    def language_supported(cls, language):
        if language not in languages:
            raise ValueError(f"Unsupported language: {language}")
        return language


class TranslationResponse(BaseModel):
    translation: str
