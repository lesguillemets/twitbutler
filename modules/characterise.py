#!/usr/bin/env python3
import unicodedata as unic

def char_data(char : str) -> "{data}":
    if len(char) != 1:
        raise ValueError("Unicode string of length 1 is required.")
    return {
        'char' : char,
        'hex' : hex(ord(char)),
        'name' : unic.name(char),
        'cat' : unic_cats[unic.category(char)],
    }

unic_cats = {
    "Cc" : "Other, Control",
    "Cf" : "Other, Format",
    "Cn" : "Other, Not Assigned",
    "Co" : "Other, Private Use",
    "Cs" : "Other, Surrogate",
    "LC" : "Letter, Cased",
    "Ll" : "Letter, Lowercase",
    "Lm" : "Letter, Modifier",
    "Lo" : "Letter, Other",
    "Lt" : "Letter, Titlecase",
    "Lu" : "Letter, Uppercase",
    "Mc" : "Mark, Spacing Combining",
    "Me" : "Mark, Enclosing",
    "Mn" : "Mark, Nonspacing",
    "Nd" : "Number, Decimal Digit",
    "Nl" : "Number, Letter",
    "No" : "Number, Other",
    "Pc" : "Punctuation, Connector",
    "Pd" : "Punctuation, Dash",
    "Pe" : "Punctuation, Close",
    "Pf" : "Punctuation, Final quote",
    "Pi" : "Punctuation, Initial quote",
    "Po" : "Punctuation, Other",
    "Ps" : "Punctuation, Open",
    "Sc" : "Symbol, Currency",
    "Sk" : "Symbol, Modifier",
    "Sm" : "Symbol, Math",
    "So" : "Symbol, Other",
    "Zl" : "Separator, Line",
    "Zp" : "Separator, Paragraph",
    "Zs" : "Separator, Space",
}


if __name__ == "__main__":
    print(char_data('あ'))
    print(char_data('a'))
    print(char_data('A'))
    print(char_data('2'))
    print(char_data('â'))
    print(char_data('δ'))
    print(char_data('㈣'))
    print(char_data('"'))
    print(char_data('ɞ'))
    print(char_data('🎼'))
