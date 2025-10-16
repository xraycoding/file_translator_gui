document.addEventListener("DOMContentLoaded", async () => {
  const langSelect = document.getElementById("langSelect");
  const fileInput = document.getElementById("fileInput");
  const translateBtn = document.getElementById("translateBtn");
  const status = document.getElementById("status");
  const output = document.getElementById("output");

  // Load available languages from Python
  const langs = await eel.get_languages()();
  langs.forEach(l => {
    const opt = document.createElement("option");
    opt.textContent = l;
    langSelect.appendChild(opt);
  });

  translateBtn.addEventListener("click", async () => {
    if (!fileInput.files.length) {
      status.textContent = "Please select a .txt file first.";
      return;
    }

    const file = fileInput.files[0];
    const filePath = file.path || file.name;
    const selectedLang = langSelect.value;

    status.textContent = "Translating...";
    output.textContent = "";

    const result = await eel.translate_file(filePath, selectedLang)();
    output.textContent = result;
    status.textContent = "Done ✅";
  });

  let filePath = "";
  let languages = [];

  eel.get_languages()((langs) => {
    const sel = document.getElementById("lang");
    langs.forEach((l) => {
      const opt = document.createElement("option");
      opt.textContent = l;
      sel.appendChild(opt);
    });
    languages = langs;
  });

  async function selectFile() {
    filePath = await eel.select_file()();
    document.getElementById("output").textContent = filePath
      ? `Selected: ${filePath}`
      : "No file selected.";
  }

  async function translateFile() {
    if (!filePath) {
      document.getElementById("output").textContent = "Please select a file first.";
      return;
    }
    const lang = document.getElementById("lang").value;
    document.getElementById("output").textContent = "Translating...";
    const result = await eel.translate_file(filePath, lang)();
    document.getElementById("output").textContent = result;
  }
});
