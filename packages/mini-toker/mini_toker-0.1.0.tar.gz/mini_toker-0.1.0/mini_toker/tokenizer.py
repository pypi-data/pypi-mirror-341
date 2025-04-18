class Tokenizer:
    def __init__(self, token_file='tokens.txt'):
        with open(token_file, encoding='utf-8') as f:
            self.tokens = [t.strip() for t in f if t.strip()]
        for sp in ('<pad>', '<capital>', '<upper>', '<nospace>'):
            if sp not in self.tokens:
                raise ValueError(f"Missing special token: {sp}")
        self.token2id = {tok: i for i, tok in enumerate(self.tokens)}
        self.id2token = {i: tok for tok, i in self.token2id.items()}

    def _segment(self, word):
        segs, i, L = [], 0, len(word)
        while i < L:
            for j in range(L, i, -1):
                sub = word[i:j]
                if sub in self.token2id:
                    segs.append(sub)
                    i = j
                    break
            else:
                ch = word[i]
                if ch in self.token2id:
                    segs.append(ch)
                    i += 1
                else:
                    raise ValueError(f"Cannot tokenize: {ch}")
        return segs

    def tokenize(self, text):
        out = []
        for word in text.strip().split():
            parts = self._segment(word)
            out.append(parts[0])
            for p in parts[1:]:
                out.extend(['<nospace>', p])
        return out

    def convert_tokens_to_ids(self, tokens):
        return [self.token2id[t] for t in tokens]

    def pad(self, ids, max_len):
        pad_id = self.token2id['<pad>']
        return ids + [pad_id] * (max_len - len(ids)) if len(ids) < max_len else ids[:max_len]

    def encode(self, text, max_length=None):
        tokens = self.tokenize(text)
        ids = self.convert_tokens_to_ids(tokens)
        return self.pad(ids, max_length) if max_length else ids

    def decode(self, ids):
        tokens = [self.id2token[i] for i in ids if self.id2token[i] != '<pad>']
        words, i = [], 0
        while i < len(tokens):
            w = tokens[i]
            i += 1
            while i + 1 < len(tokens) and tokens[i] == '<nospace>':
                w += tokens[i + 1]
                i += 2
            words.append(w)
        return ' '.join(words)
