#!/usr/bin/env python3


## by A. Mennucci

## starting from
## https://tex.stackexchange.com/a/23438/199657
## ( adapted to Python3)

## added support for characters with multiple accents,
## https://unicode.org/reports/tr15/tr15-27.html

##  and many decompositions
## https://www.compart.com/en/unicode/decomposition/

_doc_unicode2latex_unicode = r"""
This script will convert unicode to a suitable LaTeX representation.

It will convert accents, e.g. è  → \`{e}   ũ → \widetilde{u}.

It will express fonts, e.g.  ⅅ → \symbbit{D} .

it will convert greek letters, 𝛼  → '\alpha'

It will convert math symbols, e.g.  ∩ → \cap .
"""

_doc_latex2unicode_unicode = r"""
This script will convert  LaTeX to unicode.

With the --greek arguments,
  it will convert greek letters, '\alpha' → 𝛼

With the --math arguments,
  it will convert math symbols, e.g.  \cap → ∩ .

It does not (yet) convert accents or fonts.
"""

_doc_unicode2latex_ascii = r"""
This script will convert unicode to a suitable LaTeX representation.

It will convert accents, e.g. e-grave to \`{e}, u-tilde to \widetilde{u}.

It will express fonts, e.g. double-struck D to \symbbit{D}.

It will convert greek letters, alpha to '\alpha'.

It will convert math symbols, e.g. intersection to \cap.
"""

_doc_latex2unicode_ascii = r"""
This script will convert LaTeX to unicode.

With the --greek arguments,
  it will convert greek letters, '\alpha' to alpha.

With the --math arguments,
  it will convert math symbols, e.g. \cap to intersection.

It does not (yet) convert accents or fonts.
"""

doc_unicode2latex = _doc_unicode2latex_unicode
doc_latex2unicode = _doc_latex2unicode_unicode


import os, sys, copy, io, argparse, unicodedata, collections, subprocess, logging, re
logger = logging.getLogger('unicode2latex')


def _stream_supports_unicode(stream):
    """Return True if the given text stream can encode common Unicode symbols."""
    if not stream:
        return False
    encoding = getattr(stream, 'encoding', None)
    if not encoding:
        return False
    try:
        "→ ∩ α".encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def _select_help_docs():
    """Choose Unicode or ASCII help text based on stdout encoding."""
    if _stream_supports_unicode(getattr(sys, 'stdout', None)):
        return _doc_unicode2latex_unicode, _doc_latex2unicode_unicode
    return _doc_unicode2latex_ascii, _doc_latex2unicode_ascii

if __name__ == '__main__':
    syslogger = sys.stderr.write
else:
    def syslogger(x):
        return logger.warning(x.rstrip())


verbose = 0

global_prefer_unicode_math = False

# fallback for locating the following files, if 'kpsewhich' misbehaves
unicode_math_dir = '/usr/share/texlive/texmf-dist/tex/latex/unicode-math'

# backup location: files bundled with this package
unicode_math_backup_dir = os.path.join(os.path.dirname(__file__), 'tex')

# this is useless but it silence a program checker
unicode_math_table_file = unicode_math_xetex_file = None

