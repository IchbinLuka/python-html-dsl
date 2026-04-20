from __future__ import annotations
from typing import Callable, Generic, ParamSpec

type Child = "Element | str"

class css:
    def __init__(self, classes: list[str] | str | None = None, **kwargs: str | float) -> None:
        if isinstance(classes, str):
            classes = [classes]
        self.classes = classes
        self.attributes = kwargs

class ElementMeta(type):
    name: str

    def __getitem__(cls, children: tuple[Child, ...] | Child) -> Element:
        return cls()[children]


class Element(metaclass=ElementMeta):
    name: str
    def __init__(self, styles: css | None = None, **attr: str | None) -> None:
        self.children: tuple[Child, ...] = ()
        self.slot = self
        self.attr = {
            key.strip("_").replace("_", "-"): value
            for key, value in attr.items()
            if value is not None
        }
        if styles is not None:
            if styles.classes is not None:
                self.attr["class"] = " ".join(styles.classes)
            if len(styles.attributes) > 0:
                self.attr["style"] = "; ".join(
                    f"{key.strip('_').replace('_', '-')}: {value}"
                    for key, value in styles.attributes.items()
                )

    def __str__(self) -> str:
        attr = " ".join(
            f'{key}="{value}"' if len(value) > 0 else key
            for key, value in self.attr.items()
        )
        open_tag = f"{self.name} {attr}" if len(attr) > 0 else f"{self.name}"
        return f"<{open_tag}>{''.join(str(child) for child in self.children)}</{self.name}>"

    def set_slot(self, slot: Element) -> Element:
        self.slot = slot
        return self

    def __getitem__(self, children: tuple[Child, ...] | Child) -> Element:
        if self.slot is self and len(self.children) > 0:
            raise ValueError("Cannot set children on a slot that already has children")
        if isinstance(children, tuple):
            self.slot.children = children
        else:
            self.slot.children = (children,)
        return self

    def render(self) -> str:
        return f"<!DOCTYPE html>\n{str(self)}"

P = ParamSpec("P")

class component(Generic[P]):
    """Utility decorator for functional components that enables the direct usage of the [...]
    operator to both instantiate the component and add chilren, similar to regular Elements.

    Example:
    ```python
    @component
    def my_component(title: str | None = None) -> Element:
        slot = div()
        return div[title or "no title", slot].set_slot(slot)

    view = my_component["Hello, World!"]
    view2 = my_component("nice title")["Hello, World!"]
    ```
    """
    def __init__(self, fun: Callable[P, Element]) -> None:
        self.fun = fun

    def __getitem__(self, children: tuple[Child, ...] | Child):
        return self.fun()[children]  # type: ignore

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        return self.fun(*args, **kwargs)

class Fragment(Element):
    """A container element that does not render any HTML tag, useful for grouping children without a wrapper.
    Similar to fragments (<>...</>) in React.
    """
    name = ""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "".join(str(child) for child in self.children)
