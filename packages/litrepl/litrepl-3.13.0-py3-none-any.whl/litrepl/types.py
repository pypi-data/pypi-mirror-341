import re
from typing import (Any, Set, List, Dict, Tuple, Callable, Optional, Iterable)
from re import compile as re_compile
from dataclasses import dataclass
from enum import Enum
from lark import ParseTree as LarkTree

FileName=str
LitreplArgs=Any
LarkGrammar=str

# Process exit code or None (running)
ECode=Optional[int]
ECODE_RUNNING=None
ECODE_OK=0
ECODE_UNDEFINED=255

class SType(Enum):
  """ Code section types. They have short string representation and allows user
  to use short code section names and specify interpreter paths and parameters
  via settings."""
  SPython = 0
  SAI = 1
  SShell = 2

@dataclass(frozen=True)
class RunResult:
  """ Result of launchng the readout job """
  fname:FileName     # File where the output data is piped into

@dataclass
class ReadResult:
  """ Result of reading from the readout job """
  text:str           # Current contents of the readout file.
  timeout:bool       # Did the current read attmept timeout? If so, Litrepl
                     # would return control to the user with a
                     # continuation-looking result..

@dataclass
class Symbols:
  codebegin:str
  codeend:str
  resultbegin:str
  resultend:str
  comcodebegin:str
  comcodeend:str
  comresultbegin:str
  comresultend:str
  ignorebegin:str
  ignoreend:str

@dataclass
class ParseResult:
  grammar:LarkGrammar
  symbols:Symbols
  tree:LarkTree
  filetype:str

NSec=int
CursorPos=Tuple[int,int]

@dataclass
class PrepInfo:
  """ Results of the document preprocessing """
  nsec:NSec                         # Total number of code sections
  cursors:Dict[CursorPos,NSec]      # Sections, resolved from cursor positions
  pending:Dict[NSec,RunResult]      # Async job markers
  results:Dict[NSec,str]            # Results

  @staticmethod
  def empty():
    return PrepInfo(0,{},{},{})

@dataclass
class SecRec:
  """ Request for section evaluation """
  nsecs:Set[NSec]                   # Sections to evaluate
  preproc:PrepInfo                  # Results of preprocessing

  @staticmethod
  def empty():
    return SecRec(set(),PrepInfo.empty())

@dataclass
class FileNames:
  """ Interpreter state """
  wd:str                            # Working directory
  inp:str                           # Input pipe
  outp:str                          # Output pipe
  pidf:str                          # File containing current PID
  ecodef:str                        # File containing exit code
  emsgf:str                         # File containing last output


SECVAR_RE = re_compile("(\^+ *R[0-9]+ *\^+)|(v+ *R[0-9]+ *v+)|(\>+ *R[0-9]+ *\<+)",
                       flags=re.MULTILINE|re.A)


@dataclass
class EvalState:
  """ Interpreter state, tracking evaluation of document sections """
  sr:SecRec                         # The original request
  sres:Dict[int,str]                # Section results: sec.num -> result
  ledder:Dict[int,int]              # Facility to restore the cursor: line -> offset
  ecodes:Dict[int,ECode]            # Exit codes: sec.num -> exitcode
  stypes:Set[SType]                 # Section types we have already run
  nsec:int                          # Current section

  def __init__(self,sr:SecRec):
    self.sr,self.sres,self.ledder,self.ecodes,self.stypes,self.nsec=sr,{},{},{},set(),-1


class Interpreter:
  """ Interpreter abstraction. """
  def __init__(self, fns:FileNames)->None:
    """ Create the interpreter object, associated with certain files, as
    specified by `fns`."""
    self.fns=fns
  def run_child(self,interpreter:str)->int:
    """ Launch the interpreter process and wait for it to complete, then return
    the system's exit code. This method should create only one child process.
    Its stdin and stdout should be connected to pipes as described in
    `self.fns`. """
    raise NotImplementedError()
  def setup_child(self, args, finp, foutp)->None:
    """ Sets up the child process by sending interpreter-specific commands to
    the `finp` FILE descriptor which is already associated with its open pipe.
    The `foutp` is another FILE descriptor associated with the output pipe.  """
    raise NotImplementedError()
  def patterns(self)->Tuple[Tuple[str,str],Tuple[str,str]]:
    """ Return two pairs of request-response that could be used for
    synchronization. The first pair is used to get to sync before sending
    evaluation request, the second pair is used to get the evaluation response
    """
    raise NotImplementedError()
  def code_preprocess(self, a:LitreplArgs, es:EvalState, code:str) -> str:
    """ Preprocess code in an interpreter-specific way """
    raise NotImplementedError()
  def result_postprocess(self, a:LitreplArgs, text:str) -> str:
    """ Postprocess results in an interpreter-specific way """
    raise NotImplementedError()
  def run_repl(self, a:LitreplArgs) -> None:
    """ Run foreground repl shell """
    raise NotImplementedError()

