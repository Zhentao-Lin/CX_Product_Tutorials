/* global EasyMDE, marked */

let mde;
let products = [];
let currentProduct = "";
let currentStem = "";
let editKind = "chapter";
let dirty = false;

const snippets = {
  table: `| 名称 | 说明 |
|------|------|
| 示例 | 请修改 |`,
  code: "```cpp\nvoid setup() {\n  // 你的代码\n}\n```",
};

function toast(msg, isError) {
  const el = document.getElementById("toast");
  el.hidden = false;
  el.textContent = msg;
  el.style.background = isError ? "#cf222e" : "#24292f";
  setTimeout(() => { el.hidden = true; }, 6000);
}

async function api(url, opts = {}) {
  const r = await fetch(url, opts);
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || j.detail || r.statusText);
  return j;
}

function updatePreview() {
  const text = mde ? mde.value() : "";
  document.getElementById("preview").innerHTML = marked.parse(text, { breaks: true });
}

function setDirty(v) {
  dirty = v;
}

async function ensureSavedBeforeSwitch() {
  if (!dirty) return true;
  return confirm("当前内容未保存，确定放弃修改并切换？");
}

function updatePanels() {
  const isHome = editKind === "home";
  const isProduct = editKind === "product";
  const isChapter = editKind === "chapter";
  document.getElementById("productPanel").hidden = isHome;
  document.getElementById("productMeta").hidden = !isProduct;
  document.getElementById("chapterPanel").hidden = !isChapter;
  document.getElementById("chapterToolbar").hidden = !isChapter;
  document.getElementById("btnUploadImg").hidden = !isChapter;
}

async function loadHome() {
  const data = await api("/api/home");
  mde.value(data.content);
  setDirty(false);
  updatePreview();
}

async function loadProductOutline() {
  if (!currentProduct) return;
  const data = await api(`/api/product?id=${encodeURIComponent(currentProduct)}`);
  document.getElementById("fieldTitle").value = data.title || "";
  document.getElementById("fieldStatus").value = data.status || "";
  document.getElementById("fieldSummary").value = data.summary || "";
  mde.value(data.outline || "");
  setDirty(false);
  updatePreview();
}

async function loadProducts() {
  const data = await api("/api/products");
  products = data.products;
  const sel = document.getElementById("productSelect");
  sel.innerHTML = "";
  products.forEach((p) => {
    const o = document.createElement("option");
    o.value = p.id;
    o.textContent = p.title;
    sel.appendChild(o);
  });
  if (products.length) {
    if (!currentProduct || !products.find((x) => x.id === currentProduct)) {
      currentProduct = products[0].id;
    }
    sel.value = currentProduct;
    renderChapters();
  }
  await refreshGitStatus();
}

function renderChapters() {
  const p = products.find((x) => x.id === currentProduct);
  const ul = document.getElementById("chapterList");
  ul.innerHTML = "";
  (p?.chapters || []).forEach((ch) => {
    const li = document.createElement("li");
    li.textContent = `${ch.stem} — ${ch.title}`;
    li.dataset.stem = ch.stem;
    if (ch.stem === currentStem && editKind === "chapter") li.classList.add("active");
    li.onclick = () => {
      editKind = "chapter";
      document.getElementById("editKind").value = "chapter";
      openChapter(ch.stem);
    };
    ul.appendChild(li);
  });
}

async function openChapter(stem) {
  if (!(await ensureSavedBeforeSwitch())) return;
  if (!currentProduct) {
    toast("请先选择或新建产品", true);
    return;
  }
  const data = await api(
    `/api/chapter?product=${encodeURIComponent(currentProduct)}&stem=${encodeURIComponent(stem)}`
  );
  currentStem = stem;
  editKind = "chapter";
  document.getElementById("editKind").value = "chapter";
  updatePanels();
  mde.value(data.content);
  setDirty(false);
  renderChapters();
  updatePreview();
}

async function writeCurrentDoc() {
  if (editKind === "home") {
    await api("/api/home", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: mde.value() }),
    });
  } else if (editKind === "product") {
    if (!currentProduct) throw new Error("请选择产品");
    await api("/api/product", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: currentProduct,
        title: document.getElementById("fieldTitle").value,
        status: document.getElementById("fieldStatus").value,
        summary: document.getElementById("fieldSummary").value,
        outline: mde.value(),
      }),
    });
  } else if (editKind === "chapter") {
    if (!currentStem) throw new Error("请选择章节");
    await api("/api/chapter", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product: currentProduct,
        stem: currentStem,
        content: mde.value(),
      }),
    });
  }
  setDirty(false);
}

async function refreshGitStatus() {
  try {
    const s = await api("/api/status");
    document.getElementById("gitStatus").textContent = `分支: ${s.branch}\n${s.status || "(无未提交改动)"}`;
  } catch {
    document.getElementById("gitStatus").textContent = "无法读取 Git 状态";
  }
}

document.getElementById("editKind").onchange = async (e) => {
  if (!(await ensureSavedBeforeSwitch())) {
    e.target.value = editKind;
    return;
  }
  editKind = e.target.value;
  updatePanels();
  if (editKind === "home") await loadHome();
  else if (editKind === "product") await loadProductOutline();
  else if (products.find((x) => x.id === currentProduct)?.chapters?.length) {
    await openChapter(products.find((x) => x.id === currentProduct).chapters[0].stem);
  } else {
    currentStem = "";
    mde.value("");
    updatePreview();
  }
};

