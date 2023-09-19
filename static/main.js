const actionElem = document.getElementById("action-select");
const sourceElems = document.getElementsByName("source-radios");
const destElems = document.getElementsByName("dest-radios");
const resultsElem = document.getElementById("results");
const warningElem = document.getElementById("warning");
const optionElems = document.getElementsByName("option-checkboxes");

function copyToClipboard(currObj) {
  const parentOfSelected = currObj.parentNode;
  const children = parentOfSelected.childNodes;
  for (const child of children) {
    if (child.className === "code") {
      navigator.clipboard.writeText(child.textContent);
    }
  }
}

async function getRegexs() {
  let source;
  let dest;
  let action;
  let selectedOptions = [];

  for (const entry of sourceElems) {
    if (entry.checked) source = entry.value;
  }
  for (const entry of destElems) {
    if (entry.checked) dest = entry.value;
  }
  for (const elem of optionElems) {
    if (elem.checked) {
      selectedOptions.push(elem.id);
    }
  }
  action = actionElem.value;
  const data = {
    action: action,
    source: source,
    dest: dest,
    options: selectedOptions,
  };
  const response = await fetch("/api/get-regexs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  resultsElem.innerHTML = "";
  const responseData = await response.json();
  for (let regex of responseData["results"]["regexs"]) {
    const html = `<p><span id=\"action-span\"><code class=\"code\">${regex}</code>&nbsp;&nbsp;<button onclick=\"copyToClipboard(this)\">Copy</button></span></p>`;
    resultsElem.insertAdjacentHTML("beforeend", html);
  }
  warningElem.innerHTML = `<p>${responseData["results"]["help"]}</p>`;
}
getRegexs();
