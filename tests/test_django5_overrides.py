
import pytest
from django.db import models
from django_enum import EnumField
from django_enum.choices import IntegerChoices
from django import VERSION as django_version

class MyEnum(IntegerChoices):
    VAL1 = 1, 'Value 1'
    VAL2 = 2, 'Value 2'

class GroupedEnum(IntegerChoices):
    V1 = 1, 'One'
    V2 = 2, 'Two'
    V3 = 3, 'Three'

def get_choices_callable():
    return [(1, 'Callable 1'), (2, 'Callable 2')]

class EnumOverrideModel(models.Model):
    # Dict choices (Django 5.0+)
    dict_field = EnumField(MyEnum, choices={1: 'Dict 1', 2: 'Dict 2'})

    # Callable choices (Django 5.0+)
    callable_field = EnumField(MyEnum, choices=get_choices_callable)

    # Grouped choices
    grouped_field = EnumField(GroupedEnum, choices=[
        ('Group A', [(1, 'One'), (2, 'Two')]),
        ('Group B', [(3, 'Three')]),
    ])

    # Nested dict choices (Django 5.0+)
    nested_dict_field = EnumField(MyEnum, choices={
        "Audio": {
            1: "Vinyl",
            2: "CD",
        },
        "unknown": "Unknown",
    })

    class Meta:
        abstract = True
        app_label = 'tests'

def test_deconstruct_preserves_overrides():
    """Verify that deconstruct() preserves dictionary and callable overrides."""
    field = EnumOverrideModel._meta.get_field('dict_field')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['choices'] == {1: 'Dict 1', 2: 'Dict 2'}

    field = EnumOverrideModel._meta.get_field('callable_field')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['choices'] == get_choices_callable

    field = EnumOverrideModel._meta.get_field('nested_dict_field')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['choices'] == {
        "Audio": {1: "Vinyl", 2: "CD"},
        "unknown": "Unknown",
    }

def test_get_choices_handles_dict():
    """Verify that get_choices() handles dictionary choices correctly."""
    field = EnumOverrideModel._meta.get_field('dict_field')
    # Django converts dict to list of tuples internally in super().get_choices()
    choices = field.get_choices(include_blank=False)
    assert choices == [(1, 'Dict 1'), (2, 'Dict 2')]

def test_get_choices_handles_nested_dict():
    """Verify that get_choices() handles nested dictionary choices correctly."""
    field = EnumOverrideModel._meta.get_field('nested_dict_field')
    choices = field.get_choices(include_blank=False)
    # Normalized by Django + Coerced by EnumField
    assert choices == [
        ("Audio", [(1, "Vinyl"), (2, "CD")]),
        ("unknown", "Unknown"),
    ]

def test_get_choices_handles_recursion():
    """Verify that get_choices() handles grouped choices correctly."""
    field = EnumOverrideModel._meta.get_field('grouped_field')
    choices = field.get_choices(include_blank=False)
    assert choices == [
        ('Group A', [(1, 'One'), (2, 'Two')]),
        ('Group B', [(3, 'Three')]),
    ]

def test_validation_with_overridden_choices():
    """Verify that validation uses the overridden labels or values."""
    field = EnumOverrideModel._meta.get_field('dict_field')
    # Validation in Django usually checks if value is in choices
    # EnumField also tries to coerce.
    # 1 is a valid value for MyEnum and also in the dict
    field.validate(1, None)
    
    # 3 is NOT in MyEnum and NOT in the dict
    with pytest.raises(Exception): # Django raises ValidationError
        field.validate(3, None)

from django import forms as django_forms
from django_enum.forms import EnumChoiceField

def test_form_field_with_nested_dict():
    """Verify that EnumChoiceField handles nested dictionary choices (non-strict)."""
    class NonStrictForm(django_forms.Form):
        field = EnumChoiceField(
            MyEnum, 
            choices={
                "Audio": {1: "Vinyl", 2: "CD"},
                "unknown": "Unknown",
            },
            strict=False
        )

    form = NonStrictForm(data={'field': 1})
    assert form.is_valid()
    
    # 3 is not in Enum and not in dict
    form = NonStrictForm(data={'field': 3})
    assert form.is_valid() # Non-strict allows it
    
    # Rendering should include the added choice if it's not in choices
    # This verifies NonStrictMixin.render()
    widget = form.fields['field'].widget
    # Simulate a value not in choices
    rendered = widget.render('field', 3, attrs={'id': 'id_field'})
    assert 'value="3"' in rendered
    assert '>3<' in rendered

def test_default_choices_still_work():
    """Verify that if no choices are provided, defaults from enum are used."""
    class DefaultModel(models.Model):
        field = EnumField(MyEnum)
        class Meta:
            abstract = True
            app_label = 'tests'

    field = DefaultModel._meta.get_field('field')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['choices'] == [(1, 'Value 1'), (2, 'Value 2')]
