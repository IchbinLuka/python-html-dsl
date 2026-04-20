# Python DSL for HTML

This package provides a simple Python DSL for writing HTML code.

Install with:

```bash
pip install git+https://github.com/IchbinLuka/python-html-dsl.git
```

## Usage

Create a simple element:

```python
from html_dsl.html import div, p

foo = div[
    p["This is a paragraph"],
    "Children can also directly be strings.",
]

print(foo.render())
```

For specifying HTML attributes, you can do the following:

```python
image = div[
    img(src="http://example.image.com", alt="an image"),
    a(href="https://example.com")["Link to example.com"]
]
```

For styling html elements, we provide the `css` class that can be passed as a first argument to the elements.
Here, you can specify both css classes and also directly css attributes.

```python
styled = div(css("singleClass"))[
    p(css(["multiple", "classes"]))[
        div(css(width="100px", height="100%"))[
            "Hello, World!"
        ]
    ]
]
```

You can also simply use HTML elements in f-strings:

```python
foo = div[
    f"For more information see {a(href='example.com')['This cool website']}"
]
```

## Slots

If you want to implement functional components where children should be put in a specific slot, you can do the following:

```python
def nice_component(title: str) -> Element:
    slot = div()
    return div[
        p[title],
        slot,
        p["Footer"]
    ].set_slot(slot)

foo = nice_component("cool title")[
    div["Hello, World!"]
]

print(foo)
```

This will yield the following HTML:

```html
<div>
  <p>cool title</p>
  <div>Hello, World!</div>
  <p>Footer</p>
</div>
```
