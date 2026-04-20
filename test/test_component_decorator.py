from html_dsl.element import component
from html_dsl.html import div, p


@component
def simple_component(title: str | None = None):
    """
    A small component that places a title in a <p> and exposes a slot (a <div>)
    where children passed to the component will be rendered.
    """
    slot = div()
    return div[
        p[title or "no title"],
        slot
    ].set_slot(slot)


def test_bracket_only_uses_default_title_and_sets_slot_children():
    # Using the component with the [...] form only should call the wrapped function
    # with no args (so the default title is used) and then assign the provided
    # children into the internal slot.
    view = simple_component["inner content"]

    rendered = view.render()

    # default title should be used
    assert "<p>no title</p>" in rendered

    # the slot is a div and should contain the provided child text
    assert "<div>inner content</div>" in rendered

    # overall structure should be a top-level div
    assert rendered.startswith("<!DOCTYPE html>\n<div")
    assert rendered.endswith("</div>")


def test_call_with_title_then_bracket_assigns_title_and_slot_children():
    # Calling the component with arguments should forward those to the underlying
    # function, so the returned element uses the provided title. Afterwards,
    # using [...] on the returned Element should fill the slot.
    instance = simple_component("My Title")  # returns an Element
    view = instance["slot child"]

    rendered = view.render()

    assert "<p>My Title</p>" in rendered
    assert "<div>slot child</div>" in rendered


def test_multiple_instances_have_independent_slots():
    # Ensure calling the component multiple times produces independent instances
    # and that assigning children to one slot doesn't affect the other.
    a = simple_component("A")["child A"]
    b = simple_component("B")["child B"]

    ra = a.render()
    rb = b.render()

    assert "<p>A</p>" in ra
    assert "<div>child A</div>" in ra

    assert "<p>B</p>" in rb
    assert "<div>child B</div>" in rb

    # cross-check: child B should not appear in a and vice versa
    assert "<div>child B</div>" not in ra
    assert "<div>child A</div>" not in rb
