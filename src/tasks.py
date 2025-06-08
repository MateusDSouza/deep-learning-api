from models import TranslationModel
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512)
translator = T5ForConditionalGeneration.from_pretrained("t5-small")


def store_translation(t):
    model = TranslationModel(
        text=t.text, base_language=t.base_language, final_language=t.final_language
    )
    model.save()
    return model.id  # type: ignore


def run_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)

    prefix = f"translate {model.base_language} to {model.final_language}: {model.text}"
    input_ids = tokenizer(prefix, return_tensors="pt").input_ids

    outputs = translator.generate(input_ids, max_new_tokens=512)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    model.translation = translation
    model.save()


def find_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    translation = model.translation
    if translation is None:
        translation = "Processing..."
    return translation
