import re


def filter_high_value(results: list) -> list:
    filtered = []
    for item in results:
        if not item.get('url'):
            continue

        is_valid = True
        if "login" in item['url'].lower() or "signup" in item['url'].lower():
            is_valid = False

        if is_valid:
            filtered.append(item)
    return filtered

def clean_html(html: str) -> str:
    cleaned = html.replace('\\n', ' ').replace('\\n', '').replace('\\r\\n', '')
    cleaned = re.sub(r'<[^<]+?>', '', cleaned) 
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned	