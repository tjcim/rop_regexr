"""Options for app"""

REGEX_OPTIONS = {
    "no_large_retn": {"name": "No Large RetN", "status": True},
    "no_call": {"name": "No Call", "status": True},
    "no_esp": {"name": "No ESP", "status": False},
}
REGISTERS = ["eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp", "any"]
AVAILABLE_ACTIONS = {
    "copy": {
        "name": "Copy/Move",
        "regexs": [
            r"mov {dest}, {source}",
            r"lea {dest}, \[{source}(?:[\+-]0x.*?)?\]",
            r"push {source}.*pop {dest}",
            r"(?:add|adc|xor|or|and|sub|sbb) (?P&lt;dest&gt;{dest}), (?!\1){source}(?!.*pop \1.*)",
            r"xchg (?:{source}|{dest}), (?:{source}|{dest})",
        ],
        "help": "",
    },
    "add_subtract": {
        "name": "Add/Subtract",
        "regexs": [
            r"(?:add|adc|sub|sbb) (?P&lt;dest&gt;{source}), (?!\1)(?:{source}|{dest})",
            r"(?:add|adc|sub|sbb) (?:{source}), 0x.*?[ ]*;",
        ],
        "help": "When adding an immediate value, only the source regex is used.",
    },
    "mov_deref_source": {
        "name": "Dereference Source",
        "regexs": [
            r"mov {dest}, (?:dword )?\[{source}(?:[\+-]0x.*?)?\]",
            r"(?:add|adc|xor|or|and|sub|sbb|xchg) (?P&lt;dest&gt;{dest}), \[{source}(?:[\+-]0x.*?)?\]",
        ],
        "help": "",
    },
    "deref_dest": {
        "name": "Dereference Dest",
        "regexs": [
            r"mov \[{dest}(?:[\+-]0x.*?)?\], (?:dword )?{source}",
            r"(?:add|adc|xor|or|and|sub|sbb|xchg) (?P&lt;dest&gt;\[{dest}(?:[\+-]0x.*?)?\]), {source}",
        ],
        "help": "",
    },
    "zero": {
        "name": "Zero Register",
        "regexs": [
            r"(?:xor|sub|sbb) (?P&lt;source&gt;{source}), \1",
            r"(?:mul|imul) {source}",
            r"(?:shr|sar|shl|sal) {source}",
            r"cdq",  # extends sign from eax to edx
        ],
        "help": "Only the source register is used for this action.",
    },
    "negate": {
        "name": "Negate Register",
        "regexs": [
            r"(?:neg|not) {source}",  # not is simple bit flip
        ],
        "help": "Only the source register is used for this action.",
    },
    "interrupt": {
        "name": "Interrupt",
        "regexs": [
            r"int3[ ]*;",
        ],
        "help": "Source and destination registers are ignored.",
    },
    "flags": {
        "name": "Set/Clear Flags",
        "regexs": [
            r"(?:stc|clc)",
        ],
        "help": "Source and destination registers are ignored.",
    },
}
