DEFAULT_SENTENCE_BOUNDARIES = [
    r"(?<!\.)(\.)(?!\.)",
    r"(?<![0-9](\.)(?![0-9]))",
    r"\.{2,}",
    r"[\!\?]+",
    r"\:"
]

DEFAULT_PUNCTUATIONS = DEFAULT_SENTENCE_BOUNDARIES + [
    r"\,+",
    r"[\(\)\[\]\{\}\<\>]"
]