from django import forms


class Boolean(forms.Form):
    default = forms.BooleanField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Boolean, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.BooleanField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Char(forms.Form):
    default = forms.CharField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Char, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.CharField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Choice(forms.Form):
    default = forms.ChoiceField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Choice, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.ChoiceField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Date(forms.Form):
    default = forms.DateField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Date, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.DateField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class DateTime(forms.Form):
    default = forms.DateTimeField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.DateTimeField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Decimal(forms.Form):
    default = forms.DecimalField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Decimal, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.DecimalField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Duration(forms.Form):
    default = forms.DurationField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Duration, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.DurationField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Email(forms.Form):
    default = forms.EmailField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Email, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.EmailField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class File(forms.Form):
    default = forms.FileField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.FileField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class FilePath(forms.Form):
    default = forms.FilePathField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(FilePath, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.FilepathField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Float(forms.Form):
    default = forms.FloatField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Float, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.FloatField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class GenericIPAddress(forms.Form):
    default = forms.GenericIPAddressField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(GenericIPAddress, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.GenericIPAddressField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Image(forms.Form):
    default = forms.ImageField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.ImageField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Integer(forms.Form):
    default = forms.IntegerField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.IntegerField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class JSON(forms.Form):
    default = forms.JSONField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(JSON, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.JSONField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class MultipleChoice(forms.Form):
    default = forms.MultipleChoiceField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(MultipleChoice, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.MultipleChoiceField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class NullBoolean(forms.Form):
    default = forms.NullBooleanField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(NullBoolean, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.NullBooleanField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Regex(forms.Form):
    default = forms.RegexField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Regex, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.RegexField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Slug(forms.Form):
    default = forms.SlugField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Slug, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.SlugField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class Time(forms.Form):
    default = forms.TimeField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.TimeField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class TypedChoice(forms.Form):
    default = forms.TypedChoiceField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(TypedChoice, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.TypedChoiceField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class TypedMultipleChoice(forms.Form):
    default = forms.TypedMultipleChoiceField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(TypedMultipleChoice, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.TypedMultipleChoiceField(
            label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class url(forms.Form):
    default = forms.URLField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(url, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.URLField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()


class uuid(forms.Form):
    default = forms.UUIDField.widget.__name__

    def __init__(self, field_name, widget_name=default, *args, **kwargs):
        super(uuid, self).__init__(*args, **kwargs)
        self.fields[field_name] = forms.UUIDField(label=field_name)
        self.fields[field_name].widget = getattr(forms, widget_name)()
