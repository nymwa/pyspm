import sys
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--replace-unk', default=None)
    parser.add_argument('--remove-unk', action = 'store_true')
    return parser.parse_args()


class Decoder:
    def preprocess(self, x):
        return x

    def decode(self, x):
        x = x.strip().split()
        x = self.preprocess(x)
        x = ''.join(x).replace('▁', ' ')
        x = x.strip()
        return x


class UNKRemovingDecoder(Decoder):
    def preprocess(self, x):
        return [token for token in x if token != '<unk>']


class UNKReplacingDecoder(Decoder):
    def __init__(self, unk_token):
        self.unk_token = unk_token

    def preprocess(self, x):
        return [self.unk_token if token == '<unk>' else token for token in x]


def make_decoder(args):
    if args.remove_unk:
        decoder = UNKRemovingDecoder()
    elif args.replace_unk:
        decoder = UNKReplacingDecoder(args.replace_unk)
    else:
        decoder = Decoder()
    return decoder


def decode_inputs(decoder):
    for x in sys.stdin:
        x = decoder.decode(x)
        print(x)


def main():
    args = parse_args()
    decoder = make_decoder(args)
    decode_inputs(decoder)

