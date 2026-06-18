import click


class MWebCLIGroup(click.Group):

    def __init__(self, name: str | None = None, help_text: str | None = None, **kwargs):
        super().__init__(name=name, help=help_text, **kwargs)
