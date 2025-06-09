from api.models.models import TranslationModel, TextField
from transformers import T5Tokenizer, T5ForConditionalGeneration

from api.schemas.schemas import TranslationRequest

tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512)
translator = T5ForConditionalGeneration.from_pretrained("t5-small")


## IMPORTANT METHOD
def store_translation(translation_request: TranslationRequest) -> int:
    model = TranslationModel(**translation_request.model_dump()).save()
    return model.id  # type: ignore


def create_payload(model: TranslationModel):
    return f"translate {model.base_language} to {model.final_language}: {model.text}"


## IMPORTANT METHOD
def run_translation(translation_record_id: int) -> None:
    # get translation using the id
    translation_model = get_translation_by_id(translation_record_id)
    # create payload
    prefix = create_payload(translation_model)
    # transform into numbers
    input_ids = tokenizer(prefix, return_tensors="pt").input_ids
    # execute translation
    outputs = translator.generate(input_ids, max_new_tokens=512)
    # from numbers back to text
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # using the retrieval object save the translation in the object
    translation_model.translation = translation
    # store the object in the database
    translation_model.save()


## IMPORTANT METHOD
def find_translation(translation_record_id: int):
    translation = get_translation_by_id(translation_record_id).translation

    if translation is None:
        translation = "Processing..."
    return translation


def get_translation_by_id(translation_record_id: int) -> TranslationModel:
    return TranslationModel.get_by_id(translation_record_id).translation


# refactor
def verify_translation(translation: TextField):
    pass
