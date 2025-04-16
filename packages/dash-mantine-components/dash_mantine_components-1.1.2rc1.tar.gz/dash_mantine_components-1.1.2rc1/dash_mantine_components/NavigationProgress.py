# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class NavigationProgress(Component):
    """A NavigationProgress component.
NavigationProgress

Keyword arguments:

- action (a value equal to: 'start', 'stop', 'increment', 'decrement', 'set', 'reset', 'complete'; required):
    action.

- value (number; optional):
    value to set the progress bar to."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'NavigationProgress'

    _explicitize_dash_init = True

    def __init__(
        self,
        action: typing.Optional[Literal["start", "stop", "increment", "decrement", "set", "reset", "complete"]] = None,
        value: typing.Optional[typing.Union[typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex]] = None,
        **kwargs
    ):
        self._prop_names = ['action', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['action', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['action']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(NavigationProgress, self).__init__(**args)
