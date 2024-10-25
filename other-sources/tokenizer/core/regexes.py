DEFAULT_SENTENCE_BOUNDARIES = [
    #r"(?<!\.)(\.)(?!\.)",           # Single dot, not followed or preceded by a
    #r"(?<![0-9](\.)(?![0-9]))",
    r"(?<=[0-9]|[^0-9.])(\.)(?=[^0-9.]|[^0-9.]|[\s]|$)", #FIXME
    r"\.{2,}",
    r"[\!\?]+",
    r"\:"
]

DEFAULT_PUNCTUATIONS = DEFAULT_SENTENCE_BOUNDARIES + [
    r"\,+",
    r"[\(\)\[\]\{\}\<\>]"
]