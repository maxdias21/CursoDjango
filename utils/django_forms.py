def add_placeholder(form, placeholder: str):
    form.widget.attrs['placeholder'] = placeholder

def add_label(form, placeholder: str):
    form.label = placeholder

def add_help_text(form, help_text: str):
    form.help_text = help_text

