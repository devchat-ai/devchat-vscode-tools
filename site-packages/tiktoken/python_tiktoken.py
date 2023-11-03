from typing import Dict, List, Callable, Union, Tuple
from collections import defaultdict

import threading
import re
import copy

MAX_NUM_THREADS = 128

def hash_current_thread():
    return hash(threading.current_thread().ident)

def byte_pair_merge(piece: bytes, ranks: Dict[bytes, int], f: Callable[[slice], Union[int, str]]) -> List[Union[int, str]]:
    """
    Translates the _byte_pair_merge function from Rust to Python.
    """
    
    # This is a list of (start, rank).
    # The rank is of the byte pair starting at position start.
    # The rank of the last item in the list is not a valid value.
    parts = [(i, float('inf')) for i in range(len(piece) + 1)]

    def get_rank(parts: List[Tuple[int, int]], start_idx: int, skip: int) -> Union[int, None]:
        """
        Inner function to get the rank of a byte pair or sequence.
        """
        if start_idx + skip + 2 < len(parts):
            return ranks.get(piece[parts[start_idx][0]:parts[start_idx + skip + 2][0]])
        else:
            return None

    # We look up the ranks once in the beginning and iteratively update
    # them during each merge, which reduces the number of rank lookups.
    for i in range(len(parts) - 2):
        rank = get_rank(parts, i, 0)
        if rank is not None:
            assert rank != float('inf')  # Check if rank is not the sentinel value
            parts[i] = (parts[i][0], rank)

    # Main merging loop
    while len(parts) > 1:
        # float('inf') is a sentinel rank value allowing us to take the min more quickly
        min_rank = (float('inf'), 0)
        for i, (_, rank) in enumerate(parts[:-1]):
            if rank < min_rank[0]:
                min_rank = (rank, i)

        if min_rank[0] != float('inf'):
            i = min_rank[1]
            # Update ranks considering the skip
            parts[i] = (parts[i][0], get_rank(parts, i, 1) or float('inf'))
            if i > 0:
                parts[i - 1] = (parts[i - 1][0], get_rank(parts, i - 1, 1) or float('inf'))
            # Remove the part
            parts.pop(i + 1)
        else:
            break

    # Construct the output
    out = [f(slice(parts[i][0], parts[i + 1][0])) for i in range(len(parts) - 1)]
    return out

def byte_pair_encode(piece, ranks):
    if len(piece) == 1:
        # return [ranks[tuple(piece)]]
        return [ranks[piece]]
    # return byte_pair_merge(piece, ranks, lambda p: ranks[tuple(piece[p.start:p.stop])])
    return byte_pair_merge(piece, ranks, lambda p: ranks[piece[p.start:p.stop]])

def byte_pair_split(piece, ranks):
    if len(piece) == 1:
        return [piece]
    return byte_pair_merge(piece, ranks, lambda p: piece[p.start:p.stop])

class CoreBaseBPE:
    def __init__(self):
        self.encoder = {}
        self.special_tokens_encoder = {}
        self.decoder = {}
        self.special_tokens_decoder = {}
        self.regex_tls = []
        self.special_regex_tls = []
        self.sorted_token_bytes = []

    def _get_tl_regex(self):
        return self.regex_tls[hash_current_thread() % MAX_NUM_THREADS]

    def _get_tl_special_regex(self):
        return self.special_regex_tls[hash_current_thread() % MAX_NUM_THREADS]

    def _decode_native(self, tokens):
        ret = bytearray()
        for token in tokens:
            token_bytes = self.decoder.get(token, self.special_tokens_decoder.get(token))
            if token_bytes:
                ret.extend(token_bytes)
        return ret

    def _encode_ordinary_native(self, text):
        regex = self._get_tl_regex()
        ret = []
        for mat in re.finditer(regex, text):
            piece = mat.group().encode('utf-8')
            token = self.encoder.get(piece)
            if token:
                ret.append(token)
                continue
            tokens = byte_pair_encode(piece, self.encoder)
            ret.extend(tokens)
        return ret

    def _encode_native(self, text, allowed_special):
        special_regex = self._get_tl_special_regex()
        regex = self._get_tl_regex()
        ret = []
        start = 0
        last_piece_token_len = 0

        while start < len(text):
            next_special = None
            for mat in re.finditer(special_regex, text[start:]):
                if mat.group() in allowed_special:
                    next_special = mat
                    break

            for mat in re.finditer(regex, text[start:next_special.start() if next_special else None]):
                piece = mat.group().encode('utf-8')
                token = self.encoder.get(piece)
                if token:
                    ret.append(token)
                    continue
                tokens = byte_pair_encode(piece, self.encoder)
                last_piece_token_len = len(tokens)
                ret.extend(tokens)

            if next_special:
                piece = next_special.group().encode('utf-8')
                token = self.special_tokens_encoder[piece]
                ret.append(token)
                start = next_special.end()
                last_piece_token_len = 0
            else:
                break

        return ret, last_piece_token_len



