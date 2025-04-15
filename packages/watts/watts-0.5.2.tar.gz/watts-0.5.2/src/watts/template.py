# SPDX-FileCopyrightText: 2022-2025 UChicago Argonne, LLC
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Optional

import jinja2

from .fileutils import PathLike
from .parameters import Parameters


class TemplateRenderer:
    """Helper class for rendering a Jinja template

    Parameters
    ----------
    template_file
        Path to template file
    **environment_kwargs
        Keywork arguments passed to :class:`jinja2.Environment`

    Attributes
    ----------
    environment : jinja2.Environment
        Jinja environment used to manage templates
    template_file : pathlib.Path
        Path to template file to render
    suffix : str
        Suffix added to filename when rendering a template

    """
    def __init__(self, template_file: PathLike, suffix: str = '.rendered', **environment_kwargs):
        self.environment = jinja2.Environment(
            undefined=jinja2.StrictUndefined,
            **environment_kwargs
        )
        self.template_file = Path(template_file).resolve()
        self.suffix = suffix

    def __call__(self, params: Parameters, filename: Optional[PathLike] = None):
        """Render the template

        Parameters
        ----------
        params
            User parameters used to fill placeholders
        filename
            Filename for rendered template (If none is provided, by default the
            filename of the template is changed so that the new extension is
            .rendered)
        """
        # Default rendered template filename
        if filename is None:
            name = self.template_file.name
            out_path = Path(f'{name}{self.suffix}')
        else:
            out_path = Path(filename)

        # Render template and write to file
        template = self.environment.from_string(self.template_file.read_text())
        out_path.write_text(template.render(**params))
