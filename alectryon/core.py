# Copyright © 2019 Clément Pit-Claudel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import namedtuple
from textwrap import indent

from shlex import quote
from shutil import which
from subprocess import Popen, PIPE, check_output
from sys import stderr

DEBUG = False
TRACEBACK = False

def debug(text, prefix):
    if isinstance(text, (bytes, bytearray)):
        text = text.decode("utf-8", errors="replace")
    if DEBUG:
        print(indent(text.rstrip(), prefix), flush=True)

Hypothesis = namedtuple("Hypothesis", "names body type")
Goal = namedtuple("Goal", "name conclusion hypotheses")
Message = namedtuple("Message", "contents")
Sentence = namedtuple("Sentence", "contents messages goals")
Text = namedtuple("Text", "contents")

Goals = namedtuple("Goals", "goals")
Messages = namedtuple("Messages", "messages")
RichSentence = namedtuple("RichSentence", "contents outputs annots prefixes suffixes")

class GeneratorInfo(namedtuple("GeneratorInfo", "name version")):
    def fmt(self, include_version_info=True):
        return "{} v{}".format(self.name, self.version) if include_version_info else self.name

class Prover():
    @classmethod
    def version_info(cls, binpath=None):
        raise NotImplementedError()

    @classmethod
    def annotate(cls, chunks, *args, **kwargs):
        """Annotate multiple `chunks` of code.

        All fragments are executed in the same prover instance, started with
        arguments `args`, `kwargs`.  The return value is a list with as many
        elements as in `chunks`, but each element is a list of fragments: either
        ``Text`` instances (whitespace and comments) and ``Sentence`` instances (code).
        """
        raise NotImplementedError()

class REPLProver(Prover):
    REPL_BIN = None
    REPL_NAME = None
    DEFAULT_ARGS = ()

    def __init__(self, binpath=None, args=()):
        self.binpath = binpath or self.REPL_BIN
        self.args = [*args, *self.DEFAULT_ARGS]
        self.repl = None

    @classmethod
    def version_info(cls, binpath=None):
        bs = check_output([binpath or cls.REPL_BIN, "--version"])
        return GeneratorInfo(cls.REPL_NAME, bs.decode('ascii', 'ignore').strip())

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, *_exn):
        self.kill()
        return False

    def _read(self):
        response = self.repl.stdout.readline()
        debug(response, '<< ')
        return response

    def _write(self, s, end):
        debug(s, '>> ')
        self.repl.stdin.write(s + end)
        self.repl.stdin.flush()

    def kill(self):
        """Terminate this prover instance."""
        if self.repl:
            self.repl.kill()

    def prover_not_found(self):
        """Raise an error to indicate that ``self.binpath`` cannot be found."""
        raise NotImplementedError()

    def reset(self):
        """Start or restart this proper instance."""
        path = which(self.binpath)
        if path is None:
            self.prover_not_found()
        self.kill()
        cmd = [path, *self.args]
        debug(" ".join(quote(s) for s in cmd), '# ')
        self.repl = Popen(cmd, stdin=PIPE, stderr=stderr, stdout=PIPE)
