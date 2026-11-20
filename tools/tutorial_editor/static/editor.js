/* global EasyMDE, marked */

let mde;
let products = [];
let currentProduct = "";
let currentStem = "";
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
  setTimeout(() => { el.hidden = true; }, 5000);
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
    currentProduct = products[0].id;
    sel.value = currentProduct;
    renderChapters();
    if (products[0].chapters.length) {
      await openChapter(products[0].chapters[0].stem);
    }
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
    if (ch.stem === currentStem) li.classList.add("active");
    li.onclick = () => openChapter(ch.stem);
    ul.appendChild(li);
  });
}

async function openChapter(stem) {
  if (dirty && !confirm("当前章节有未保存修改，继续切换？")) return;
  const data = await api(`/api/chapter?product=${encodeURIComponent(currentProduct)}&stem=${encodeURIComponent(stem)}`);
  currentStem = stem;
  mde.value(data.content);
  setDirty(false);
  renderChapters();
  updatePreview();
}

async function writeChapter() {
  if (!currentStem) throw new Error("请先选择章节");
  await api("/api/chapter", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      product: currentProduct,
      stem: currentStem,
      content: mde.value(),
    }),
  });
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

document.getElementById("productSelect").onchange = async (e) => {
  currentProduct = e.target.value;
  renderChapters();
  const p = products.find((x) => x.id === currentProduct);
  if (p?.chapters?.length) await openChapter(p.chapters[0].stem);
  else {
    currentStem = "";
    mde.value("");
    updatePreview();
  }
};

document.getElementById("btnNewChapter").onclick = async () => {
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
    currentProduct = document.getElementById("productSelect").value;
    await openChapter(stem.replace(/\.md$/, ""));
    toast("章节已创建");
  } catch (err) {
    toast(err.message, true);
  }
};

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
  if (!file) return;
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
  if (!currentStem) return;
  if (!confirm(`确定删除章节 ${currentStem}？此操作在「保存」后才会提交到 Git。`)) return;
  try {
    await api(`/api/chapter?product=${encodeURIComponent(currentProduct)}&stem=${encodeURIComponent(currentStem)}`, { method: "DELETE" });
    await loadProducts();
    toast("章节已删除");
  } catch (err) {
    toast(err.message, true);
  }
};

document.getElementById("btnSave").onclick = async () => {
  try {
    if (currentStem) await writeChapter();
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
  if (!confirm("将推送到 GitHub，网站约在 1～2 分钟内更新。继续？")) return;
  try {
    if (currentStem && dirty) await writeChapter();
    if (dirty) {
      await api("/api/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: document.getElementById("commitMsg").value || undefined }),
      });
    }
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
  loadProducts().catch((e) => toast(e.message, true));
});