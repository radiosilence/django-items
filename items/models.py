# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField

from items.conf import is_default, settings, get_model, get_model_name


ITEM_TYPES = settings.ITEMS.get('ITEM_TYPES', (
    ('CN', _('Consumable')),
    ('UN', _('Unlabeled')),
    ('LB', _('Labeled')),
))


class Slugged(models.Model):
    slug = models.SlugField(verbose_name=_('Slug'))

    class Meta:
        abstract = True


class Named(models.Model):
    name = models.SlugField(verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Ordered(models.Model):
    order = models.PositiveIntegerField(verbose_name=_('Order'), null=True,
        blank=True)

    class Meta:
        abstract = True


class BaseManufacturer(Slugged, Named, models.Model):
    """ The manufacturer of an item class """

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        abstract = True


class BaseCategory(Slugged, Named, models.Model):
    """ Category of the item class """

    parent = models.ForeignKey(get_model_name('Category'),
        verbose_name=_('Parent'), blank=True, null=True,
        related_name='children')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        abstract = True


class BaseItemClass(Slugged, Named, models.Model):
    """ This is the model it all revolves around. """
    item_type = models.CharField(verbose_name=_('Item Type'),
        max_length=2, choices=ITEM_TYPES, default="UN")
    short_description = models.TextField(verbose_name=_('Short Description'),
        blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'),
        blank=True, null=True)
    unit_price = models.DecimalField(verbose_name=_('Unit Price'),
        max_digits=32, decimal_places=4)
    manual = models.FileField(verbose_name=_('Manual'),
        upload_to='manuals', blank=True, null=True)
    category = models.ForeignKey(get_model_name('Category'),
        verbose_name=_('Category'), related_name='items')
    manufacturer = models.ForeignKey(get_model_name('Manufacturer'), related_name='items')

    class Meta:
        verbose_name = _('Item Class')
        verbose_name_plural = _('Item Classes')
        abstract = True


class BaseItem(models.Model):
    label = models.CharField(verbose_name=_('Label'), max_length=255,
        null=True, blank=True)
    base_stock = models.PositiveIntegerField(verbose_name=_('Base Stock'),
        default=1)
    num_damaged = models.PositiveIntegerField(verbose_name=_('Number Damaged'),
        default=1)
    num_missing = models.PositiveIntegerField(verbose_name=_('Number Missing'),
        default=1)
    num_discarded = models.PositiveIntegerField(verbose_name=_('Number Discard'),
        default=1)

    @property
    def available_stock(self):
        return self.base_stock - (
            self.num_damaged + self.num_missing + self.num_discarded
        )

    def available_on_date(self, date):
        pass

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        abstract = True


class BaseItemAttributeClass(Named, models.Model):
    class Meta:
        verbose_name = _('Item Attribute Class')
        verbose_name = _('Item Attribute Classes')
        abstract = True


class BaseItemAttribute(Ordered, models.Model):
    cls = models.ForeignKey(get_model_name('ItemAttributeClass'),
        verbose_name=_('Class'),  related_name="attributes")
    text = models.TextField(verbose_name=_('Text'))
    item = models.ForeignKey(get_model_name('Item'), verbose_name=_('Item'),
        related_name='attributes')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _('Item Attribute')
        verbose_name_plural = _('Item Attributes')
        abstract = True


class BaseItemImage(Named, Ordered, models.Model):
    image = ImageField(verbose_name=_('Image'), upload_to='item_image')
    item_class = models.ForeignKey(get_model_name('ItemClass'), related_name='photos')

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = _('Item Image')
        verbose_name_plural = _('Item Images')
        abstract = True



class Manufacturer(BaseManufacturer):
    class Meta:
        managed = is_default('Manufacturer')


class Category(BaseCategory):
    class Meta:
        managed = is_default('Category')


class ItemClass(BaseItemClass):
    class Meta:
        managed = is_default('ItemClass')


class Item(BaseItem):
    class Meta:
        managed = is_default('Item')


class ItemAttributeClass(BaseItemAttributeClass):
    class Meta:
        managed = is_default('ItemAttributeClass')


class ItemAttribute(BaseItemAttribute):
    class Meta:
        managed = is_default('ItemAttribute')


class ItemImage(BaseItemImage):
    class Meta:
        managed = is_default('ItemImage')