document.getElementById("productSelect").onchange = async (e) => {
  if (!(await ensureSavedBeforeSwitch())) {
    e.target.value = currentProduct;
    return;
  }
  currentProduct = e.target.value;
  renderChapters();
  if (editKind === "product") await loadProductOutline();
  else if (editKind === "chapter") {
    const p = products.find((x) => x.id === currentProduct);
    if (p?.chapters?.length) await openChapter(p.chapters[0].stem);
    else {
      currentStem = "";
      mde.value("");
      updatePreview();
    }
  }
};

document.getElementById("btnNewProduct").onclick = async () => {
  const id = prompt("新产品 ID（如 CX_ESP32_S31_Module_Xiaozhi_Board）：");
  if (!id) return;
  const title = prompt("产品显示名称：");
  if (!title) return;
  const summary = prompt("产品简介（可留空）：", `${title} 教程`);
  const addChapter = confirm("是否同时创建第一章 01-overview？");
  const body = { id, title, summary: summary || "" };
  if (addChapter) {
    body.chapter = "01-overview";
    body.chapter_title = "概述";
  }
  try {
    await api("/api/product", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    currentProduct = id;
    await loadProducts();
    document.getElementById("productSelect").value = id;
    toast("产品已创建，已加入站点总纲列表。请保存并发布。");
    editKind = "product";
    document.getElementById("editKind").value = "product";
    updatePanels();
    await loadProductOutline();
  } catch (err) {
    toast(err.message, true);
  }
};

document.getElementById("btnNewChapter").onclick = async () => {
  if (!currentProduct) {
    toast("请先选择产品", true);
    return;
  }
  const stem = prompt("新章节文件名（如 03-wifi）：");
  if (!stem) return;
  const title = prompt("章节标题：", "新章节");
  if (!title) return;
  try {
    await api("/api/chapter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product: currentProduct, stem, title }),
    });
    await loadProducts();
    editKind = "chapter";
    document.getElementById("editKind").value = "chapter";
    updatePanels();
    await openChapter(stem.replace(/\.md$/, ""));
    toast("章节已创建");
  } catch (err) {
    toast(err.message, true);
  }
};

["fieldTitle", "fieldStatus", "fieldSummary"].forEach((id) => {
  document.getElementById(id).addEventListener("input", () => setDirty(true));
});

document.querySelectorAll("[data-snippet]").forEach((btn) => {
  btn.onclick = () => {
    const key = btn.dataset.snippet;
    mde.codemirror.replaceSelection("\n\n" + snippets[key] + "\n");
    setDirty(true);
    updatePreview();
  };
});

document.getElementById("btnUploadImg").onclick = () => document.getElementById("fileImg").click();

document.getElementById("fileImg").onchange = async (e) => {
  const file = e.target.files?.[0];
  if (!file || editKind !== "chapter") return;
  const fd = new FormData();
  fd.append("product", currentProduct);
  fd.append("file", file);
  try {
    const r = await fetch("/api/upload-image", { method: "POST", body: fd });
    const j = await r.json();
    if (!r.ok) throw new Error(j.error || "上传失败");
    mde.codemirror.replaceSelection("\n\n" + j.markdown + "\n");
    setDirty(true);
    updatePreview();
    toast("图片已上传并插入引用");
  } catch (err) {
    toast(err.message, true);
  }
  e.target.value = "";
};

document.getElementById("btnDeleteChapter").onclick = async () => {
  if (editKind !== "chapter" || !currentStem) return;
  if (!confirm(`确定删除章节 ${currentStem}？`)) return;
  try {
    await api(
      `/api/chapter?product=${encodeURIComponent(currentProduct)}&stem=${encodeURIComponent(currentStem)}`,
      { method: "DELETE" }
    );
    currentStem = "";
    await loadProducts();
    toast("章节已删除");
    mde.value("");
    updatePreview();
  } catch (err) {
    toast(err.message, true);
  }
};

document.getElementById("btnSave").onclick = async () => {
  try {
    await writeCurrentDoc();
    const msg = document.getElementById("commitMsg").value.trim();
    const j = await api("/api/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg || undefined }),
    });
    toast(j.message || "保存成功");
    await refreshGitStatus();
    await loadProducts();
  } catch (err) {
    toast(err.message, true);
  }
};

document.getElementById("btnPublish").onclick = async () => {
  if (!confirm("推送到 GitHub，网站约 1～2 分钟更新。继续？")) return;
  try {
    if (dirty) await writeCurrentDoc();
    const msg = document.getElementById("commitMsg").value.trim();
    await api("/api/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg || undefined }),
    });
    const j = await api("/api/publish", { method: "POST" });
    toast(j.message);
    await refreshGitStatus();
  } catch (err) {
    toast(err.message, true);
  }
};

window.addEventListener("DOMContentLoaded", () => {
  mde = new EasyMDE({
    element: document.getElementById("editor"),
    spellChecker: false,
    autofocus: true,
    status: false,
    toolbar: false,
  });
  mde.codemirror.on("change", () => {
    setDirty(true);
    updatePreview();
  });
  updatePanels();
  loadProducts()
    .then(() => {
      if (products[0]?.chapters?.length) return openChapter(products[0].chapters[0].stem);
    })
    .catch((e) => toast(e.message, true));
});