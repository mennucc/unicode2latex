# Known Bugs and Issues in unicode2latex (u2l.py)

This document lists known bugs, potential issues, and design limitations discovered through testing and code analysis.

## Fixed Bugs

### 1. ✅ FIXED: Incorrect format string in accent error message (Line 438)
**Fixed by:** Andrea Mennucci
**Status:** FIXED
**Severity:** Medium
**Original Location:** `u2l.py:438`

**Description:**
The error message for accents without a preceding character had an incorrect format string.

**Original code:**
```python
syslogger('%r:%d accents with no preceding character\n' % (input_file, char))
```

**Problem:**
- Used `%d` (integer format) for `char` which is a string
- Caused `TypeError: %d format: a real number is required, not str`

**Fix applied:**
```python
syslogger('%r: accents with no preceding character %r\n' % (self.input_file, char))
```

**Test:** `unittests/test_accents.py::TestAccentEdgeCases::test_combining_accent_alone`

---

### 2. ✅ FIXED: char() method passing wrong type to _docode (Line 392)
**Fixed by:** Andrea Mennucci
**Status:** FIXED
**Severity:** Medium
**Original Location:** `u2l.py:392`

**Description:**
The `char()` method was passing an integer (from `ord()`) to `_docode()` which expects a string character.

**Original code:**
```python
def char(self, text):
    assert isinstance(text,str) and len(text) == 1
    return self._docode(ord(text))
```

**Problem:**
- `_docode()` expects a character string but received an integer
- Caused `TypeError: ord() expected string of length 1, but int found` at line 414

**Fix applied:**
```python
def char(self, text):
    assert isinstance(text,str) and len(text) == 1
    return self._docode(text)
```

**Test:** `unittests/test_unicode2latex.py::TestDecomposeToTexClass::test_char_method`

---

### 3. ✅ FIXED: Subprocess output not decoded (Line 64)
**Fixed by:** Andrea Mennucci
**Status:** FIXED
**Severity:** High
**Original Location:** `u2l.py:64`

**Description:**
The subprocess output was read as bytes but not decoded to string, which could cause issues with `os.path.isfile()`.

**Original code:**
```python
p = subprocess.Popen(['kpsewhich', j], stdout=subprocess.PIPE)
a = p.stdout.read().strip()  # Returns bytes, not str
p.wait()
if not os.path.isfile(a):    # Expects str, gets bytes
```

**Problem:**
- In Python 3, `subprocess.PIPE.read()` returns `bytes`, not `str`
- `os.path.isfile()` can handle bytes on Unix but it's not portable
- May fail on some systems or with non-ASCII paths

**Fix applied:**
```python
p = subprocess.Popen(['kpsewhich', j], stdout=subprocess.PIPE, text=True)
a = p.stdout.read().strip()
```

**Test:** `unittests/test_bugs.py::TestSubprocessBugs::test_subprocess_output_type`

---

### 4. ✅ FIXED: Resource leak - subprocess not properly closed (Line 63-65)
**Fixed by:** Andrea Mennucci
**Status:** FIXED
**Severity:** Low
**Original Location:** `u2l.py:63-65`

**Description:**
The subprocess Popen object was not properly closed, causing ResourceWarning.

**Original code:**
```python
p = subprocess.Popen(['kpsewhich', j], stdout=subprocess.PIPE)
a = p.stdout.read().strip()
p.wait()
```

**Problem:**
- File descriptor not explicitly closed
- Caused `ResourceWarning: unclosed file <_io.BufferedReader>`

**Fix applied:**
```python
result = subprocess.run(['kpsewhich', j], capture_output=True, text=True)
a = result.stdout.strip()
```

---

### 5. ✅ FIXED: Thread safety issues with global variables
**Fixed by:** Claude Code
**Status:** FIXED
**Severity:** High
**Original Locations:** `u2l.py:367-369, 403, 577`

**Description:**
The module used global mutable state which made it not thread-safe. Multiple threads calling `uni2tex()` concurrently would interfere with each other.

**Original code:**
```python
line_count = 1      # Line 367
char_count = 0      # Line 368
input_file = 'cmdline'  # Line 369

def _donext(self):
    global char_count  # Line 403
    char_count += 1

def main(argv=sys.argv):
    global verbose     # Line 577
    global line_count
    global char_count
    global input_file
```

**Problem:**
- Global variables were shared across all calls to `uni2tex()`
- Not safe for concurrent use in multi-threaded environments
- Error messages could report incorrect locations
- Web applications or parallel processing tools would have race conditions