for j in 'unicode-math-table.tex' , 'unicode-math-xetex.sty':
    a = None
    try:
        with subprocess.Popen(['kpsewhich', j], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            a = p.stdout.read().strip()
            a = a.decode('utf-8', errors='surrogateescape')
            p.wait()
    except (FileNotFoundError, OSError) as e_:
        logger.info('kpsewhich not available (%s), will use fallback locations', e_)
        a = None
    except Exception as e_:
        logger.warning('Error running kpsewhich for %r: %s', j, e_)
        a = None

    if not a or not os.path.isfile(a):
        if a:
            logger.warning('kpsewhich: cannot locate %r', j)
        # Try system texlive directory
        a = os.path.join(unicode_math_dir, j)
        if not os.path.isfile(a):
            logger.warning('Cannot locate %r in system texlive directory', j)
            # Try backup location bundled with package
            a = os.path.join(unicode_math_backup_dir, j)
            if not os.path.isfile(a):
                logger.warning('Cannot locate %r in backup directory either', j)
                a = None
            else:
                logger.info('Using backup copy of %r from package', j)
    f = j.replace('-','_')[:-4] + '_file'
    globals()[f] = a

## https://en.wikipedia.org/wiki/Combining_Diacritical_Marks
## https://en.wikipedia.org/wiki/Combining_Diacritical_Marks_for_Symbols
accents_unicode2latex = {
    0x0300: '`', 0x0301: "'", 0x0302: '^', 0x0308: '"',
    0x030B: 'H', 0x0303: '~', 0x0327: 'c', 0x0328: 'k',
    0x0304: '=', 0x0331: 'b', 0x0307: '.', 0x0323: 'd',
    0x030A: 'r', 0x0306: 'u', 0x030C: 'v',
}

accents_latex2unicode = {
    k:v for (v,k) in accents_unicode2latex.items()
}

## Mapping from text-mode accent symbols to math-mode accent commands
## Text mode: \'{e} → Math mode: \acute{e}
accents_textmode_to_mathmode = {
    '`': 'grave',      # grave accent
    "'": 'acute',      # acute accent
    '^': 'hat',        # circumflex
    '~': 'tilde',      # tilde
    '"': 'ddot',       # umlaut/diaeresis
    '=': 'bar',        # macron
    '.': 'dot',        # dot above
    'u': 'breve',      # breve
    'v': 'check',      # caron/check
    # Note: some accents don't have direct math equivalents:
    # 'H': double acute (no standard math command)
    # 'c': cedilla (no standard math command)
    # 'k': ogonek (no standard math command)
    # 'b': bar below (no standard math command)
    # 'd': dot below (no standard math command)
    # 'r': ring above (no standard math command)
}

## these unicodes exists in unicode-math-table.tex but they do not work in practice

math_unicode_skip = [
    0x221A, # SQUARE ROOT
    0x23DF, # BOTTOM CURLY BRACKET
    ]

## seed with some assignments that will supersed 'unicode-math-table.tex'

math_unicode2latex = {
    0xD7 : ['\\times'],
    0x221E : ['\\infty'],
    0xab : ['\\guillemotleft'],
    0xbb : ['\\guillemotright'],
    # note that previously circ was mapped to
    #   \smwhtcircle , unicode WHITE BULLET
    # now it is mapped to
    #   \vysmwhtcircle , unicode RING OPERATOR
    0x2218 : ['\\circ'],
    # in the table 0x21D4 is associated to \Leftrightarrow
    0x21D4 : ['\\iff'],
    # convert unicode — EM DASH to ---
    # note that this is currently a one-way conversion,
    # latex2unicode does not convert --- to —
    0x2014 : ['---'],
}

math_latex2unicode = {
    k[0]:[v] for (v,k) in math_unicode2latex.items()
}

## add some one-way conversions

math_latex2unicode.update({
    #U+2016 DOUBLE VERTICAL LINE
    # this will be back-converted to \Vert
    r'\|' : [0x2016],
    # U+21D4 LEFT RIGHT DOUBLE ARROW
    # this will be back-converted to \iff , a
    r'\iff' : [0x21D4] ,
    })



mathaccents_unicode2latex = {}

mathaccents_latex2unicode = {}

## see also
## https://ctan.math.washington.edu/tex-archive/fonts/kpfonts-otf/doc/unimath-kpfonts.pdf

if unicode_math_table_file and os.path.isfile(unicode_math_table_file):
  with  open(unicode_math_table_file) as F:
    for s in F:
        if s.startswith('\\UnicodeMathSymbol'):
            s = s.split('{')
            code=int(s[1].lstrip('"').rstrip('}').rstrip(' '),16)
            latex=s[2].rstrip('}').rstrip(' ')
            typ_ = s[3].rstrip('}')
            info = s[4].rstrip('}')
            #
            U = math_unicode2latex
            L = math_latex2unicode
            if 'accent' in typ_:
                if not (  ( 0x300 <= code and code <= 0x36F ) or  (0x20D0 <= code and code <= 0x20FF) ):
                    syslogger('(Warning accent %r code 0x%x out of standard unicode table)\n' % (latex, code))
                U = mathaccents_unicode2latex
                L = mathaccents_latex2unicode
            #
            if latex not in L:
                if code in math_unicode_skip:
                    if verbose >= 3:
                        syslogger('(Skip %s 0x%x  )\n' % (latex, code))
                else:
                    L[latex] = [code]
                    if verbose >= 3 : syslogger('(Assign %s → 0x%x   (%s))\n' % (latex, code, typ_))
            elif code not in L[latex]:
                L[latex].append(code)
            #
            if code not in U:
                U[code] = [latex]
                if verbose >= 3 : syslogger('(Assign 0x%x → %s (%s))\n' % (code, latex, typ_))
            elif latex not in U[code]:
                U[code].append(latex)   
            if '/' in info:
                info = info.split(' ')
                for i in info:
                    if i and i[0] == '/':
                        oc = '\\' + i[1:]
                        if oc not in L:
                            L[oc] = [code]
                        elif code not in L[oc]:
                            L[oc].append(code)


S = re.compile(r'\\def\s*{(\\[a-zA-Z]*)\s*}\s*{\s*(\\[a-zA-Z]*)\s*}')
R = re.compile(r'\\def\s*(\\[a-zA-Z]*)\s*{\s*(\\[a-zA-Z]*)\s*}')
if unicode_math_xetex_file is not None:
  with open(unicode_math_xetex_file) as F:
    for n,l in enumerate(F):
        for a, b in S.findall(l) + R.findall(l):
            codes = math_latex2unicode.get(b)
            if codes is None:
                if verbose >= 3 : syslogger('(file unicode-math-xetex.sty line %d unknown %s in %r)\n' % (  n, b, l))
                continue
            if a in math_latex2unicode:
                oldcodes = math_latex2unicode[a]
                for code in codes:
                    if code not in oldcodes:
                        oldcodes.append(code)
            else:
                math_latex2unicode[a] = codes
                if verbose >= 3:
                    syslogger('(file unicode-math-xetex.sty line %d added %s for %s → 0x%x)\n' % ( n, a, b, code))


if verbose >= 1:
    for k,v in math_unicode2latex.items():
        if len(v)>1:
            syslogger('multiple unicode to latex, %r -> %r\n' %(k,v))
    for k,v in math_latex2unicode.items():
        if len(v)>1:
            syslogger('multiple latex to unicode, %r -> %r\n' %(k,v))

## table of replacement, that is, if you translate latex1 -> unicode -> latex2
## this lists all cases in which latex1 != latex2

math_replacements = {
}

for k,v in math_latex2unicode.items():
    c = v[0]
    l2 = math_unicode2latex.get(c,[None])[0]
    if k != l2:
        math_replacements[k] = l2


############ mathematical greek mapping

#This mapping 
# was taken from https://www.math.toronto.edu/mathit/symbols-letter.pdf
# was then compiled with XeLaTeX in math mode

greek_xelatex_input = list(map(str.split,\
r"""Γ \Gamma \\ 
Θ \Theta \\ 
Λ \Lambda \\ 
Ξ \Xi \\ 
Π \Pi \\ 
Σ \Sigma \\ 
Υ \Upsilon \\ 
Φ \Phi \\
Ψ \Psi \\ 
α \alpha \\ 
β \beta \\ 
γ \gamma \\ 
δ \delta \\ 
ε \varepsilon \\ 
ζ \zeta \\ 
η \eta \\ 
θ \theta \\ 
θ \vartheta \\ 
ι \iota \\ 
κ \kappa \\ 
λ \lambda \\ 
μ \mu \\ 
ν \nu \\ 
ξ \xi \\ 
π \pi \\ 
ρ \rho \\ 
ς \varsigma \\ 
σ \sigma \\ 
τ \tau \\ 
υ \upsilon \\ 
φ \phi \\ 
φ \varphi \\ 
χ \chi \\ 
ψ \psi \\ 
ω \omega \\ 
Ω \Omega \\ 
∆ \Delta \\ 
𝜖 \epsilon \\ 
𝜚 \varrho \\ 
𝜛 \varpi \\
""".splitlines()))

# and got this PDF

greek_xelatex_ouput = """ΓΓ
ΘΘ
ΛΛ
ΞΞ
ΠΠ
ΣΣ
ΥΥ
ΦΦ
ΨΨ
𝛼𝛼
𝛽𝛽
𝛾𝛾
𝛿𝛿
𝜀𝜀
𝜁𝜁
𝜂𝜂
𝜃𝜃
𝜃𝜗
𝜄𝜄
𝜅𝜅
𝜆𝜆
𝜇𝜇
𝜈𝜈
𝜉𝜉
𝜋𝜋
𝜌𝜌
𝜍𝜍
𝜎𝜎
𝜏𝜏
𝜐𝜐
𝜑𝜙
𝜑𝜑
𝜒𝜒
𝜓𝜓
𝜔𝜔
Ω
∆Δ
𝜖𝜖
𝜚𝜚
𝜛𝜛
""".splitlines()

assert len(greek_xelatex_input) == len(greek_xelatex_ouput), \
        (len(greek_xelatex_input) , len(greek_xelatex_ouput))

## the mapping was not exactly as in the previous PDF
#for j in greek_xelatex_ouput:
#    if len(j) == 2 and j[0] != j[1]:
#        print(' symbols %r ord 0x%x 0x%x ' %    (j, ord(j[0]), ord(j[1])) )
## symbols '𝜃𝜗' ord 0x1d703 0x1d717 
## symbols '𝜑𝜙' ord 0x1d711 0x1d719 
## symbols '∆Δ' ord 0x2206 0x394 


greek_latex2unicode = { greek_xelatex_input[n][1] : ord(greek_xelatex_ouput[n][-1]) for n in range(len(greek_xelatex_ouput)) }

greek_unicode2latex= {
    k:v for (v,k) in greek_latex2unicode.items()
}

#############################################


##https://ctan.mirror.garr.it/mirrors/ctan/macros/unicodetex/latex/unicode-math/unicode-math.pdf
##table 7
fonts = (
    ('SANS-SERIF BOLD ITALIC', '\\symbfsfit'),
    ('SANS-SERIF BOLD',        '\\symbfit'),
    ('SANS-SERIF ITALIC',      '\\symsfit'),
    ('BOLD ITALIC',  '\\symbfit'),
    ## currently broken
    #('BOLD FRAKTUR', '\\symbffrac'),
    ('BOLD SCRIPT',  '\\symbfscr'),
    ('DOUBLE-STRUCK ITALIC',  '\\symbbit'),
    #
    ('DOUBLE-STRUCK',  '\\symbb'),
    ('BLACK-LETTER',   '\\symfrak'),
    ('FRAKTUR',        '\\symfrak'),
    ('SANS-SERIF',     '\\symsf'),
    ('MONOSPACE',      '\\symtt'),
    ('SCRIPT',         '\\symscr'),
    ('BOLD',           '\\symbf'),
    ('ITALIC',         '\\symit'),
    )
    

modifiers = {
    '<super>': '^{%s}' , '<sub>' : '_{%s}',
}


class Decompose_to_tex(object):
  def __init__(self, add_font_modifiers=True, convert_accents = True, prefer_unicode_math = global_prefer_unicode_math, input_file='cmdline', accent_mode='text'):
      self.output = []
      self.add_font_modifiers = add_font_modifiers
      self.convert_accents = convert_accents
      self.prefer_unicode_math = prefer_unicode_math
      self.math_unicode2latex = math_unicode2latex
      self.extra_unicode2latex = {}
      # Instance variables for tracking position (thread-safe)
      self.line_count = 1
      self.char_count = 0
      self.input_file = input_file
      # Accent mode: 'text', 'math', or 'auto'
      # 'text': always use text-mode accents like \'{e}
      # 'math': always use math-mode accents like \acute{e}
      # 'auto': try to detect context (not yet implemented, defaults to 'text')
      if accent_mode not in ('text', 'math', 'auto'):
          raise ValueError(f"accent_mode must be 'text', 'math', or 'auto', got {accent_mode!r}")
      self.accent_mode = accent_mode
  #
  def update_extra(self, D):
      self.extra_unicode2latex.update(D)
  #
  @property
  def result(self):
      s = ''.join(self.output)
      self.output = []
      return s
  #
  def char(self, text):
      assert isinstance(text,str) and len(text) == 1
      return self._docode(text)
  #
  def parse(self, text):
      self.iterator = iter(text)
      try:
          while True:
              self._donext()
      except StopIteration:
          pass
  #
  def _donext(self):
    #
    #if isinstance(text,  collections.abc.Iterable):
    char = next(self.iterator)
    self.char_count += 1
    code = ord(char)
    return self._docode(char)
  #
  def _docode(self, char, useless=None):
    decompose_to_tex = self._docode
    output = self.output
    code = ord(char)
    cat = unicodedata.category(char)
    dec = unicodedata.decomposition(char)
    name = unicodedata.name(char, '')
    #
    if code in self.extra_unicode2latex :
        latex = self.extra_unicode2latex[code]
        if verbose: syslogger('%r:%d:%d extra %r %x %s\n' % (self.input_file, self.line_count, self.char_count,char,code,latex))
        output.append(latex+' ')
        return
    #
    if self.prefer_unicode_math and code in self.math_unicode2latex and code > 0x7f:
        latex = self.math_unicode2latex[code][0]
        if verbose: syslogger('%r:%d:%d math %r %x %s\n' % (self.input_file, self.line_count, self.char_count,char,code,latex))
        output.append(latex+' ')
        return
    #
    if (verbose and dec) or (verbose > 1 ):
        syslogger('%r:%d:%d decomposing %r %x %r %r %r\n' % (self.input_file, self.line_count, self.char_count,char,code,cat,dec,name))
    #
    if cat in ("Mn", "Mc") and code in accents_unicode2latex and self.convert_accents :
        try:
            n = output.pop()
        except IndexError:
            syslogger('%r: accents with no preceding character %r\n' % (self.input_file, char))
            n=' '

        # Generate accent based on accent_mode
        accent_symbol = accents_unicode2latex[code]

        if self.accent_mode == 'math':
            # Use math-mode accent if available
            if accent_symbol in accents_textmode_to_mathmode:
                math_accent = accents_textmode_to_mathmode[accent_symbol]
                output.append( "\\%s{%s}" % (math_accent, n) )
            else:
                # Fallback to text mode for accents without math equivalent
                output.append( "\\%s{%s}" % (accent_symbol, n) )
        elif self.accent_mode == 'auto':
            # TODO: Implement auto-detection of math vs text mode
            # For now, default to text mode
            output.append( "\\%s{%s}" % (accent_symbol, n) )
        else:  # self.accent_mode == 'text'
            # Text-mode accent (default)
            output.append( "\\%s{%s}" % (accent_symbol, n) )
        return
    
    if dec:
        if dec.startswith('<fraction>'):
            dec =  dec.split()[1:]
            dec = list(map(lambda x : chr(int(x,16)), dec))
            if dec[-1] == '/': dec[-1] = ''
            output.append( r'{\sfrac{%s}{%s}}' % (dec[0],dec[-1]))
            return
        decsplit = dec.split()
        base, acc = decsplit[:2]
        if base == '<font>':
            if not self.add_font_modifiers :
                acc = int(acc, 16)
                decompose_to_tex(chr(acc), output)
                return
            mod = '%s'
            N = copy.copy(name)
            for s,l in fonts:
                if s in N:
                    #print((s,N))
                    mod = l + '{' +  mod + '}'
                    j = N.index(s)
                    N = N[:j] + N[j+len(s):]
                    #print((s,N))
            acc = int(acc, 16)
            decompose_to_tex(chr(acc), output)
            n = output.pop()
            output.append( mod % n )
            return
        if base == '<small>':
            acc = int(acc, 16)
            decompose_to_tex(chr(acc), output)
            n = output.pop()
            output.append( r'{\scriptsize{%s}}' % n )
            return
        if base == '<compat>':
            # greek characters, `var` version
            acc = int(acc, 16)
            if 0x370 <= acc <= 0x3ff:
                decompose_to_tex(chr(acc), output)
                n = output.pop()
                output.append( n[0] + 'var' + n[1:] )
                return
            elif 'LIGATURE' in name:
                for l in decsplit[1:]:
                    l = int(l, 16)
                    decompose_to_tex(chr(l), output)
                return
            syslogger('%r:%d:%d unsupported <compat> %r\n' % (self.input_file, self.line_count, self.char_count,dec))
        elif base in modifiers:
            mod = modifiers[base]
            acc = int(acc, 16)
            decompose_to_tex(chr(acc), output)
            n = output.pop()
            output.append( mod % n )
            return
        elif base.startswith('<'):
            syslogger('%r:%d:%d unsupported modifier %r\n' % (self.input_file, self.line_count, self.char_count,base))
            #acc = int(acc, 16)
            #decompose_to_tex(chr(acc), output)
            #n = output.pop()
            #output.append( mod % n )
            output.append(char)
            return
        try:
            base = int(base, 16)
            acc = int(acc, 16)
            if acc in accents_unicode2latex:
                if not self.convert_accents:
                    output.append(char)
                    return
                decompose_to_tex(chr(base), output)
                n = output.pop()

                # Use accent_mode for decomposed accents too
                accent_symbol = accents_unicode2latex[acc]
                if self.accent_mode == 'math' and accent_symbol in accents_textmode_to_mathmode:
                    math_accent = accents_textmode_to_mathmode[accent_symbol]
                    output.append( "\\%s{%s}" % (math_accent, n) )
                else:
                    output.append( "\\%s{%s}" % (accent_symbol, n) )
                return
        except ValueError:
            syslogger('%r:%d:%d unsupported decomposition %r\n' % (self.input_file, self.line_count, self.char_count,dec))
    #
    if name.startswith('GREEK'):
        char = name.split()[-1].lower()
        if char == 'lamda':
            char = 'lambda'
        if 'SMALL' not in name:
            char = char[0].upper() + char[1:]
        output.append('\\' + char + ' ')
        return
    #
    if code in math_unicode2latex and code > 0x7f:
        latex = math_unicode2latex[code][0]
        if verbose: syslogger('%r:%d:%d math %r %x %s\n' % (self.input_file, self.line_count, self.char_count,char,code,latex))
        output.append(latex+' ')
        return
    if code > 127:
        syslogger('%r:%d:%d could not convert %r %x to ascii\n' % (self.input_file, self.line_count, self.char_count,char,code))
    output.append(char)
        
def uni2tex(text, extra = None, **k):
    decompose_to_tex = Decompose_to_tex(**k)
    if extra:
        decompose_to_tex.update_extra(extra)
    decompose_to_tex.parse(text)
    return decompose_to_tex.result

#### FakePlasTeX was extracted and simplified from the plasTeX project

def tex2uni(inp, out, D):
    from .FakePlasTeX import FakeContext, TokenizerPassThru 
    t = TokenizerPassThru.TokenizerPassThru(inp, FakeContext.FakeContext())
    t = iter(t)
    for tok in t:
        #print(repr(tok))
        if isinstance(tok, TokenizerPassThru.EscapeSequence):
            macroname = str(tok.macroName)
            m = '\\' + macroname
            if m in D:
                out.write(D[m])
            else:
                if '::' in tok:
                    m= tok.split('::').pop()
                out.write(m)
        elif isinstance(tok, TokenizerPassThru.Comment):
            out.write('%' + str(tok))
        else:
            out.write(str(tok))



#########


def main(argv=sys.argv):
    exe_name = os.path.basename(argv[0])
    is_latex2unicode = (exe_name == 'latex2unicode')
    doc_unicode2latex_local, doc_latex2unicode_local = _select_help_docs()
    #
    global verbose
    parser = argparse.ArgumentParser(prog=exe_name, 
                                     description= 'convert LaTeX to Unicode' if is_latex2unicode else \
                                        'convert Unicode to LaTeX',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog = doc_latex2unicode_local if is_latex2unicode else doc_unicode2latex_local)
    parser.add_argument('--verbose','-v',action='count',default=verbose)
    parser.add_argument('--output','-o',
                        #required = is_latex2unicode,
                        help='output file')
    parser.add_argument('--input','-i',
                        help='read input file')
    parser.add_argument('--stdin',action='store_true',
                        help='read stdin (instead of input file)')
    parser.add_argument('text', nargs='*',
                        help='the unicode text')
    #
    if is_latex2unicode:
        parser.add_argument('--math','-M',action='store_true',
                            help=r'converto math to unicode  e.g.: \int  → ∫ ')
        parser.add_argument('--greek','-G',action='store_true',
                            help=r'converto greek to unicode  e.g.: \alpha  → α ')
    else:
        parser.add_argument('--prefer-unicode-math','-P',action='store_true',
                            default=global_prefer_unicode_math,
                            help='converto to unicode-math commands whenever possible')
        parser.add_argument('--no-fonts',action='store_true',
                            help='do not add font modifiers')
        parser.add_argument('--no-accents',action='store_true',
                            help='do not convert accents')
        parser.add_argument('--accent-mode', choices=['text', 'math', 'auto'],
                            default='text',
                            help="accent output mode: 'text' for \\'{e}, 'math' for \\acute{e}, 'auto' for auto-detect (default: text)")
    #
    args = parser.parse_args(argv[1:])
    #
    if 1 != bool(args.text) + bool(args.input) + bool(args.stdin):
        parser.print_help()
        return (1)
    #
    verbose = args.verbose
    #
    if is_latex2unicode:
        if args.output not in (None, '-'):
            out = open(args.output, 'w')
        else:
            out = sys.stdout
        #
        if args.stdin:
            inp = sys.stdin
        elif args.text:
            inp = io.StringIO(' '.join(args.text))
        else:
            inp = open(args.input)
        #
        D = {}
        if args.math:
            D.update( { k:chr(v[0]) for k,v in math_latex2unicode.items() } )
        if args.greek:
            D.update( { k:chr(v) for k,v in greek_latex2unicode.items() }  )
        tex2uni(inp, out, D)
        return (0)
    #
    if args.input or args.stdin:
        out=sys.stdout
        if args.output:
            out = open(args.output, 'w')
        if args.text:
            logger.warning('Cmdline %r ignored', args.text)

        input_file_name = 'stdin' if args.stdin else args.input
        decompose_to_tex =  Decompose_to_tex(add_font_modifiers=(not args.no_fonts),
                                             convert_accents=(not args.no_accents),
                                             prefer_unicode_math = args.prefer_unicode_math,
                                             input_file=input_file_name,
                                             accent_mode=args.accent_mode)
        if args.stdin:
            I = sys.stdin
        else:
            I =  open(args.input)
        for L in I:
                decompose_to_tex.parse(L)
                out.write(decompose_to_tex.result)
                decompose_to_tex.char_count = 0
                decompose_to_tex.line_count += 1
        return (0)
    #
    decompose_to_tex =  Decompose_to_tex(add_font_modifiers=(not args.no_fonts),
                                         convert_accents=(not args.no_accents),
                                         prefer_unicode_math = args.prefer_unicode_math,
                                         accent_mode=args.accent_mode)
    #
    for  t in args.text:
        if not isinstance(t,str):
            t = str(t, "utf-8")
        decompose_to_tex.parse(t)
        print(decompose_to_tex.result)
    return (0)

if __name__ == '__main__':
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.exit(main(sys.argv))
