from flask import Flask, request, render_template

app = Flask(__name__)


OPTIONS = {
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
            r"(?:add|adc|sub|sbb) (?:{source}), 0x.*?;",
        ],
        "help": "When adding an immediate value, only the source regex is used."
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
            r"int3;",
        ],
        "help": "Source and destination registers are ignored.",
    },
    "flags": {
        "name": "Set/Clear Flags",
        "regexs": [
            r"(?:stc|clc)",
        ],
        "help": "Source and destination registers are ignored.",
    }
}


def format_action(action_name, source, dest, options):
    if source == "any":
        source = "e[abcds][ipx]"
    if dest == "any":
        dest = "e[abcds][ipx]"
    regexs = [item.format(source=source, dest=dest) for item in AVAILABLE_ACTIONS[action_name]["regexs"]]
    for option in options:
        if option == 'no_call':
            regexs = [rf"(?!.*call.*){item}" for item in regexs]
        if option == 'no_large_retn':
            regexs = [rf"{item}.*(?:ret;|retn 0x00[012][02468ACE];)" for item in regexs]
        if option == 'no_esp':
            regexs = [rf"(?!.*esp.*){item}" for item in regexs]
    return {"regexs": regexs, "help": AVAILABLE_ACTIONS[action_name].get("help")}


@app.get("/")
def home_get():
    return render_template("home.j2", registers=REGISTERS, available_actions=AVAILABLE_ACTIONS, source="eax", dest="eax", options=OPTIONS)


@app.post("/api/get-regexs")
def get_regexs():
    data = request.json
    selected_action = data["action"]
    source = data["source"]
    dest = data["dest"]
    options = data["options"]
    results = format_action(selected_action, source, dest, options)
    return {"results": results}


if __name__ == "__main__":
    app.run()