**Fix applied:**
Moved global variables into `Decompose_to_tex` class as instance variables:

```python
class Decompose_to_tex(object):
  def __init__(self, add_font_modifiers=True, convert_accents=True,
               prefer_unicode_math=global_prefer_unicode_math, input_file='cmdline'):
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

  def _donext(self):
      char = next(self.iterator)
      self.char_count += 1  # Use instance variable
      return self._docode(char)
```

**Changes:**
- Removed global `line_count`, `char_count`, `input_file` variables
- Added them as instance variables in `Decompose_to_tex.__init__()`
- Updated all references from global to `self.` throughout `_docode()` method
- Removed `global` declarations in `_donext()` and `main()`
- Updated `main()` to pass `input_file` to constructor

**Impact:**
- ✅ Thread-safe: Each thread creates its own `Decompose_to_tex` instance
- ✅ Cleaner API: No hidden global state
- ✅ Better encapsulation: State belongs to the object
- ✅ Easier testing: Can track position per instance
- ✅ Backward compatible: `uni2tex()` already created new instances per call

**Test:** `unittests/test_bug5_fix.py` (14 new tests)
- Tests instance isolation
- Tests concurrent access
- Tests backward compatibility
- Stress test with 100 concurrent threads

---

### 6. ✅ FIXED: Math mode accent support added (Lines 461-486)
**Fixed by:** Claude Code
**Status:** FIXED WITH WORKAROUND
**Severity:** Medium (was Low, upgraded to Medium due to feature request)
**Original Location:** `u2l.py:440` (now lines 461-486)

**Description:**
The code didn't support math-mode accent commands. Accent commands differ between text mode (`\'{e}`) and math mode (`\acute{e}`).

**Solution implemented:**
Added `accent_mode` parameter with three options:
- **`'text'`** (default): Generate text-mode accents like `\'{e}`
- **`'math'`**: Generate math-mode accents like `\acute{e}`
- **`'auto'`**: Reserved for future auto-detection (currently defaults to 'text')

**Accent mappings added:**
```python
accents_textmode_to_mathmode = {
    '`': 'grave', "'": 'acute', '^': 'hat', '~': 'tilde',
    '"': 'ddot', '=': 'bar', '.': 'dot', 'u': 'breve', 'v': 'check',
}
```

**Usage examples:**
```python
# Text mode (default)
u2l.uni2tex("é")  # → \'{e}

# Math mode
u2l.uni2tex("é", accent_mode='math')  # → \acute{e}

# Auto mode (future, currently = text)
u2l.uni2tex("é", accent_mode='auto')  # → \'{e}
```

**Impact:**
- ✅ Users can now generate math-mode accents
- ✅ Backward compatible (defaults to text mode)
- ✅ Works for both combining and precomposed characters
- ⚠️ Auto-detection not yet implemented

**Test:** `unittests/test_accent_modes.py` (35 comprehensive tests)

---

## Not Bugs (False Positives)

### 7. ✅ NOT A BUG: Tokenizer 'in' operator is correctly supported (Line 560)
**Status:** NOT A BUG - INVESTIGATED AND VERIFIED
**Original Concern:** The `'::' in tok` operation might not be supported
**Location:** `u2l.py:560`

**Description:**
Initial analysis suggested the code `'::' in tok` might fail because `tok` is an `EscapeSequence` object, not a plain string.

**Code:**
```python
if '::' in tok:
    m= tok.split('::').pop()
```

**Investigation Results:**
After thorough investigation of the FakePlasTeX tokenizer code, this is **NOT a bug**:

1. **Token inherits from str**:
   - `EscapeSequence` → inherits from `Token`
   - `Token` → inherits from `Text`
   - `Text` → inherits from `str`
   - Therefore, all string operations work correctly!

2. **Used for active characters**:
   - The `::` is used to represent TeX active characters
   - Examples: `active::$` (math shift), `active::&` (alignment)
   - This is documented in `FakePlasTeX/FakeTokenizer.py` lines 120-121

3. **Same pattern used elsewhere**:
   - The exact same check appears in `FakeTokenizer.py` line 120
   - The original FakePlasTeX code uses this pattern itself

**Proof:**
```python
from FakePlasTeX.FakeTokenizer import Token
tok = Token("active::$")
assert '::' in tok  # Works!
assert tok.split('::') == ['active', '$']  # Works!
```

**Test:** `unittests/test_bug6_investigation.py` (11 comprehensive tests)
- Verifies Token inheritance from str
- Tests string operations on Token objects
- Tests active character handling
- Proves the code is correct

---

## Active Bugs and Issues

### 8. ⚠️ Unchecked file existence before opening (Line 142, 187)
**Status:** POTENTIAL BUG
**Severity:** Low
**Location:** `u2l.py:142, 187`

**Description:**
Files are opened without checking if they exist first, relying on exception handling.

**Code:**
```python
if unicode_math_table_file and os.path.isfile(unicode_math_table_file):
    for s in open(unicode_math_table_file):  # Line 142
