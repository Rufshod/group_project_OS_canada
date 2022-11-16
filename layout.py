# Add code here for layout.

from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, symbol_dict: dict) -> None:
        self._symbol_dict = symbol_dict