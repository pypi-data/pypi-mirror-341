from typing import Optional, Sequence, Union

from django.db.models import Model, QuerySet
from rest_framework import serializers


class OrmOnlyMixin:
    """
    orm only by serializer fields
    """
    orm_only_enabled = None
    serializer_class: serializers.ModelSerializer = None

    @classmethod
    def should_enable_orm_only(cls, serializer_class):
        """
        Determine whether the orm-only mechanism should be enabled.
        Priority: Meta setting > class attr > global setting.
        """
        # 1.Meta setting
        meta_value = getattr(serializer_class.Meta, 'orm_only_fields', None)
        if meta_value is not None:
            return bool(meta_value)

        # 2.cls setting
        if cls.orm_only_enabled is not None:
            return bool(cls.orm_only_enabled)

        # 3.global setting
        from django.conf import settings
        return getattr(settings, 'ORM_ONLY_ENABLED', False)

    @classmethod
    def get_model_fields_from_serializer(cls, serializer_class: serializers.ModelSerializer = None):
        """
        Get the list of fields that are both defined in the model and exposed in the serializer.

        Args:
            serializer_class: A DRF ModelSerializer class.

        Returns:
            A list of field names present in both the model and serializer.
        """
        # Skip if orm-only is disabled
        if not cls.should_enable_orm_only(serializer_class):
            return []
        # Get the model class from the serializer
        model = getattr(serializer_class.Meta, 'model')

        # Explicitly defined fields
        serializer_fields = getattr(serializer_class.Meta, 'fields')
        if not serializer_fields:
            # Get all serializer-exposed fields (declared and auto-generated)
            serializer_fields = set(serializer_class().get_fields().keys())
        elif serializer_fields in ['__all__']:
            # Do not apply `.only()`
            return []
        else:
            # convert to set
            serializer_fields = set(serializer_fields)
        # Get all field names defined in the model (including FKs)
        model_fields = set(f.name for f in model._meta.get_fields())

        # Return intersection of model and serializer fields
        return list(model_fields & serializer_fields)

    @classmethod
    def fields(cls, serializer_class: serializers.ModelSerializer = None):
        """
        get fields
        """
        if serializer_class:
            return cls.get_model_fields_from_serializer(serializer_class=serializer_class)
        return cls.get_model_fields_from_serializer(serializer_class=cls.serializer_class)


class OrmOnlyViewMixin(OrmOnlyMixin):
    """
    Designed to work with Django REST Framework.


    # Example usage in a DRF ViewSet:
    #
    # class UserViewSet(OrmOnlyViewMixin, ModelViewSet):
    #     queryset = User.objects.all()
    #     serializer_class = UserSerializer
    #
    #     def get_queryset(self):
    #         qs = super().get_queryset()
    #         return self.hook_orm_fields(qs)
    """
    def hook_orm_fields(self, qs=None):
        """
        Dynamically apply `.only()` based on serializer fields.
        """
        serializer_class = self.get_serializer_class()
        if not serializer_class:
            return qs
        fields = self.fields(serializer_class=serializer_class)
        if not fields:
            return qs
        return qs.only(*fields)


class OrmOnlyServiceMixin(OrmOnlyMixin):
    """
    当作srv
    """
    qs: QuerySet = None

    @classmethod
    def only(cls, serializer_class: serializers.ModelSerializer = None, qs: QuerySet = None):
        """
        only fields
        """
        fields = cls.fields(serializer_class=serializer_class)
        _qs = qs
        if not qs:
            _qs = cls.qs
        return _qs.only(*fields)

    @classmethod
    def _data(cls,
              # qs=None,
              qs: Optional[Union[Model, QuerySet, Sequence[Model]]] = None,
              serializer_class: serializers.ModelSerializer = None, many: bool = False):
        return serializer_class(qs, many= many).data

    @classmethod
    def data(cls, serializer_class: serializers.ModelSerializer = None):
        """
        instance serializer data
        """
        instance = cls.only(serializer_class=serializer_class).first()
        return cls._data(qs=instance, many=False)

    @classmethod
    def data_list(cls,  serializer_class: serializers.ModelSerializer = None):
        qs = cls.only(serializer_class=serializer_class)
        return cls._data(qs=qs, many=False)



