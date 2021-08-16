import sys
import sentencepiece as spm
from pathlib import Path
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--model-file')
    parser.add_argument('--let-unk', action = 'store_true')
    parser.add_argument('--dropout', type = float, default = None)
    return parser.parse_args()


class Encoder:
    def __init__(self, args):
        self.args = args
        model_file = str(Path(args.model_file).resolve())
        self.sp = spm.SentencePieceProcessor(model_file = model_file)

    def encode(self, x):
        x = x.strip()
        x = self.encode_text(x)
        x = self.join_text(x)
        return x

    def encode_text(self, x):
        return self.sp.encode(x,
                out_type = int)

    def join_text(self, x):
        x = [self.sp.IdToPiece(i) for i in x]
        return ' '.join(x)


class DropoutEncoder(Encoder):
    def encode_text(self, x):
        return self.sp.encode(x,
                out_type = int,
                enable_sampling = True,
                alpha = self.args.dropout)


class LetUNKEncoder(Encoder):
    def encode_text(self, x):
        return self.sp.encode(x,
                out_type = str)

    def join_text(self, x):
        return ' '.join(x)


class LetUNKDropoutEncoder(LetUNKEncoder):
    def encode_text(self, x):
        return self.sp.encode(x,
                out_type = str,
                enable_sampling = True,
                alpha = self.args.dropout)


def make_encoder(args):
    if args.let_unk:
        if args.dropout is None:
            encoder = LetUNKEncoder(args)
        else:
            encoder = LetUNKDropoutEncoder(args)
    else:
        if args.dropout is None:
            encoder = Encoder(args)
        else:
            encoder = DropoutEncoder(args)
    return encoder


def encode_inputs(encoder):
    for x in sys.stdin:
        x = encoder.encode(x)
        print(x)


def main():
    args = parse_args()
    encoder = make_encoder(args)
    encode_inputs(encoder)

