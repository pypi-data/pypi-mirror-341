import re


def split_string(
    input_string: str,
    split_chars: tuple | list
) -> list[tuple[str, str]]:
    pattern = '|'.join(map(re.escape, split_chars))

    match_posses = re.finditer(f"(.*?)(?:{pattern}|$)", input_string)
    matches = [match.group(1) for match in match_posses if match.group(1)]

    values = re.findall(pattern, input_string)

    if not input_string.startswith(tuple(split_chars)):
        values.insert(0, '')

    return zip(matches, values)