import os
from typing import Tuple, TypedDict
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "list_of_links",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("list_of_links", path=build_dir)


class Link(TypedDict):
    subject: str
    link: str

def list_of_links(title: str, links: Tuple[Link, ...], default_link: str | None = None, key: str | None = None):
    """
    Generates a component consisting of a title and a list of links. Each link is a
    tuple containing a label and a URL. An optional default link can be specified,
    which will be highlighted or selected by default. A key can be provided for
    component identification and interaction tracking.

    Parameters
    ----------
    title : str
        The title for the list of links component.
    links : tuple of dicts
        A tuple of dicts where each tuple consists of a label and a URL
        for an individual link.
    default_link : optional
        The default link that should be highlighted or selected.
    key : optional
        An optional key for identifying the component, useful for interaction
        tracking and event handling.

    Returns
    -------
    component_value :
        The resulting component after processing the title and list of links.

    """

    default_link = default_link or links[0]["link"] if links else None

    component_value = _component_func(title=title, links=links, key=key, default=default_link)
    return component_value
