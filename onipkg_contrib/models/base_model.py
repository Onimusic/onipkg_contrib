import os
import uuid

from django.contrib import admin
from django.db import models
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _

from ..validators import validate_file_max_5000


class BaseModelManager(models.Manager):
    """Manager do BaseModel.
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseModel(models.Model):
    """Base model with mandatory fields

    Attrs:
        created_at (datetime): Date and time of model's creation.
        updated_at (datetime): Date and time of model's last update.
    """
    # uuid = models.UUIDField(verbose_name=trans('UUID'), default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deletado'), help_text=_('Se for marcado, este objeto será apagado do banco de dados'))

    # sobrescrita do manager padrão
    objects = BaseModelManager()

    class Meta:
        abstract = True

    @staticmethod
    def filter_objects_based_on_user(request_user_profile, queryset: QuerySet):
        return queryset

    def delete(self, *args, **kwargs):
        """
        Soft delete opcional. Para forçar o delete, passar o argumento force=True
        """
        if kwargs.get('force'):
            super().delete(using=kwargs.get('using'), keep_parents=kwargs.get('keep_parents'))
        else:
            self.deleted = True
            self.save()


class DSPSIdFieldsModel(BaseModel):
    """Base model with mandatory fields and DSP ids
    """
    dsp_itunes_id = models.CharField(verbose_name=_('Itunes ID'), max_length=100, unique=True, null=True, blank=True)
    dsp_spotify_id = models.CharField(verbose_name=_('Spotify ID'), max_length=100, unique=True, null=True, blank=True)
    dsp_youtube_id = models.CharField(verbose_name=_('Youtube ID'), max_length=200, unique=True, null=True, blank=True)
    dsp_chartmetric_id = models.CharField(verbose_name=_('Chartmetric ID'), max_length=200, unique=True, null=True,
                                          blank=True)

    class Meta:
        abstract = True


class BaseContact(BaseModel):
    """Base model for contacts

    Attrs:
        name (str): Contact name. Eg: Sales.
        person_name (str): Contact Person.
        person_email (str): Contact Person email.
        person_phone (str): Contact Person phone.
        notes (str): Misc notes.
    """
    name = models.CharField(verbose_name=_('Name or Role'), max_length=100)
    person_name = models.CharField(verbose_name=_('Person Name'), max_length=100)
    person_email = models.CharField(verbose_name=_('Person Email'), max_length=100)
    person_phone = models.CharField(verbose_name=_('Person Phone'), max_length=100, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        """str method"""
        return str(self.name) + " - " + str(self.person_name)


def get_file_path(instance, filename, folder='uploads'):
    """Define o file_path do arquivo usando um nome aleatorio para o filename, impedindo conflitos de nome igual"""
    filename = "%s%s" % (uuid.uuid4(), filename)
    return os.path.join(folder, filename)


class BaseFile(BaseModel):
    """Base model for FILES

    Attrs:
        name (str):
        file (file):
    """
    file = models.FileField(verbose_name=_('Name'), upload_to=get_file_path, validators=[validate_file_max_5000])
    name = models.CharField(verbose_name=_('File Name'), help_text=_('Max file size 5mb.'), max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        """str method"""
        return self.name


class BaseAdminNoDeleteAction(admin.ModelAdmin):
    """Base model for Admin classe with no delete selected actions
    """

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class BaseApiDataClass:
    def get_data_for_api(self, **kwargs):
        """Generic data

        :return: dict()
        """
        return {
            'class_name': self.__class__
        }
