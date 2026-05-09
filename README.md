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

If you want to implement functional components where children should be put in a specific slot, you can do the following.
A slot can be any element, however for this purpose, we also provide a special `Fragment` element that behaves similar to
fragments in React (<>...</>) and does not force you to wrap the children of the component in an element.

```python
def get_element(title: str) -> Element:
    slot = Fragment()
    return div[
        p[title],
        slot,
        p["Footer"]
    ].set_slot(slot)

foo = get_element("cool title")[
    div["Hello, World!"],
    p["Goodbye!"],
]

print(foo)
```

This will yield the following HTML:

```html
<div>
  <p>cool title</p>
  <div>Hello, World!</div>
  <p>Goodbye!</p>
  <p>Footer</p>
</div>
```

## Components

We also provide a `@component` decorator that enables the direct usage of the `[...]` operator to both instantiate the component and add
chilren, similar to regular Elements:

```python
@component
def my_component(title: str | None = None) -> Element:
    slot = Fragment()
    return div[title or "no title", slot].set_slot(slot)

view = my_component["Hello, World!"]
view2 = my_component("nice title")["Hello, World!"]
```

## Usage with FastAPI

This package can also easilly be used with libraries such as FastAPI as an alternative to e.g. Jinja1:

```python
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return html[
        body[
            div["Hello, world"]
        ]
    ].render()
```
