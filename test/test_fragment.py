import pytest

from html_dsl.element import Fragment
from html_dsl.html import div, p


def test_fragment_renders_children_without_wrapper():
    # A Fragment should render its children directly without any enclosing tag.
    frag = Fragment()[p["Child"], "text"]
    rendered = frag.render()

    assert rendered == "<!DOCTYPE html>\n<p>Child</p>text"
    # Also ensure __str__ returns only the inner content (no tags)
    assert str(frag) == "<p>Child</p>text"


def test_fragment_inside_an_element_does_not_add_extra_tag():
    # When used as a child of another element, the Fragment should not introduce an extra wrapper.
    outer = div[Fragment()[p["X"], "Y"]]
    rendered = outer.render()

    assert rendered == "<!DOCTYPE html>\n<div><p>X</p>Y</div>"


def test_empty_fragment_renders_nothing_but_allows_doctype():
    # A Fragment with no children should render as an empty string for str()
    f = Fragment()
    assert str(f) == ""
    assert f.render() == "<!DOCTYPE html>\n"


def test_setting_children_twice_raises_value_error():
    # Element.__getitem__ should raise when attempting to set children on a slot that already has children.
    frag = Fragment()["one"]
    with pytest.raises(ValueError):
        frag["two"]