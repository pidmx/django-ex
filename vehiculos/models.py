# -*- coding: utf-8 -*-
from django import forms
from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

class Principal(Page):
    body = RichTextField(blank=True)

    def get_context(self, request):
    # Update context to include only published posts, ordered by reverse-chron
        context = super(Principal, self).get_context(request)
        tipopages = self.get_children().live().order_by('-first_published_at')
        context['tipopages'] = tipopages
        return context

    #content_panels = Page.content_panels + [
    #    FieldPanel('body', classname="full"),
    #]
    subpage_types = ['TipoDeVehiculo']

class TipoDeVehiculo(Page):
    icono = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    

    content_panels = Page.content_panels + [
        ImageChooserPanel('icono'),
    ]
     # Parent page / subpage type rules

    # parent_page_types = []
    subpage_types = ['ListaDeVehiculos']

class ListaDeVehiculos(Page):
    intro = RichTextField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
    # Update context to include only published posts, ordered by reverse-chron
        context = super(ListaDeVehiculos, self).get_context(request)
        vehiculos = self.get_children().live().order_by('first_published_at')
        context['vehiculos'] = vehiculos
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('logo'),
    ]

    # parent_page_types = []
    subpage_types = ['DetalleDeVehiculo']

class DetalleDeVehiculo(Page):
    sku = models.CharField(max_length=9, blank=True, null=True)
    especificaciones = RichTextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=100000.00, blank=True, null=True)
    cotizacion = models.IntegerField(default=140000,blank=True,null=True)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    imagen_principal = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.imagen
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('sku'),
        index.SearchField('especificaciones'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('sku'),
            ImageChooserPanel('imagen_principal'),
            FieldPanel('precio'),
            FieldPanel('cotizacion'),
            ImageChooserPanel('logo'),
            FieldPanel('especificaciones'),
        ], heading="Información del Vehículo"),
        InlinePanel('gallery_images', label="Colores"),
        InlinePanel('extra_images', label="Galería de Accesorios"),
        InlinePanel('mounted_images', label="Accesorios Superpuestos"),
    ]

    #parent_page_types = []
    subpage_types = []

class DetalleDeVehiculoGalleryImage(Orderable):
    page = ParentalKey(DetalleDeVehiculo, related_name='gallery_images')
    miniatura = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, 
        on_delete=models.CASCADE, related_name='+'
    )
    imagen = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    color = models.CharField(blank=False, max_length=250)

    panels = [
        #ImageChooserPanel('miniatura'),
        ImageChooserPanel('imagen'),
        FieldPanel('color'),
    ]

class DetalleDeVehiculoGalleryExtraImage(Orderable):
    page = ParentalKey(DetalleDeVehiculo, related_name='extra_images')
    imagen = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    descripcion = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('imagen'),
        FieldPanel('descripcion'),
    ]

class DetalleDeVehiculoGalleryMountedImage(Orderable):
    page = ParentalKey(DetalleDeVehiculo, related_name='mounted_images')
    miniatura = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, 
        on_delete=models.CASCADE, related_name='+'
    )
    imagen = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    descripcion = models.CharField(blank=True, max_length=250)
    precio = models.DecimalField(max_digits=7, decimal_places=2, default=10000.00)

    panels = [
        ImageChooserPanel('miniatura'),
        ImageChooserPanel('imagen'),
        FieldPanel('descripcion'),
        FieldPanel('precio'),
    ]