import re
from .regexes import DEFAULT_SENTENCE_BOUNDARIES, DEFAULT_PUNCTUATIONS

def sentencize(
        raw_input_document,
        sentence_boundaries=DEFAULT_SENTENCE_BOUNDARIES,
        delimiter_token="<SPLIT>"
):
    """
    Gets a list of sentence objects extracted from the given string

    Inputs:
    - raw_input_document : str
        Text where the sentences will be extracted from
    - sentence_boundaries : str
        Regex patterns representing the boundaries between
    each sentence in the text
    - delimiter_token : str
        String representation of the token delimiting the separation
    between the sentences

    Returns:
    - A list of Sentence objects, each one holding its tokens
    """

    # Separating the sentences in the string with the delimiter token
    working_document = raw_input_document
    for bound in sentence_boundaries:
        working_document = re.sub(
            bound, 
            f"\g<0>{delimiter_token}",
            working_document,
            flags=re.UNICODE
        )

    # Splitting the string on the delimiter tokens
    # Gets a list with the string representations of each sentence
    string_sentences = [s.strip() for s in working_document.split(delimiter_token) if s.split() != ""]

    # Creating the Sentence objects and structuring their linked list
    sentences_obj = []
    previous = None
    for sent in string_sentences:
        # Getting the start and end positions of the sentence in the text
        start_pos = raw_input_document.find(sent)
        end_pos = start_pos + len(sent)
        # Instantiating the Sentence object
        new_sent = Sentence(start_pos, end_pos, raw_input_document)
        sentences_obj.append(new_sent)
        # Linking the new sentence object in the linked list
        if previous is not None:
            previous.next_sentence = new_sent
            new_sent.previous_sentence = previous
        # Updating the previous sentence
        previous = new_sent
    return sentences_obj

def tokenize(
        raw_input_sentence,
        join_split_text=True,
        split_text_char='\-',
        punctuation_patterns=DEFAULT_PUNCTUATIONS,
        split_characters=r'[\s\t\n\r]',
        delimiter_token='<SPLIT>'
):
    """
    Tokenizes the sentence string. Returns a list of tokens.

    Parameters:
    - raw_input_sentence : str
        Text representation of the sentence
    - join_split_text : bool
        Indicates the existence of a token separator that needs to be
        removed
    - split_text_char : str
        Regex pattern to be removed from the original text of the sentence
        before tokenization
    - punctuation_patterns : list[str]
        List of regex patterns representing the punctuations of the vocabulary
    - split_characters : str
        Regex pattern of the characters (or a set of those) that separate the
        tokens
    - delimiter_token : str
        Text representing the token used to mark token boundaries
    """

    working_sentence = raw_input_sentence

    # Joining text split by 'split_text_char'
    if join_split_text:
        working_sentence = re.sub(f"\w+({split_text_char})\n\w+", '', working_sentence)
    # Separating punctuation from words
    for punct in punctuation_patterns:
        working_sentence = re.sub(punct, " \g<0> ", working_sentence)
    # Splitting the sentence by the split characters
    working_sentence = re.sub(split_characters, delimiter_token, working_sentence)
    str_tokens = [t.strip() for t in working_sentence.split(delimiter_token) if t.strip() != ""]
    # Generating Start Of Sentence (SOS) token
    previous = Token(0, 0, raw_input_sentence, SOS=True)
    # Creating the list of tokens
    token_list = [previous]
    for t in str_tokens:
        # Get start and end positions of the token in the text
        start_pos = raw_input_sentence.find(t)
        end_pos = start_pos + len(t)
        # Instantiating a new token object
        new_token = Token(start_pos, end_pos, raw_input_sentence)
        # Appending the token to the list
        token_list.append(new_token)
        # Linking the new token to the linked list
        previous.next_token = new_token
        new_token.previous_token = previous
        # Updating the previous token
        previous = new_token

    # Adding the End Of Sentence (EOS) special token 
    if not previous.SOS:
        eos = Token(len(raw_input_sentence), len(raw_input_sentence), raw_input_sentence, EOS=True)
        previous.next_token = eos
        eos.previous_token = previous
        token_list.append(eos)

    return token_list

class BasicStruc:
    def __init__(self):
        self._index = 0
        self.raw = None

    def get(self):
        return self.raw

    def _get_lower_level(self):
        """
        Returns the lower level contained in the object:
        - Document -> list[Sentence]
        - Sentence -> list[Token]
        """
        # Needs to be overriden
        return []

    def _get_max_index(self):
        """
        Returns the maximum index of the iterator
        """
        return len(self._get_lower_level())

    def __getitem__(self, idx):
        """
        Returns the element of the object's lower level list at the position 
        specified by 'idx' (int)
        """
        return self._get_lower_level()[idx]

    # Representations of the object
    def __repr__(self):
        return self.get()
    
    def __str__(self):
        return self.get()
    
    # Iterator functions
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < self._get_max_index():
            result = self._get_lower_level()[self._index]
            self._index += 1
            return result
        raise StopIteration

class Document(BasicStruc):
    def __init__(
            self,
            document_text
    ):
        super(Document, self).__init__()
        self.raw = document_text
        self.sentences = sentencize(self.raw)

    def _get_lower_level(self):
        return self.sentences
    
class Sentence(BasicStruc):
    def __init__(
            self,
            start_pos,
            end_pos,
            raw_document_ref
    ):
        super(Sentence, self).__init__()
        self.start_pos = int(start_pos)
        self.end_pos = int(end_pos)
        self._document_string = raw_document_ref
        self.next_sentence = None
        self.previous_sentence = None
        self.raw = self._document_string[self.start_pos:self.end_pos]
        self.tokens = tokenize(self.get())
    
    def _get_lower_level(self):
        return self.tokens
    
    def __eq__(self, other):
        return self.get() == other
    
class Token(BasicStruc):
    def __init__(
            self,
            start_pos,
            end_pos,
            raw_sentence_ref,
            SOS=False,
            EOS=False
    ):
        super(Token, self).__init__()
        self.start_pos = int(start_pos)
        self.end_pos = int(end_pos)
        self.sentence_string = raw_sentence_ref
        self.raw = self.sentence_string[self.start_pos:self.end_pos]
        self.next_token = None
        self.previous_token = None
        self.SOS = SOS
        self.EOS = EOS

    def get(self):
        if self.SOS:
            return "<SOS>"
        elif self.EOS:
            return "<EOS>"
        else:
            return super().get()
        
    def __eq__(self, other):
        return self.get() == other