class CoreBPE(CoreBaseBPE):

    # _tiktoken.CoreBPE(mergeable_ranks, special_tokens, pat_str)
    def __init__(self, encoder, special_tokens_encoder, pattern):
        self.encoder = encoder
        self.special_tokens_encoder = special_tokens_encoder
        
        self.regex = re.compile(pattern)
        
        special_parts = [re.escape(key) for key in special_tokens_encoder.keys()]
        self.special_regex = re.compile("|".join(special_parts))
        
        self.decoder = {v: k for k, v in encoder.items()}
        
        assert len(encoder) == len(self.decoder), "Encoder and decoder must be of equal length; maybe you had duplicate token indices in your encoder?"
        
        self.special_tokens_decoder = {v: bytes(k, 'utf-8') for k, v in special_tokens_encoder.items()}
        
        self.sorted_token_bytes = sorted(list(encoder.keys()))

        self.regex_tls = [copy.deepcopy(self.regex) for _ in range(MAX_NUM_THREADS)]
        self.special_regex_tls = [copy.deepcopy(self.special_regex) for _ in range(MAX_NUM_THREADS)]


        

    
    def encode_ordinary(self, text):
        return self._encode_ordinary_native(text)
    
    def encode(self, text, allowed_special):
        return self._encode_native(text, allowed_special)[0]
    

    def _encode_bytes(self, bytes):
        try:
            text = bytes.decode('utf-8')
            return self._encode_ordinary_native(text)
        except UnicodeDecodeError as e:
            text = bytes[:e.start].decode('utf-8', 'ignore')
            tokens, last_piece_token_len = self._encode_native(text, set())
            tokens, last_piece_token_len = self._increase_last_piece_token_len(tokens, last_piece_token_len)
            
            if tokens and last_piece_token_len > 0:
                unstable_bytes = self._decode_native(tokens[-last_piece_token_len:])
                unstable_bytes.extend(bytes[e.start:])
                
                tokens = tokens[:-last_piece_token_len]
                tokens.extend(byte_pair_encode(unstable_bytes, self.encoder))  # Assuming byte_pair_encode is defined elsewhere
                
            return tokens

    def encode_with_unstable(self, text, allowed_special):
        tokens, completions = self._encode_unstable_native(text, allowed_special)
        py_completions = [list(seq) for seq in completions]
        return tokens, py_completions

    def encode_single_token(self, piece):
        token = self.encoder.get(piece)
        if token:
            return token
        
        piece_str = piece.decode('utf-8', 'ignore')
        token = self.special_tokens_encoder.get(piece_str)
        if token:
            return token
        
        raise KeyError(piece)

    def encode_single_piece(self, piece):
        token = self.encoder.get(piece)
        if token:
            return [token]
        
        return byte_pair_encode(piece, self.encoder)  # Assuming byte_pair_encode is defined elsewhere

    def decode_bytes(self, tokens):
        return self._decode_native(tokens)

    def decode_single_token_bytes(self, token):
        bytes_val = self.decoder.get(token) or self.special_tokens_decoder.get(token)
        if bytes_val:
            return bytes_val
        raise KeyError(str(token))

    def token_byte_values(self):
        return [bytes(x) for x in self.sorted_token_bytes]



