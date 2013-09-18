from django.conf import settings
from django.db.models.loading import get_model as _get_model

settings.ITEMS = getattr(settings, 'ITEMS', {})
settings.ITEMS_MODELS = getattr(settings, 'ITEMS', {})

MODELS = (
    'Manufacturer',
    'Category',
    'ItemClass',
    'Item',
    'ItemAttributeClass',
    'ItemAttribute',
    'ItemPhoto',
)

for model in MODELS:
    settings.ITEMS_MODELS[model] = settings.ITEMS_MODELS.get(model, ''.join(['items.', model]))


def get_model(model):
    return _get_model(*settings.ITEMS_MODELS.get(model).split('.'))

def get_model_name(model):
    return settings.ITEMS_MODELS.get(model)
