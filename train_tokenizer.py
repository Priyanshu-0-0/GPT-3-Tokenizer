from Tokenizer_help_funtions import pair_switch , get_pair_counts
import regex as re

class gpt4_tokenizer:
    def __init__(self,text,vocab_size):
        self.text=text
        self.vocab_size=vocab_size
        self.merges={}
        self.vocab = {idx: bytes([idx]) for idx in range(256)}

    def train(self, text,vocab_size, verbose=False,regex=False):
        
        GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
        if regex==True:
            print("regex applied")
            text = " ".join(re.findall(GPT4_SPLIT_PATTERN, text))
        #text=re.findall(GPT4_SPLIT_PATTERN, text)
        #text = [list(ch.encode("utf-8")) for ch in text]
        text = text.encode("utf-8")
        text=list(map(int,text))

        number_of_merges=vocab_size-256
        bpe_tokens=list(text)

        for i in range(number_of_merges):
            pair_dict = get_pair_counts(bpe_tokens)
            pair = max(pair_dict, key=pair_dict.get)
            if verbose==True:
                print(f"Token {pair} is merged as {i+256}")
            bpe_tokens = pair_switch(bpe_tokens, pair, i+256)
            self.merges[pair] = i+256
        return self.merges, bpe_tokens
    
    def decode(self,ids):

    
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]

        tokens = b"".join(self.vocab[idx] for idx in ids)
        decoded_text = tokens.decode("utf-8", errors="replace")
        return decoded_text
    
    def encoder(self,text):
        # Convert the text to bytes
        tokens=list(text.encode("utf-8"))
        tokens=list(map(int,tokens))
        while len(tokens)>=2:
            pair_counts=get_pair_counts(tokens)
            pair=min(pair_counts,key=lambda p:self.merges.get(p,float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens=pair_switch(tokens,pair,idx)
        return tokens