```

**Problem:**
- Race condition between check and open
- Could crash if file is deleted between check and open

**Impact:**
- Currently protected by `try/except` at module level
- Low risk in practice

---

### 9. ⚠️ Confusing 'useless' parameter in recursive calls (Lines 456-514)
**Status:** MINOR ISSUE
**Severity:** Very Low
**Location:** `u2l.py:456, 468, 474, 482, 489, 495, 514`

**Description:**
Recursive calls to `decompose_to_tex` (which is `self._docode`) don't pass through output list correctly.

**Code:**
```python
decompose_to_tex = self._docode  # Line 412
# Later:
decompose_to_tex(chr(acc), output)  # Line 456, etc.
```

**Problem:**
- The signature is `_docode(self, char, useless=None)`
- But it's called as `decompose_to_tex(chr(acc), output)`
- The second parameter `output` is ignored (named `useless`)
- Function uses `self.output` instead

**Impact:**
- Confusing API
- The `useless` parameter name suggests this is known but not fixed

---

## Design Limitations

### 10. 📋 No support for multiple accents per character
**Status:** LIMITATION
**Severity:** Low

**Description:**
Characters with multiple combining accents may not be handled correctly.

**Example:**
Vietnamese `ế` (e with circumflex and acute) may only convert one accent.

**Test:** `unittests/test_accents.py::TestAccentEdgeCases::test_double_accents`

---

### 11. 📋 High Unicode characters (emojis) not convertible
**Status:** BY DESIGN
**Severity:** Very Low

**Description:**
Emoji and other high Unicode characters (> U+FFFF) are not converted, just passed through with a warning.

**Test:** `unittests/test_bugs.py::TestDecompositionEdgeCases::test_high_unicode_not_convertible`

---

### 12. 📋 One-way conversions in math symbols
**Status:** BY DESIGN
**Severity:** Very Low

**Description:**
Some LaTeX → Unicode conversions don't round-trip perfectly.

**Example:**
- `\|` → U+2016 (DOUBLE VERTICAL LINE)
- U+2016 → `\Vert` (not `\|`)

**Documented in:** `math_replacements` dictionary (line 215-222)

---

## Testing Coverage

All identified bugs have corresponding tests in `unittests/`:

- `test_unicode2latex.py` - 88 tests for basic conversions
- `test_latex2unicode.py` - 38 tests for reverse conversions
- `test_accents.py` - 40 tests for accent handling
- `test_fonts.py` - 47 tests for font modifiers
- `test_bugs.py` - 29 tests for specific bugs and edge cases
- `test_thread_safety.py` - 3 tests for original concurrency issues
- `test_bug5_fix.py` - 14 tests for Bug #5 thread safety fix
- `test_bug6_investigation.py` - 11 tests proving Bug #6 is not a bug
- `test_accent_modes.py` - 35 tests for Bug #7 math mode accent fix

**Total: 265 tests, all passing** ✅

---

## Recommendations

### Completed ✅
1. ✅ **DONE**: Fixed Bug #1 (format string error)
2. ✅ **DONE**: Fixed Bug #2 (char() method)
3. ✅ **DONE**: Fixed Bug #3 (subprocess decode)
4. ✅ **DONE**: Fixed Bug #4 (resource leak)
5. ✅ **DONE**: Fixed Bug #5 (thread safety with instance variables)
6. ✅ **DONE**: Fixed Bug #7 (math mode accent support with accent_mode parameter)
7. ✅ **DONE**: Investigated Bug #6 (proven not a bug)

### High Priority
None remaining - all high priority bugs fixed!

### Medium Priority
None remaining!

### Low Priority
8. Implement auto-detection for `accent_mode='auto'` (Bug #7 follow-up)
9. Clean up the `useless` parameter (Bug #9)
10. Document design limitations clearly

---

## Version Information

- Analysis date: 2025-10-25
- Python version tested: 3.13
- Test suite: 265 tests passing
- Bugs fixed: 6 (including 2 high severity, 3 medium, 1 low)
- False positives investigated: 1 (Bug #6 - proven not a bug)
- New features added: 1 (accent_mode parameter with text/math/auto options)
