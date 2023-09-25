from flask import Flask, request, render_template

from available_actions import AVAILABLE_ACTIONS

app = Flask(__name__)


OPTIONS = {
    "no_large_retn": {"name": "No Large RetN", "status": True},
    "no_call": {"name": "No Call", "status": True},
    "no_esp": {"name": "No ESP", "status": False},
}
REGISTERS = ["eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp", "any"]


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
            regexs = [rf"{item}.*(?:ret;|retn 0x00[012][0-9A-F];)" for item in regexs]
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
