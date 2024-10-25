import string

class DummySentencizer:
    def __init__(
            self,
            input_text,
            split_characters=[".", ":", "!", "?"],
            delimiter_token="<SPLIT>"
    ):
        self.sentences = []
        self.raw = str(input_text)
        self._split_characters = split_characters
        self._delimiter_token = delimiter_token
        self._index = 0
        self._sentencize()

    def _sentencize(self):
        work_sentence = self.raw
        for character in self._split_characters:
            repl_seq = character + "" + self._delimiter_token
            work_sentence = work_sentence.replace(character, repl_seq)
        self.sentences = [s.strip() for s in work_sentence.split(self._delimiter_token) if s != ""]

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self.sentences):
            result = self.sentences[self._index]
            self._index+=1
            return result
        raise StopIteration
    

class DummyTokenizer:
    def __init__(
            self,
            sentence,
            token_boundaries=[" ", "-"],
            punctuations=string.punctuation,
            delimiter_token="<SPLIT>"
    ):
        self.tokens = []
        self.raw = str(sentence)
        self._token_boundaries = token_boundaries
        self._delimiter_token = delimiter_token
        self._punctuations = punctuations
        self._index = 0
        self._tokenize()

    def _tokenize(self):
        work_sentence = self.raw
        for punctuation in self._punctuations:
            bound = self._token_boundaries[0]
            repl_seq = bound + punctuation + bound
            work_sentence = work_sentence.replace(punctuation, repl_seq)

        for delimiter in self._token_boundaries:
            work_sentence = work_sentence.replace(delimiter, self._delimiter_token)
        
        self.tokens = [t.strip() for t in work_sentence.split(self._delimiter_token) if t != ""]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self.tokens):
            result = self.tokens[self._index]
            self._index = self._index + 1
            return result
        raise StopIteration