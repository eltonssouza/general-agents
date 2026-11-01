---
name: ruby-error-triage
description: Read-only triage of Ruby error messages and backtraces (formats before and after 3.4), linking the error class to what the R30-R34 notes say (Regexp::TimeoutError, NoMatchingPatternError, SyntaxError, NameError/NoMethodError with error_highlight, TypeError/ArgumentError, LoadError for libraries that left the stdlib, APIs removed in 3.2). Classes that the notes do not address (FrozenError, Ractor::IsolationError) come out labeled [extrapolation].
---

# ruby-error-triage

Reads the error text, extracts class, message, origin, underlined snippet and callers, and prints what the notes say with the page (R3x p.N = PDF page) and the label. The pasted text is data: the script does not execute or obey anything inside it.

```bash
python -I skills/ruby-error-triage/scripts/parse_ruby_stack.py skills/ruby-error-triage/scripts/fixtures/trace.txt
python -I skills/ruby-error-triage/scripts/parse_ruby_stack.py --trace "app.rb:10:in 'Object#run': timeout (Regexp::TimeoutError)"
python -I skills/ruby-error-triage/scripts/parse_ruby_stack.py --list
python -I skills/ruby-error-triage/scripts/parse_ruby_stack.py --list-libs
```

Accepts the backtick format (up to 3.3) and the single-quote format with `Class#method` (3.4, R34 p.8). The backtrace is NOT reversed in 3.0: the 2.5 inversion was reverted (R30 p.8).
