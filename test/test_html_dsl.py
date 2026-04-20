import re

from html_dsl.html import div, p, img, a, css


def test_simple_render():
    foo = div[
        p["This is a paragraph"],
        "Children can also directly be strings.",
    ]

    rendered = foo.render()
    expected = "<!DOCTYPE html>\n<div><p>This is a paragraph</p>Children can also directly be strings.</div>"
    assert rendered == expected


def test_attributes_and_nested_elements():
    node = div[
        img(src="http://example.image.com", alt="an image"),
        a(href="https://example.com")["Link to example.com"],
    ]

    rendered = node.render()

    # DOCTYPE and outer div present
    assert rendered.startswith("<!DOCTYPE html>\n<div")
    assert rendered.endswith("</div>")

    # img tag and its attributes present (don't rely on attribute ordering)
    assert "<img" in rendered
    assert 'src="http://example.image.com"' in rendered
    assert 'alt="an image"' in rendered

    # anchor tag and its text content
    assert '<a href="https://example.com">Link to example.com</a>' in rendered


def test_css_classes_and_inline_styles():
    styled = div(css("singleClass"))[
        p(css(["multiple", "classes"]))[
            div(css(width="100px", height="100%"))[
                "Hello, World!"
            ]
        ]
    ]

    rendered = styled.render()

    # class attributes
    assert 'class="singleClass"' in rendered
    assert 'class="multiple classes"' in rendered

    # style attribute should contain both width and height declarations (order-insensitive)
    assert "width: 100px" in rendered
    assert "height: 100%" in rendered

    # ensure the innermost text is present
    assert "Hello, World!" in rendered


def test_fstring_integration_with_elements():
    # Using an element inside an f-string should inline the element's markup
    content = f"For more information see {a(href='example.com')['This cool website']}"
    node = div[content]

    rendered = node.render()

    # The anchor must be inlined inside the div's content
    assert '<a href="example.com">This cool website</a>' in rendered

    # Ensure surrounding f-string text is also present
    assert "For more information see" in rendered