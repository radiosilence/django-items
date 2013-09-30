from django.conf import settings
from django.db.models.loading import get_model as _get_model

settings.ITEMS = getattr(settings, 'ITEMS', {})
settings.ITEMS_MODELS = getattr(settings, 'ITEMS_MODELS', {})

MODELS = (
    'Manufacturer',
    'Category',
    'Item',
    'ItemAttributeRow',
    'ItemAttributeClass',
    'ItemAttribute',
    'ItemImage',
    'ItemInstance',
)

DEFAULT_MODELS = []

for model in MODELS:
    cls = settings.ITEMS_MODELS.get(model)
    if not cls:
        cls = ''.join(['items.', model])
        DEFAULT_MODELS.append(model)
    settings.ITEMS_MODELS[model] = cls


def is_default(model):
    return model in DEFAULT_MODELS

def get_model(model):
    return _get_model(*settings.ITEMS_MODELS.get(model).split('.'))

def get_model_name(model):
    return settings.ITEMS_MODELS.get(model)
