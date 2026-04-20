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
