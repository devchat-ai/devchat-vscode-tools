import re
import hashlib
from typing import Dict, List, Tuple, Union

Rank = int

def _byte_pair_merge(ranks: Dict[bytes, Rank], piece: bytes) -> List[Tuple[bytes, Rank]]:
    parts = []
    min_rank = (float('inf'), float('inf'))
    for i in range(len(piece) - 1):
        rank = ranks.get(piece[i:i + 2], float('inf'))
        if rank < min_rank[0]:
            min_rank = (rank, i)
        parts.append((piece[i:i + 2], rank))
    parts.append((piece[len(piece) - 1:], float('inf')))
    parts.append((piece[len(piece):], float('inf')))

    while min_rank[0] != float('inf'):
        i = min_rank[1]
        if i > 0:
            parts[i - 1] = (parts[i - 1][0], get_rank_with_ranks(piece, parts, i - 1, ranks))
        parts[i] = (parts[i][0], get_rank_with_ranks(piece, parts, i, ranks))
        del parts[i + 1]

        min_rank = (float('inf'), float('inf'))
        for j, (_, rank) in enumerate(parts[:-1]):
            if rank < min_rank[0]:
                min_rank = (rank, j)
    return parts

def get_rank_with_ranks(piece: bytes, parts: List[Tuple[bytes, Rank]], i: int, ranks: Dict[bytes, Rank]) -> Rank:
    if (i + 3) < len(parts):
        key = piece[parts[i][0].start:parts[i + 3][0].start]
        return ranks.get(key, float('inf'))
    else:
        return float('inf')

def byte_pair_encode(piece: bytes, ranks: Dict[bytes, Rank]) -> List[Rank]:
    assert len(piece) > 1
    parts = _byte_pair_merge(ranks, piece)
    tokens = []
    current_token = []
    for part in parts[:-1]:
        if len(current_token) == 0:
            current_token.append(part[0])
        elif ranks.get(b''.join(current_token + [part[0]])) is not None:
            current_token.append(part[0])
        else:
            tokens.append(ranks[b''.join(current_token)])
            current_token = [part[0]]
    tokens.append(ranks[b''.join(current_token)])
    return tokens

def byte_pair_split(piece: bytes, ranks: Dict[bytes, Rank]) -> List[bytes]:
    assert len(piece) > 1
    parts = _byte_pair_merge(ranks, piece)
    return [part[0] for part in parts[:-1]]

class CoreBPE:
    def __init__(self, encoder: Dict[bytes, Rank], special_tokens_encoder: Dict[str, Rank], pattern: str):
        self.encoder = encoder
        self.special_tokens_encoder = special_tokens_encoder
        self.decoder = {v: k for k, v in encoder.items()}
        self.special_tokens_decoder = {v: k.encode('utf-8') for k, v in special_tokens_encoder.items()}
        self.regex = re.compile(pattern)
        self.special_regex = re.compile('|'.join(map(re.escape, special_tokens_encoder.keys())))

    def encode_ordinary(self, text: str) -> List[Rank]:
        try:
            def encode_text(text):
                try:
                    return self.encoder[text]
                except Exception:
                    return 0
            return [encode_text(piece.encode("utf-8")) for piece in self.regex.findall(text)]
        except Exception:
            return []

    def encode(self, text: str, allowed_special: set) -> List[Rank]:
        tokens = []
        start = 0
        for match in self.special_regex.finditer(text):
            if match.start() > start:
                tokens.extend(self.encode_ordinary(text[start:match.start()]))
            if match.group(0) in allowed_special:
                tokens.append(self.special_tokens_encoder[match.group(0)])
            start = match.end()
        if start < len(text):
            tokens.extend(self.encode_ordinary(text[start:]))
        return tokens

    def decode_bytes(self, tokens: List[Rank]) -> bytes:
        return b''.join(self.decoder.get(token, self.special_tokens_decoder.get(token)) for token in tokens)

    def token_byte_values(self) -> List[bytes]:
        return self.sorted_token_bytes

