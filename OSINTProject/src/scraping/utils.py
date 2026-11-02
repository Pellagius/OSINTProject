import re

def clean_html_content(html: str) -> str:
    """
    Basic cleaning of raw web content.
    Removes script and style tags, and extra whitespace.
    """
    # Remove script and style elements
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
    # Remove extra whitespaces
    html = " ".join(html.split())
    return html
