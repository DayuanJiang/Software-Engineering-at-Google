(function () {
  "use strict";
  const base = new URL(".", document.baseURI);
  const asset = (path) => new URL(path, base).href;
  const storageKey = "sweg-reader-preferences-v1";
  const han = /[\u3400-\u9fff]/;
  let preferences = { mode: "bilingual", size: 19, code: "original",
    theme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light" };
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    if (["bilingual", "chinese"].includes(saved.mode)) preferences.mode = saved.mode;
    if (Number.isFinite(saved.size)) preferences.size = Math.max(16, Math.min(22, Math.round(saved.size)));
    if (["light", "dark"].includes(saved.theme)) preferences.theme = saved.theme;
    if (typeof saved.lastRoute === "string") preferences.lastRoute = saved.lastRoute;
    if (["original", "python"].includes(saved.code)) preferences.code = saved.code;
  } catch (_) { /* Reading remains available when local storage is restricted. */ }
  document.documentElement.dataset.theme = preferences.theme;
  document.documentElement.style.setProperty("--reading-size", preferences.size + "px");
  const svgCache = new Map();
  const manifestPromise = fetch(asset("assets/reader-manifest.json")).then((response) => {
    if (!response.ok) throw new Error("Reader manifest unavailable");
    return response.json();
  });
  let currentPage = null;
  let currentGuide = null;
  let routeVersion = 0;
  let resizeObservers = [];
  let headings = [];
  let scrollFrame = 0;
  let viewerScale = 1;
  let viewerSvg = null;
  let viewerFocus = null;
  let viewerSequence = 0;
  let svgSequence = 0;
  let updateSidebar = () => {};
  let closeNote = () => {};
  let closeSettings = () => {};
  let bindNote = () => {};
  const noteContent = new Map();
  let preparationError = null;

  function routePage(vm, manifest) {
    const file = decodeURIComponent(vm.route.file || "").replace(/^\/+/, "");
    return manifest.chapters.find((page) => file.endsWith(page.file)) || null;
  }

  function icon(name) {
    return '<svg class="reader-icon" aria-hidden="true"><use href="' +
      asset("assets/reader-icons.svg") + "#icon-" + name + '"></use></svg>';
  }
  function button(label, name, extraClass = "") {
    const node = document.createElement("button");
    node.type = "button";
    node.className = "icon-button " + extraClass;
    node.title = label;
    node.setAttribute("aria-label", label);
    node.innerHTML = icon(name);
    return node;
  }
  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify(preferences)); } catch (_) {}
  }
  function applyPreferences() {
    closeNote();
    document.documentElement.dataset.theme = preferences.theme;
    document.documentElement.style.setProperty("--reading-size", preferences.size + "px");
    document.body.dataset.readingMode = preferences.mode;
    document.querySelectorAll("[data-reader-mode]").forEach((node) => {
      node.setAttribute("aria-pressed", String(node.dataset.readerMode === preferences.mode));
    });
    document.querySelectorAll("[data-reader-code]").forEach((node) => {
      node.setAttribute("aria-pressed", String(node.dataset.readerCode === preferences.code));
    });
    const size = document.getElementById("reader-font-value");
    if (size) size.textContent = String(preferences.size);
    const minus = document.getElementById("reader-font-minus");
    const plus = document.getElementById("reader-font-plus");
    if (minus) minus.disabled = preferences.size <= 16;
    if (plus) plus.disabled = preferences.size >= 22;
    const theme = document.getElementById("reader-theme");
    if (theme) {
      const label = preferences.theme === "light" ? "切换深色" : "切换浅色";
      theme.innerHTML = icon(preferences.theme === "light" ? "moon" : "sun");
      theme.title = label;
      theme.setAttribute("aria-label", label);
    }
  }
  function keepPosition(change) {
    const candidates = [...document.querySelectorAll("#main > p, #main > h2, #main > h3")];
    const target = candidates.find((node) => !node.classList.contains("translated-source") &&
      node.getBoundingClientRect().bottom > 160 && getComputedStyle(node).display !== "none");
    const top = target ? target.getBoundingClientRect().top : 0;
    change();
    if (target) window.scrollBy(0, target.getBoundingClientRect().top - top);
    updateScroll();
  }
  function menuState() {
    const narrow = matchMedia("(max-width: 900px)").matches;
    const open = narrow ? document.body.classList.contains("close") : !document.body.classList.contains("close");
    document.getElementById("reader-menu")?.setAttribute("aria-expanded", String(open));
    document.querySelector(".toc-toggle")?.setAttribute("aria-expanded", String(document.body.classList.contains("toc-open")));
  }
  function toggleMenu() {
    document.body.classList.remove("toc-open");
    document.body.classList.toggle("close");
    menuState();
  }

  function mountChrome() {
    if (document.querySelector(".reader-topbar")) return;
    const sidebar = document.querySelector(".sidebar");
    if (sidebar) sidebar.id = "reader-sidebar";
    const header = document.createElement("header");
    header.className = "reader-topbar";
    const main = document.createElement("div");
    main.className = "reader-topbar-main";
    const menu = button("章节目录", "menu");
    menu.id = "reader-menu";
    menu.setAttribute("aria-controls", "reader-sidebar");
    menu.addEventListener("click", (event) => {
      event.stopPropagation();
      toggleMenu();
    });
    const brand = document.createElement("span");
    brand.className = "reader-brand";
    brand.textContent = "谷歌的软件工程";
    main.append(menu, brand);
    const controls = document.createElement("div");
    controls.className = "reader-preferences";
    const mode = document.createElement("div");
    mode.className = "mode-switch";
    mode.setAttribute("role", "group");
    mode.setAttribute("aria-label", "阅读模式");
    [["bilingual", "中英对照"], ["chinese", "中文优先"]].forEach(([value, label]) => {
      const item = document.createElement("button");
      item.type = "button";
      item.dataset.readerMode = value;
      item.textContent = value === "bilingual" ? "中英" : "中文";
      item.setAttribute("aria-label", label); item.title = label;
      item.addEventListener("click", () => keepPosition(() => {
        preferences.mode = value;
        applyPreferences();
        persist();
      }));
      mode.append(item);
    });
    const font = document.createElement("div");
    font.className = "font-control";
    font.setAttribute("role", "group");
    font.setAttribute("aria-label", "正文字号");
    const decrease = button("减小字号", "minus");
    decrease.id = "reader-font-minus";
    const increase = button("增大字号", "plus");
    increase.id = "reader-font-plus";
    const value = document.createElement("output");
    value.id = "reader-font-value";
    value.setAttribute("aria-live", "polite");
    decrease.addEventListener("click", () => changeFont(-1));
    increase.addEventListener("click", () => changeFont(1));
    font.append(decrease, value, increase);
    controls.append(mode);
    const actions = document.createElement("div");
    actions.className = "reader-topbar-actions";
    const toc = button("本章目录", "list", "toc-toggle");
    toc.setAttribute("aria-controls", "reader-toc");
    toc.addEventListener("click", () => {
      if (matchMedia("(max-width: 900px)").matches) {
        document.body.classList.remove("close"); menuState();
      }
      const open = document.body.classList.toggle("toc-open");
      toc.setAttribute("aria-expanded", String(open));
    });
    const theme = button("切换深色", "moon");
    theme.id = "reader-theme";
    theme.addEventListener("click", () => {
      preferences.theme = preferences.theme === "light" ? "dark" : "light";
      applyPreferences(); persist();
    });
    const appearance = button("阅读设置", "type");
    appearance.id = "reader-appearance";
    appearance.setAttribute("aria-controls", "reader-settings");
    appearance.setAttribute("aria-expanded", "false");
    const settings = document.createElement("section");
    settings.id = "reader-settings"; settings.className = "reader-settings"; settings.hidden = true;
    settings.setAttribute("aria-label", "阅读设置");
    const settingsTitle = document.createElement("h2"); settingsTitle.textContent = "阅读设置";
    const sizeLabel = document.createElement("span"); sizeLabel.textContent = "字号";
    const sizeRow = document.createElement("div"); sizeRow.className = "settings-row";
    sizeRow.append(sizeLabel, font);
    const themeLabel = document.createElement("span"); themeLabel.textContent = "外观";
    const themeRow = document.createElement("div"); themeRow.className = "settings-row";
    themeRow.append(themeLabel, theme);
    const codeLabel = document.createElement("span"); codeLabel.textContent = "代码示例";
    const codeSwitch = document.createElement("div"); codeSwitch.className = "mode-switch";
    codeSwitch.setAttribute("role", "group"); codeSwitch.setAttribute("aria-label", "代码示例语言");
    [["original", "原文"], ["python", "Python"]].forEach(([value, label]) => {
      const item = document.createElement("button");
      item.type = "button"; item.dataset.readerCode = value; item.textContent = label;
      item.addEventListener("click", () => {
        preferences.code = value; applyPreferences(); persist();
        const main = document.getElementById("main");
        if (main && currentPage) applyCodeVariants(main, currentPage, routeVersion);
      });
      codeSwitch.append(item);
    });
    const codeRow = document.createElement("div"); codeRow.className = "settings-row";
    codeRow.append(codeLabel, codeSwitch);
    settings.append(settingsTitle, sizeRow, themeRow, codeRow);
    closeSettings = (restoreFocus = false) => {
      if (settings.hidden) return;
      settings.hidden = true; appearance.setAttribute("aria-expanded", "false");
      if (restoreFocus) appearance.focus();
    };
    appearance.addEventListener("click", () => {
      const open = settings.hidden;
      settings.hidden = !open; appearance.setAttribute("aria-expanded", String(open));
      if (open) {
        closeNote();
        const bounds = appearance.getBoundingClientRect();
        settings.style.right = Math.max(12, innerWidth - bounds.right) + "px";
        decrease.focus();
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (!settings.contains(event.target) && !appearance.contains(event.target)) closeSettings();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !settings.hidden) closeSettings(true);
    });
    const repo = document.createElement("a");
    repo.className = "icon-button"; repo.href = "https://github.com/DayuanJiang/Software-Engineering-at-Google";
    repo.target = "_blank"; repo.rel = "noopener noreferrer";
    repo.title = "GitHub 仓库"; repo.setAttribute("aria-label", "GitHub 仓库");
    repo.innerHTML = icon("github");
    actions.append(appearance, toc, repo);
    const progress = document.createElement("div");
    progress.className = "reader-progress";
    progress.setAttribute("role", "progressbar");
    progress.setAttribute("aria-label", "阅读进度");
    progress.setAttribute("aria-valuemin", "0");
    progress.setAttribute("aria-valuemax", "100");
    progress.innerHTML = "<span></span>";
    header.append(main, controls, actions, progress);
    document.body.append(header);
    document.body.append(settings);
    const scrim = document.createElement("button");
    scrim.type = "button"; scrim.className = "sidebar-scrim";
    scrim.setAttribute("aria-label", "收起章节目录");
    scrim.addEventListener("click", toggleMenu);
    document.body.append(scrim);
    const aside = document.createElement("nav");
    aside.id = "reader-toc"; aside.className = "reader-toc";
    aside.setAttribute("aria-label", "本章目录");
    document.body.append(aside);
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !document.querySelector("dialog[open]")) {
        document.body.classList.remove("toc-open");
        if (matchMedia("(max-width: 900px)").matches) document.body.classList.remove("close");
        menuState();
      }
    });
    const sidebarRoot = document.querySelector(".sidebar");
    if (sidebarRoot) {
      updateSidebar = () => {
        const name = sidebarRoot.querySelector(".app-name");
        if (name && sidebarRoot.firstElementChild !== name) sidebarRoot.prepend(name);
        const brandLink = name?.querySelector("a");
        if (brandLink && !brandLink.dataset.readerBrand) {
          brandLink.dataset.readerBrand = "true";
          const book = document.createElement("span"); book.textContent = "谷歌的软件工程";
          const original = document.createElement("small"); original.textContent = "Software Engineering at Google";
          brandLink.replaceChildren(book, original);
        }
        sidebarRoot.querySelectorAll(".sidebar-nav > ul > li > a").forEach((link) => {
          const route = decodeURIComponent(new URL(link.href).hash.split("?")[0]).replace(/^#/, "").replace(/\.md$/, "");
          link.parentElement.classList.toggle("active", route === currentPage?.route);
        });
      };
      new MutationObserver(updateSidebar).observe(sidebarRoot, { childList: true, subtree: true });
      updateSidebar();
      mountSearch(sidebarRoot);
    }
    document.addEventListener("click", (event) => {
      if (event.target.closest(".sidebar-nav a") && matchMedia("(max-width: 900px)").matches) {
        document.body.classList.remove("close"); menuState();
      }
    });
    document.querySelector(".skip-link")?.addEventListener("click", (event) => {
      event.preventDefault();
      const content = document.getElementById("main");
      content?.setAttribute("tabindex", "-1");
      content?.focus();
      content?.scrollIntoView();
    });
    mountViewer();
    mountNotePopover();
    applyPreferences(); menuState();
    window.addEventListener("scroll", updateScroll, { passive: true });
    window.addEventListener("resize", () => {
      menuState(); updateScroll(); closeSettings(); if (viewerSvg) fitViewer();
    }, { passive: true });
  }
  function changeFont(delta) {
    keepPosition(() => {
      preferences.size = Math.max(16, Math.min(22, preferences.size + delta));
      applyPreferences(); persist();
    });
  }

  function cleanTitle(main) {
    if (!main.querySelector(":scope > h1")) {
      const first = main.querySelector(":scope > h2");
      if (first) {
        const h1 = document.createElement("h1");
        h1.id = first.id; h1.innerHTML = first.innerHTML; first.replaceWith(h1);
      }
    }
    const title = [...main.querySelectorAll(":scope > h1")].find((node) => han.test(node.textContent));
    const englishTitle = [...main.querySelectorAll(":scope > h1")].find((node) => !han.test(node.textContent));
    if (title && englishTitle) {
      const subtitle = document.createElement("p");
      subtitle.className = "reader-original-title";
      subtitle.lang = "en";
      subtitle.id = englishTitle.id;
      subtitle.innerHTML = englishTitle.innerHTML;
      englishTitle.replaceWith(subtitle);
    }
    [...main.children].forEach((node) => {
      const text = node.textContent.trim();
      if (node.tagName === "P" && /^CHAPTER\s+\d+$/.test(text.replace(/\*/g, "").trim())) node.classList.add("chapter-kicker");
      if (node.tagName === "P" && /^(?:—|--|——)\s*\S/.test(text) && text.length < 120) {
        node.classList.add("reader-attribution");
      }
      const continuedCredit = node.previousElementSibling?.classList.contains("chapter-credit") &&
        node.children.length && [...node.children].every((child) => child.tagName === "STRONG") && /\sEdited by\b/.test(text);
      if (node.tagName === "P" && (/^(Written|Edited) by\b/.test(text) || continuedCredit)) {
        node.classList.add("chapter-credit"); node.lang = "en";
        const original = document.createElement("span");
        original.className = "credit-original"; original.textContent = text;
        const translated = document.createElement("span");
        translated.className = "credit-chinese"; translated.lang = "zh-CN";
        translated.textContent = text.replace(/^Written by\s*/, "作者：").replace(/(?:^|\s)Edited by\s*/, "；编辑：").replace(/^；/, "");
        node.replaceChildren(original, translated);
      }
      if (node.tagName === "P" && text.length < 100 && han.test(text) && /[a-zA-Z]/.test(text) &&
        node.children.length && [...node.childNodes].every((child) => child.nodeType === Node.TEXT_NODE ?
          !child.textContent.trim() : child.tagName === "STRONG") && /\s$/.test(text.slice(0, text.search(han)))) {
        node.classList.add("reader-subheading");
        const original = document.createElement("span"); original.className = "heading-original"; original.lang = "en";
        original.textContent = text.slice(0, text.search(han));
        const translated = document.createElement("span"); translated.lang = "zh-CN"; translated.textContent = text.slice(text.search(han));
        node.replaceChildren(original, translated);
      }
    });
    main.querySelectorAll("h2,h3,h4").forEach((heading) => {
      const next = heading.nextElementSibling;
      if (!han.test(heading.textContent) && next?.tagName === heading.tagName && han.test(next.textContent)) {
        const label = next.querySelector(".anchor > span") || next;
        label.prepend(document.createTextNode(heading.textContent.trim() + " "));
        if (heading.id) {
          const alias = document.createElement("span");
          alias.id = heading.id; alias.className = "reader-heading-alias"; alias.setAttribute("aria-hidden", "true");
          next.prepend(alias);
        }
        heading.remove();
      }
    });
    main.querySelectorAll("h2,h3,h4").forEach((heading) => {
      const label = heading.querySelector(".anchor > span") || heading;
      const text = label.textContent;
      const split = text.search(han);
      if (split <= 0 || !/[a-zA-Z]/.test(text.slice(0, split)) || !/\s$/.test(text.slice(0, split))) return;
      const original = document.createElement("span");
      original.className = "heading-original"; original.lang = "en";
      original.textContent = text.slice(0, split).trim() + " ";
      const translated = document.createElement("span");
      translated.lang = "zh-CN"; translated.textContent = text.slice(split);
      label.replaceChildren(original, translated);
    });
    let next = (title || main.querySelector(":scope > h1"))?.nextElementSibling;
    while (next?.classList.contains("chapter-credit")) next = next.nextElementSibling;
    if (next?.tagName === "P" && next.children.length && [...next.childNodes].every((node) =>
      node.nodeType === Node.TEXT_NODE ? !node.textContent.trim() : node.tagName === "EM")) {
      next.classList.add("chapter-epigraph");
    }
  }

  function classifyCaptions(main) {
    const kindLabels = { Figure: "图", Example: "例", Table: "表" };
    for (const paragraph of main.querySelectorAll("p")) {
      if (paragraph.closest("pre,code,.reader-translator-note")) continue;
      const text = paragraph.textContent.trim().replace(/^\*+|\*+$/g, "").trim();
      const english = text.match(/^(Figure|Example|Table)\s*(\d+[-.]\d+)\.?/);
      const chinese = text.match(/^[图表例]\s*\d+[-.]\d+(?:[.：:\s]|$)/);
      if (!english && !chinese) continue;
      paragraph.classList.add("reader-caption");
      if (english && han.test(text)) {
        const firstHan = text.search(han);
        let prefix = text.slice(0, firstHan).trim().replace(/[\s*]+$/, "");
        let translated = text.slice(firstHan).replace(/[\s*]+$/, "");
        if (!/^[图表例]\s*\d/.test(translated)) {
          const repeated = new RegExp(english[1] + "\\s*" + english[2].replace(".", "\\.") + "\\.?\\s*$");
          prefix = prefix.replace(repeated, "").trim();
          translated = kindLabels[english[1]] + english[2] + " " + translated;
        }
        const notes = [...paragraph.querySelectorAll(".note-reference")];
        const original = document.createElement("span");
        original.className = "translated-source"; original.lang = "en";
        original.textContent = prefix + (prefix ? " " : "");
        const target = document.createElement("span"); target.lang = "zh-CN"; target.textContent = translated;
        paragraph.replaceChildren(original, target, ...notes);
      } else if (english) {
        const next = paragraph.nextElementSibling;
        if (next?.tagName === "P" && new RegExp("^[图表例]\\s*" + english[2].replace(".", "\\.")).test(next.textContent.trim())) {
          paragraph.classList.add("translated-source"); next.classList.add("reader-caption");
        }
      } else if (/^\*|\*$/.test(paragraph.textContent.trim())) {
        paragraph.textContent = text;
      }
    }
  }

  function classifyProse(main, page) {
    const normalize = (s) => s.replace(/\s+/g, " ").trim();
    const keep = (page?.keepEnglish || []).map(normalize);
    const isText = (node) => /^(P|UL|OL|LI|BLOCKQUOTE)$/.test(node.tagName) &&
      !node.matches(".chapter-credit,.chapter-kicker,.reader-original-title,.reader-caption,.reader-subheading,.reader-attribution,[data-reviewed-translation]") &&
      !node.closest(".reader-notes,.reader-translator-note") &&
      !node.querySelector("[data-reviewed-translation]") &&
      !node.querySelector("pre,figure,img,table");
    const language = (node) => {
      if (!isText(node)) return "boundary";
      if (/^(UL|OL)$/.test(node.tagName)) {
        const languages = new Set([...node.children].map((child) => han.test(child.textContent) ? "zh" : /[a-zA-Z]/.test(child.textContent) ? "en" : ""));
        if (languages.has("en") && languages.has("zh")) return "boundary";
      }
      const text = node.textContent.trim();
      if (han.test(text)) return "zh";
      return /[a-zA-Z]/.test(text) ? "en" : "boundary";
    };
    [main, ...main.querySelectorAll("blockquote,ul,ol,li")].forEach((container) => {
      const nodes = [...container.children];
      nodes.forEach((node) => {
        if (language(node) === "en") {
          node.classList.add("english-prose"); node.setAttribute("lang", "en");
        }
      });
      let i = 0;
      while (i < nodes.length) {
        if (language(nodes[i]) !== "en") { i += 1; continue; }
        const en = [];
        while (i < nodes.length && language(nodes[i]) === "en") en.push(nodes[i++]);
        const zh = [];
        let j = i;
        while (j < nodes.length && language(nodes[j]) === "zh") zh.push(nodes[j++]);
        if (en.length !== zh.length || !en.every((node, k) => node.tagName === zh[k].tagName)) continue;
        en.forEach((node) => {
          const text = normalize(node.textContent);
          if (!keep.some((source) => source.includes(text) || text.includes(source))) node.classList.add("translated-source");
        });
      }
    });
  }

  // The translation sometimes repeats a code block after both the English and the Chinese paragraph.
  // Keep the copy that follows the Chinese text, hide the earlier copy, and hide list items left empty.
  function hideRepeatedCode(main) {
    const pres = [...main.querySelectorAll("pre")];
    // Compare without shell prompts, whitespace, or a trailing period so a "$ cmd" copy matches "cmd".
    const body = (pre) => (pre.querySelector("code") || pre).textContent.split("\n")
      .map((line) => line.replace(/^\s*\$\s*/, "")).join("").replace(/\s+/g, "").replace(/[.。;]$/, "");
    pres.forEach((pre, i) => {
      if (pres.slice(i + 1).some((other) => body(other) === body(pre))) pre.classList.add("repeated-source");
    });
    main.querySelectorAll("li").forEach((item) => {
      const remaining = [...item.childNodes].filter((node) => node.nodeType === Node.TEXT_NODE
        ? node.textContent.trim() : !node.matches(".translated-source,.repeated-source") && node.textContent.trim());
      if (!remaining.length) item.classList.add("translated-source");
    });
    main.querySelectorAll("ul,ol").forEach((list) => {
      if (list.children.length && [...list.children].every((child) => child.classList.contains("translated-source"))) {
        list.classList.add("translated-source");
      }
    });
  }

  function replaceText(root, text, replacement) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.parentElement.closest("pre,code,.reader-notes,.reader-translator-note")) continue;
      const offset = node.data.indexOf(text);
      if (offset < 0) continue;
      const range = document.createRange();
      range.setStart(node, offset); range.setEnd(node, offset + text.length);
      range.deleteContents(); range.insertNode(replacement);
      return true;
    }
    return false;
  }

  function proseRange(root, text) {
    const normalize = (s) => s.replace(/\[(?:\^\d+|\d+\^)\]/g, "").replace(/\s+/g, " ").trim();
    const needle = normalize(text);
    const blocks = [...root.querySelectorAll("p,li,td,h2,h3,h4")].filter((block) =>
      !block.closest("pre,.reader-translator-note,.chapter-visual,.section-visual") && !block.querySelector("p,li"));
    for (const block of blocks) {
      const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
      const positions = [];
      let flattened = "";
      let current;
      while ((current = walker.nextNode())) {
        if (current.parentElement.closest(".note-trigger")) continue;
        for (let index = 0; index < current.data.length; index++) {
          const reference = current.data.slice(index).match(/^\[(?:\^\d+|\d+\^)\]/);
          if (reference) { index += reference[0].length - 1; continue; }
          const char = current.data[index];
          if (/\s/.test(char)) {
            if (!flattened || flattened.endsWith(" ")) continue;
            flattened += " ";
          } else flattened += char;
          positions.push({ node: current, start: index, end: index + 1 });
        }
      }
      const index = flattened.indexOf(needle);
      if (index < 0) continue;
      const start = positions[index], end = positions[index + needle.length - 1];
      const range = document.createRange();
      range.setStart(start.node, start.start); range.setEnd(end.node, end.end);
      return range;
    }
    return null;
  }

  function insertAfterText(root, text, node) {
    const range = proseRange(root, text);
    if (!range) return false;
    range.collapse(false);
    if (range.endContainer.nodeType === Node.TEXT_NODE && range.endOffset === range.endContainer.length) {
      let sibling = range.endContainer.nextSibling;
      let last = null;
      while (sibling && ((sibling.nodeType === Node.TEXT_NODE && !sibling.textContent) ||
        (sibling.nodeType === Node.ELEMENT_NODE && sibling.classList.contains("note-reference")))) {
        if (sibling.nodeType === Node.ELEMENT_NODE) last = sibling;
        sibling = sibling.nextSibling;
      }
      if (last) { last.after(node); return true; }
    }
    range.insertNode(node); return true;
  }

  function replaceProseText(root, text, node) {
    const range = proseRange(root, text);
    if (!range) return false;
    range.deleteContents(); range.insertNode(node); return true;
  }

  function noteMarker(id, language, serial = 1, label = "注释 " + id) {
    const marker = document.createElement("span"); marker.className = "note-reference";
    const trigger = document.createElement("button");
    trigger.type = "button"; trigger.className = "note-trigger";
    trigger.id = "note-ref-" + id + "-" + language + (serial > 1 ? "-" + serial : "");
    trigger.dataset.note = id; trigger.dataset.noteLanguage = language; trigger.dataset.noteLabel = label;
    trigger.setAttribute("aria-label", "查看" + label);
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-controls", "reader-note-popover");
    trigger.setAttribute("aria-expanded", "false");
    trigger.innerHTML = '<span class="note-dot" aria-hidden="true"></span>';
    bindNote(trigger); marker.append(trigger);
    return marker;
  }

  function htmlContent(html, language, page) {
    const wrapper = document.createElement("div");
    wrapper.lang = language; wrapper.innerHTML = html;
    wrapper.querySelectorAll("a[href]").forEach((link) => {
      const href = link.getAttribute("href");
      if (href.startsWith("#")) return;
      link.href = new URL(href, asset(page.file)).href;
      if (new URL(link.href).origin !== location.origin) {
        link.target = "_blank"; link.rel = "noopener noreferrer";
      }
    });
    return wrapper;
  }

  function reviewedContent(main, page) {
    const review = page?.readerReview;
    if (!review) return;
    const normalize = (text) => text.replace(/\s+/g, " ").trim();
    for (const edit of review.textEdits || []) {
      if (!replaceProseText(main, edit.source, document.createTextNode(edit.replacement))) {
        throw new Error("Reviewed display correction missing: " + edit.source);
      }
    }
    if (review.epigraph) {
      const source = [...main.querySelectorAll(".chapter-epigraph")].find((node) =>
        normalize(node.textContent) === normalize(review.epigraph.english));
      if (!source) throw new Error("Reviewed epigraph no longer matches the chapter");
      const epigraph = document.createElement("blockquote");
      epigraph.className = "chapter-epigraph";
      const english = source.cloneNode(true);
      english.className = "english-prose translated-source"; english.lang = "en";
      const chinese = document.createElement("p"); chinese.lang = "zh-CN";
      chinese.textContent = review.epigraph.chinese;
      const author = document.createElement("cite"); author.textContent = review.epigraph.author;
      epigraph.append(english, chinese, author); source.replaceWith(epigraph);
    }
    for (const item of review.proseCodeBlocks || []) {
      const block = [...main.querySelectorAll("pre")].find((node) => node.textContent.trim() === item.text);
      if (!block) throw new Error("Reviewed quotation no longer matches the chapter");
      if (item.parts) {
        const fragment = document.createDocumentFragment();
        for (const part of item.parts) {
          const quote = document.createElement("blockquote");
          quote.className = "reader-quotation"; quote.lang = part.language === "zh" ? "zh-CN" : "en";
          const content = htmlContent(part.html, quote.lang, page);
          quote.append(...content.childNodes); fragment.append(quote);
        }
        block.replaceWith(fragment);
        continue;
      }
      const quote = document.createElement("blockquote");
      quote.className = "reader-quotation"; quote.lang = item.language === "zh" ? "zh-CN" : "en";
      const paragraph = document.createElement("p");
      paragraph.textContent = item.text.replace(/^\*|\*$/g, "");
      quote.append(paragraph); block.replaceWith(quote);
    }
    for (const [index, item] of (review.translatorNotes || []).entries()) {
      const block = [...main.querySelectorAll("pre")].find((node) => node.textContent.trim() === item.text);
      if (!block && review.format === 2) {
        const id = "translator-" + (index + 1);
        const content = htmlContent(item.bodyHtml, "zh-CN", page);
        if (item.href) {
          const link = document.createElement("a");
          link.href = item.href; link.textContent = item.linkText || "参考来源";
          link.target = "_blank"; link.rel = "noopener noreferrer"; content.append(link);
        }
        noteContent.set(id, { zh: content });
        if (!replaceProseText(main, item.renderedText, noteMarker(id, "zh", 1, item.title || "译者注"))) {
          throw new Error("Inline translator note source missing: " + item.renderedText);
        }
        continue;
      }
      if (!block) throw new Error("Reviewed translator note no longer matches the chapter");
      const details = document.createElement("details"); details.className = "reader-translator-note";
      const title = document.createElement("summary"); title.textContent = item.title;
      const body = document.createElement("p"); body.textContent = item.body;
      const link = document.createElement("a"); link.href = item.href; link.textContent = item.linkText;
      link.target = "_blank"; link.rel = "noopener noreferrer";
      details.append(title, body, link); block.replaceWith(details);
    }
    for (const item of review.translations || []) {
      const normalized = (s) => normalize(s.replace(/\[\^\d+\]/g, ""));
      if (item.kind === "heading") {
        const heading = [...main.querySelectorAll("h2,h3,h4")].find((node) => normalized(node.textContent) === normalized(item.english));
        if (!heading) throw new Error("Reviewed heading translation missing: " + item.english);
        const label = heading.querySelector(".anchor > span") || heading;
        const original = document.createElement("span"); original.className = "heading-original"; original.lang = "en";
        original.textContent = item.english + " ";
        const translated = document.createElement("span"); translated.lang = "zh-CN"; translated.textContent = item.chinese;
        label.replaceChildren(original, translated);
        continue;
      }
      const matches = [...main.querySelectorAll("p,li")].filter((node) =>
        !node.querySelector("p,li") && normalized(node.textContent) === normalized(item.english));
      if (matches.length !== 1) throw new Error("Reviewed translation source not found: " + item.english.slice(0, 70));
      const source = matches[0];
      source.classList.add("english-prose", "translated-source");
      source.dataset.reviewedTranslation = "true"; source.lang = "en";
      if (item.kind === "epigraph" && item.author) {
        const attribution = source.nextElementSibling;
        if (attribution?.classList.contains("reader-attribution") && !han.test(attribution.textContent)) {
          attribution.classList.add("translated-source"); attribution.dataset.reviewedTranslation = "true";
        }
      }
      const translated = htmlContent(item.chineseHtml, "zh-CN", page);
      translated.dataset.reviewedTranslation = "true";
      if (item.kind === "epigraph") translated.className = "chapter-epigraph";
      if (item.author) {
        const author = document.createElement("cite"); author.textContent = item.author;
        translated.append(author);
      }
      source.after(translated);
    }
    buildFootnotes(main, page, review.footnotes || []);
    const tables = [...main.querySelectorAll("table")];
    for (const pair of review.pairedTables || []) {
      for (const language of ["english", "chinese"]) {
        const table = tables[pair[language + "Index"]];
        const headers = table ? [...table.rows[0].cells].map((cell) => normalize(cell.textContent)) : [];
        if (!table || table.rows.length !== pair[language].rows ||
          headers.length !== pair[language].headers.length ||
          headers.some((header, index) => header !== pair[language].headers[index])) {
          throw new Error("Reviewed bilingual table changed: " + page.id);
        }
      }
      const english = tables[pair.englishIndex];
      english.classList.add("translated-source"); english.lang = "en";
      const caption = english.previousElementSibling;
      if (caption?.tagName === "P" && /^Table\s+\d/.test(caption.textContent) && !han.test(caption.textContent)) {
        caption.classList.add("translated-source");
      }
    }
    for (const pair of review.pairedSources || []) {
      const range = proseRange(main, pair.english);
      if (!range || !proseRange(main, pair.chinese)) throw new Error("Reviewed bilingual prose pair not found: " + pair.english.slice(0, 80));
      const parent = (range.commonAncestorContainer.nodeType === Node.ELEMENT_NODE ?
        range.commonAncestorContainer : range.commonAncestorContainer.parentElement).closest("p,li,td");
      if (parent && normalize(parent.textContent) === normalize(pair.english) && !parent.querySelector("pre,img,table")) {
        parent.classList.add("translated-source", "english-prose"); parent.lang = "en";
        parent.dataset.reviewedTranslation = "true";
        const quote = parent.parentElement;
        if (quote.matches("blockquote.reader-quotation") && quote.children.length === 1) quote.classList.add("translated-source");
      } else {
        const original = document.createElement("span");
        original.className = "translated-source"; original.lang = "en";
        original.dataset.reviewedTranslation = "true"; original.append(range.extractContents());
        range.insertNode(original);
      }
    }
    main.querySelectorAll("blockquote").forEach((node) => {
      if (!node.textContent.trim() && !node.querySelector("img,svg,pre")) node.remove();
    });
  }

  function buildFootnotes(main, page, notes) {
    const ids = new Set(notes.map((note) => String(note.id)));
    main.querySelectorAll("a").forEach((link) => {
      const id = link.textContent.trim().match(/^\^(\d+)$/)?.[1];
      if (id && ids.has(id)) link.replaceWith(document.createTextNode("[^" + id + "]"));
    });
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      if (textNode.parentElement.closest("pre,code")) continue;
      textNode.data = textNode.data.replace(/\[(\d+)\^\]/g, (match, id) => ids.has(id) ? "[^" + id + "]" : match);
    }
    for (const note of notes) {
      const prefix = "[^" + note.id + "]:";
      const compiled = page.readerReview.format === 2;
      const english = compiled ? htmlContent(note.englishHtml, "en", page) :
        [...main.querySelectorAll("blockquote > p")].find((node) => node.textContent.trim().startsWith(prefix));
      const chinese = compiled ? htmlContent(note.chineseHtml, "zh-CN", page) : english?.nextElementSibling;
      if (!english || !chinese || !han.test(chinese.textContent)) throw new Error("Unpaired footnote " + note.id);
      const quote = english.parentElement;
      if (!compiled) replaceText(english, prefix, document.createTextNode(""));
      const oldNumber = chinese.textContent.match(new RegExp("^\\s*(?:\\[" + note.id + "\\]|" + note.id + ")\\s+"));
      if (!compiled && oldNumber) replaceText(chinese, oldNumber[0], document.createTextNode(""));
      english.className = ""; english.lang = "en";
      chinese.lang = "zh-CN";
      const citations = new Set([...chinese.querySelectorAll("a[href]")].map((link) => link.href));
      for (const source of english.querySelectorAll("a[href]")) {
        if (citations.has(source.href)) continue;
        const citation = document.createElement("a");
        citation.className = "note-citation"; citation.href = source.href;
        citation.textContent = "参考来源"; citation.title = source.textContent;
        citation.target = "_blank"; citation.rel = "noopener noreferrer";
        chinese.append(document.createTextNode(" "), citation); citations.add(source.href);
      }
      english.remove(); chinese.remove();
      noteContent.set(note.id, { en: english, zh: chinese });
      if (quote && !quote.children.length) quote.remove();
      for (const language of ["en", "zh"]) {
        const findReference = () => {
          const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
          let text;
          while ((text = walker.nextNode())) {
            if (!text.data.includes("[^" + note.id + "]") || text.parentElement.closest("pre,code,.reader-translator-note")) continue;
            const block = text.parentElement.closest("p,li,td");
            if (!block) continue;
            let offset = text.data.indexOf("[^" + note.id + "]");
            while (offset >= 0) {
              const preceding = document.createRange(); preceding.setStart(block, 0); preceding.setEnd(text, offset);
              const firstHan = block.textContent.search(han);
              const markerLanguage = firstHan < 0 || preceding.toString().length < firstHan ? "en" : "zh";
              if (markerLanguage === language) return { text, offset };
              offset = text.data.indexOf("[^" + note.id + "]", offset + 1);
            }
          }
          return null;
        };
        const replaceReference = (reference, replacement) => {
          const range = document.createRange();
          range.setStart(reference.text, reference.offset);
          range.setEnd(reference.text, reference.offset + note.id.length + 3);
          range.deleteContents(); range.insertNode(replacement);
        };
        if ((language === "en" && note.relocateEnglish) || (language === "zh" && note.relocateChinese)) {
          let reference;
          while ((reference = findReference())) replaceReference(reference, document.createTextNode(""));
        }
        if (!findReference()) {
          const after = language === "zh" ? note.after : note.englishAfter;
          if (!after || !insertAfterText(main, after, document.createTextNode("[^" + note.id + "]"))) {
            throw new Error("Footnote reference missing: " + note.id + " " + language);
          }
        }
        let serial = 0;
        let reference;
        while ((reference = findReference())) replaceReference(reference, noteMarker(note.id, language, ++serial));
      }
    }
  }

  function mountNotePopover() {
    const panel = document.createElement("aside");
    panel.id = "reader-note-popover"; panel.className = "note-popover"; panel.hidden = true;
    panel.setAttribute("role", "dialog"); panel.setAttribute("aria-modal", "false");
    panel.setAttribute("aria-labelledby", "reader-note-label");
    const head = document.createElement("div"); head.className = "note-popover-head";
    const label = document.createElement("h2"); label.id = "reader-note-label";
    const dismiss = button("关闭注释", "x");
    const body = document.createElement("div"); body.className = "note-popover-body";
    head.append(label, dismiss); panel.append(head, body); document.body.append(panel);
    let active = null;
    let pinned = false;
    let hideTimer = 0;
    let suppressFocus = false;
    const position = () => {
      if (!active || panel.hidden) return;
      const rect = active.getBoundingClientRect();
      const minimum = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--header-height"), 10) + 12;
      if (rect.bottom < minimum || rect.top > innerHeight) { closeNote(); return; }
      const below = innerHeight - rect.bottom - 20;
      const above = rect.top - minimum - 8;
      panel.style.width = Math.min(380, innerWidth - 32) + "px";
      panel.style.maxHeight = Math.min(420, Math.max(above, below)) + "px";
      const height = panel.offsetHeight;
      const width = panel.offsetWidth;
      const top = below >= height ? rect.bottom + 8 : rect.top - height - 8;
      panel.style.top = Math.max(minimum, Math.min(top, innerHeight - height - 12)) + "px";
      panel.style.left = Math.max(16, Math.min(rect.left + rect.width / 2 - width / 2, innerWidth - width - 16)) + "px";
    };
    closeNote = (restoreFocus = false) => {
      clearTimeout(hideTimer);
      if (!active) return;
      const previous = active;
      previous.setAttribute("aria-expanded", "false");
      panel.hidden = true; active = null; pinned = false;
      if (restoreFocus && previous.isConnected) {
        suppressFocus = true; previous.focus({ preventScroll: true });
        queueMicrotask(() => { suppressFocus = false; });
      }
    };
    const open = (trigger, pin = false) => {
      clearTimeout(hideTimer);
      const content = noteContent.get(trigger.dataset.note)?.[trigger.dataset.noteLanguage];
      if (!content) return;
      if (active && active !== trigger) active.setAttribute("aria-expanded", "false");
      const changed = active !== trigger;
      pinned = changed ? pin : (pinned || pin); active = trigger;
      closeSettings();
      label.textContent = trigger.dataset.noteLabel || "注释 " + trigger.dataset.note;
      if (changed || panel.hidden) {
        body.replaceChildren(content.cloneNode(true)); body.scrollTop = 0;
      }
      panel.hidden = false;
      trigger.setAttribute("aria-expanded", "true");
      position();
    };
    const scheduleClose = () => {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(() => {
        if (!pinned && active && !active.matches(":hover") && !panel.matches(":hover") &&
          active !== document.activeElement && !panel.contains(document.activeElement)) closeNote();
      }, 180);
    };
    bindNote = (trigger) => {
      trigger.addEventListener("pointerenter", (event) => {
        if (event.pointerType === "mouse") open(trigger);
      });
      trigger.addEventListener("pointerleave", scheduleClose);
      trigger.addEventListener("focus", () => { if (!suppressFocus) open(trigger); });
      trigger.addEventListener("blur", scheduleClose);
      trigger.addEventListener("click", () => {
        if (active === trigger && pinned) closeNote();
        else open(trigger, true);
      });
      trigger.addEventListener("keydown", (event) => {
        if (event.key === "ArrowDown" || (event.key === "Tab" && !event.shiftKey && active === trigger)) {
          event.preventDefault(); open(trigger, true); dismiss.focus();
        }
      });
    };
    panel.addEventListener("pointerenter", () => clearTimeout(hideTimer));
    panel.addEventListener("pointerleave", scheduleClose);
    panel.addEventListener("focusout", scheduleClose);
    panel.addEventListener("keydown", (event) => {
      if (event.key === "Tab" && event.shiftKey && event.target === dismiss && active) {
        event.preventDefault(); active.focus();
      }
    });
    dismiss.addEventListener("click", () => closeNote(true));
    document.addEventListener("pointerdown", (event) => {
      if (active && !panel.contains(event.target) && !active.contains(event.target)) closeNote();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && active) {
        event.preventDefault(); closeNote(true);
      }
    });
    window.addEventListener("scroll", position, { passive: true });
    window.addEventListener("resize", position, { passive: true });
  }

  async function loadSvg(path) {
    if (!svgCache.has(path)) {
      svgCache.set(path, fetch(asset(path)).then((response) => {
        if (!response.ok) throw new Error("SVG unavailable: " + path);
        return response.text();
      }).then((text) => {
        const doc = new DOMParser().parseFromString(text, "image/svg+xml");
        const root = doc.documentElement;
        if (doc.querySelector("parsererror") || root.localName !== "svg") throw new Error("Invalid SVG");
        if (root.querySelector("script,foreignObject,image,a")) throw new Error("Active SVG content rejected");
        for (const node of [root, ...root.querySelectorAll("*")]) {
          for (const attr of node.attributes) {
            if (/^on/i.test(attr.name) || (attr.localName === "href" && !attr.value.startsWith("#"))) {
              throw new Error("External/active SVG attribute rejected");
            }
          }
        }
        if (/@import|url\(\s*['"]?(?:https?:|data:|javascript:)/i.test(text)) throw new Error("External SVG styles rejected");
        return root;
      }).catch((error) => { svgCache.delete(path); throw error; }));
    }
    const root = await svgCache.get(path);
    const copy = document.importNode(root, true);
    const scope = "diagram-instance-" + (++svgSequence);
    const chapterClass = [...copy.classList].find((name) => /^cg-ch\d+(?:-\d+)?$/.test(name));
    copy.dataset.svgScope = scope;
    if (chapterClass) {
      copy.querySelectorAll("style").forEach((style) => {
        style.textContent = style.textContent.replaceAll("." + chapterClass, '[data-svg-scope="' + scope + '"]');
      });
    }
    return copy;
  }
  function uniqueSvgIds(svg, prefix) {
    const ids = new Map();
    [svg, ...svg.querySelectorAll("[id]")].filter((node) => node.id).forEach((node) => ids.set(node.id, prefix + node.id));
    [svg, ...svg.querySelectorAll("*")].forEach((node) => {
      if (node.id) node.id = ids.get(node.id);
      for (const attr of [...node.attributes]) {
        let value = attr.value.replace(/url\(#([^)]+)\)/g, (_, id) => "url(#" + (ids.get(id) || id) + ")");
        if (attr.name === "aria-labelledby" || attr.name === "aria-describedby") value = value.split(" ").map((id) => ids.get(id) || id).join(" ");
        if (attr.localName === "href" && value.startsWith("#")) value = "#" + (ids.get(value.slice(1)) || value.slice(1));
        node.setAttribute(attr.name, value);
      }
      if (node.localName === "style") node.textContent = node.textContent.replace(/url\(#([^)]+)\)/g, (_, id) => "url(#" + (ids.get(id) || id) + ")");
    });
    svg.setAttribute("aria-labelledby", (svg.getAttribute("aria-labelledby") || "").split(" ").map((id) => ids.get(id) || id).join(" "));
    return svg;
  }

  async function insertGuide(main, guide, version) {
    const isSection = Boolean(guide.afterParagraph);
    const figure = document.createElement(isSection ? "figure" : "details");
    figure.className = isSection ? "section-visual" : "chapter-visual";
    if (!isSection) figure.open = true;
    figure.dataset.chapter = String(guide.chapter);
    figure.dataset.guide = guide.id || "ch" + String(guide.chapter).padStart(2, "0");
    const caption = document.createElement(isSection ? "figcaption" : "summary");
    const marker = document.createElement("span"); marker.className = "guide-label";
    marker.innerHTML = icon("book-open"); marker.append(document.createTextNode("本章图解"));
    const title = document.createElement(isSection ? "span" : "h2");
    title.className = "guide-title"; title.textContent = guide.title; title.id = "guide-" + (guide.id || guide.chapter);
    const expand = button("放大图解", "maximize-2");
    expand.addEventListener("click", () => openViewer(guide, expand).catch((error) => {
      console.error(error);
      summary.textContent = "图解暂时无法加载";
    }));
    const chevron = document.createElement("span"); chevron.className = "guide-chevron";
    chevron.innerHTML = icon("chevron-down");
    if (isSection) caption.append(title, expand);
    else caption.append(marker, title, chevron);
    const toolbar = document.createElement("div"); toolbar.className = "diagram-toolbar";
    if (!isSection) toolbar.append(expand);
    const stage = document.createElement("div");
    stage.className = "diagram-stage";
    stage.innerHTML = '<div class="diagram-loading" role="status">图解加载中</div>';
    const summary = document.createElement("p");
    summary.className = "guide-summary"; summary.textContent = guide.summary;
    if (isSection) figure.append(caption, stage, summary);
    else figure.append(caption, toolbar, stage, summary);
    const chineseTitle = [...main.querySelectorAll(":scope > h1")].find((node) => han.test(node.textContent));
    let anchor = chineseTitle || main.querySelector("h1,h2");
    let next = anchor?.nextElementSibling;
    while (next?.classList.contains("chapter-credit")) { anchor = next; next = next.nextElementSibling; }
    if (isSection) {
      const normalized = (s) => s.replace(/\s+/g, " ").trim();
      anchor = [...main.querySelectorAll(":scope > p, :scope > [data-reviewed-translation] > p")].find((node) =>
        normalized(node.textContent).includes(normalized(guide.afterParagraph)));
      if (!anchor) throw new Error("Section guide insertion point missing: " + guide.id);
    }
    if (anchor) anchor.after(figure); else main.prepend(figure);
    let selected = "";
    let request = 0;
    const render = async () => {
      const path = (stage.clientWidth || main.clientWidth) < 560 ? guide.mobile : guide.desktop;
      if (path === selected) return;
      selected = path;
      const serial = ++request;
      try {
        const svg = await loadSvg(path);
        if (version !== routeVersion || serial !== request || !figure.isConnected) return;
        stage.replaceChildren(svg);
        figure.dataset.layout = path === guide.mobile ? "mobile" : "desktop";
      } catch (error) {
        if (!figure.isConnected) return;
        stage.innerHTML = '<p class="diagram-loading" role="status">图解暂时无法加载</p>';
        console.error(error);
      }
    };
    await render();
    if (version !== routeVersion || !figure.isConnected) return;
    const observer = new ResizeObserver(render);
    observer.observe(stage); resizeObservers.push(observer);
    if (!isSection) figure.addEventListener("toggle", () => { if (figure.open) render(); });
  }

  function buildToc(main) {
    const toc = document.getElementById("reader-toc");
    toc.replaceChildren();
    const title = document.createElement("h2"); title.textContent = "本章目录";
    const close = button("收起本章目录", "x", "reader-toc-close");
    close.addEventListener("click", () => {
      document.body.classList.remove("toc-open"); menuState();
    });
    toc.append(title, close);
    headings = [...main.querySelectorAll("h2[id],h3[id]")];
    for (const heading of headings) {
      const link = document.createElement("a");
      const text = heading.textContent.trim();
      const firstHan = text.search(han);
      link.textContent = firstHan >= 0 ? text.slice(firstHan) : text;
      link.href = "#" + (currentPage?.route || "/") + "?id=" + encodeURIComponent(heading.id);
      link.dataset.heading = heading.id;
      link.dataset.depth = heading.tagName.slice(1);
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const disclosure = heading.closest("details");
        if (disclosure) disclosure.open = true;
        heading.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
        history.replaceState(null, "", link.href);
        document.body.classList.remove("toc-open");
        menuState();
      });
      toc.append(link);
    }
    updateScroll();
  }
  function updateScroll() {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      scrollFrame = 0;
      const total = document.documentElement.scrollHeight - innerHeight;
      const percent = total > 0 ? Math.min(100, Math.max(0, scrollY / total * 100)) : 100;
      const bar = document.querySelector(".reader-progress");
      if (bar) {
        bar.setAttribute("aria-valuenow", String(Math.round(percent)));
        bar.firstElementChild.style.transform = "scaleX(" + percent / 100 + ")";
      }
      let active = headings[0];
      const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--header-height"), 10) + 70;
      for (const heading of headings) if (heading.getBoundingClientRect().top <= offset) active = heading;
      document.querySelectorAll(".reader-toc a").forEach((node) => {
        if (node.dataset.heading === active?.id) node.setAttribute("aria-current", "location");
        else node.removeAttribute("aria-current");
      });
    });
  }

  function footer(main, manifest, page) {
    const index = manifest.chapters.findIndex((c) => c.id === page?.id);
    const nav = document.createElement("nav");
    nav.className = "chapter-pagination"; nav.setAttribute("aria-label", "章节翻页");
    [index - 1, index + 1].forEach((i, position) => {
      const chapter = manifest.chapters[i];
      if (!chapter || index < 0) return;
      const link = document.createElement("a");
      link.href = "#" + chapter.route;
      link.dataset.direction = position ? "next" : "previous";
      const text = document.createElement("span");
      const label = document.createElement("small"); label.textContent = position ? "下一篇" : "上一篇";
      text.append(label, document.createTextNode(chapter.title));
      const marker = document.createElement("span"); marker.innerHTML = icon(position ? "chevron-right" : "chevron-left");
      if (!position) link.append(marker, text); else link.append(text, marker);
      nav.append(link);
    });
    main.append(nav);
  }

  // Per-chapter review data (footnotes, translations, display edits) is fetched on demand.
  function loadReview(page) {
    if (!page.review) return Promise.resolve(null);
    if (!page.reviewPromise) {
      page.reviewPromise = fetch(asset(page.review)).then((response) => {
        if (!response.ok) throw new Error("Reader review unavailable: " + page.id);
        return response.json();
      }).then((review) => { page.readerReview = review; return review; })
        .catch((error) => { delete page.reviewPromise; throw error; });
    }
    return page.reviewPromise;
  }

  // Code examples: highlight originals, and optionally swap in Python rewrites loaded per chapter.
  const PRISM_ALIASES = { "c++": "cpp", golang: "go" };
  const LANGUAGE_LABELS = { java: "Java", cpp: "C++", c: "C", go: "Go" };
  function highlightCode(code, language) {
    const prism = window.Prism;
    const grammar = prism && prism.languages[language];
    if (grammar) return prism.highlight(code, grammar, language);
    return code.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
  }
  function highlightOriginals(main) {
    for (const pre of main.querySelectorAll("pre[data-lang]")) {
      const code = pre.querySelector("code");
      const language = PRISM_ALIASES[pre.dataset.lang.toLowerCase()] || pre.dataset.lang.toLowerCase();
      if (!code || code.querySelector(".token") || !window.Prism?.languages[language]) continue;
      code.innerHTML = highlightCode(code.textContent, language);
      code.className = "lang-" + language;
    }
  }
  function loadCodeVariants(page) {
    if (!page?.codeVariants) return Promise.resolve([]);
    if (!page.variantsPromise) {
      page.variantsPromise = fetch(asset(page.codeVariants)).then((response) => {
        if (!response.ok) throw new Error("Code variants unavailable: " + page.id);
        return response.json();
      }).catch((error) => { delete page.variantsPromise; throw error; });
    }
    return page.variantsPromise;
  }
  // Each translated example carries a small language tab group in its corner. The tabs switch the
  // global preference, so choosing Python on one block switches every block in the book.
  const variantState = new WeakMap();
  function languageTabs(variant) {
    const tabs = document.createElement("div");
    tabs.className = "code-lang-tabs"; tabs.setAttribute("role", "group"); tabs.setAttribute("aria-label", "代码示例语言");
    const label = LANGUAGE_LABELS[variant.language] || variant.language;
    [["python", "Python"], ["original", "原文"]].forEach(([value, text]) => {
      const tab = document.createElement("button");
      tab.type = "button"; tab.dataset.code = value; tab.textContent = text;
      if (value === "original") tab.title = "原书示例：" + label;
      if (value === "python" && !variant.python) {
        tab.setAttribute("aria-disabled", "true"); tab.title = variant.note;
      } else {
        tab.addEventListener("click", () => {
          if (preferences.code === value) return;
          preferences.code = value; applyPreferences(); persist();
          const main = document.getElementById("main");
          if (main && currentPage) applyCodeVariants(main, currentPage, routeVersion);
        });
      }
      tabs.append(tab);
    });
    return tabs;
  }
  async function applyCodeVariants(main, page, version) {
    let variants;
    try { variants = await loadCodeVariants(page); } catch (error) { console.error(error); return; }
    if (version !== routeVersion) return;
    for (const variant of variants) {
      for (const pre of main.querySelectorAll("pre")) {
        const code = pre.querySelector("code");
        if (!code) continue;
        let state = variantState.get(pre);
        if (!state) {
          if (pre.textContent.trim() !== variant.source) continue;
          state = { variant, html: code.innerHTML, className: code.className, lang: pre.dataset.lang || "" };
          variantState.set(pre, state);
          pre.classList.add("has-lang-tabs");
          pre.prepend(languageTabs(variant));
        } else if (state.variant !== variant) continue;
        const python = preferences.code === "python" && variant.python;
        code.innerHTML = python ? highlightCode(variant.python, "python") : state.html;
        code.className = python ? "lang-python" : state.className;
        pre.dataset.lang = python ? "python" : state.lang;
        pre.querySelectorAll(".code-lang-tabs button").forEach((tab) => {
          tab.setAttribute("aria-pressed", String(tab.dataset.code === (python ? "python" : "original")));
        });
      }
    }
  }

  // Full-text search over a prebuilt index; the index is downloaded only when someone searches.
  let searchIndexPromise = null;
  function loadSearchIndex() {
    if (!searchIndexPromise) {
      searchIndexPromise = fetch(asset("assets/search-index.json")).then((response) => {
        if (!response.ok) throw new Error("Search index unavailable");
        return response.json();
      }).catch((error) => { searchIndexPromise = null; throw error; });
    }
    return searchIndexPromise;
  }
  function highlight(text, query) {
    const fragment = document.createDocumentFragment();
    const lower = text.toLowerCase();
    let from = 0, at;
    while ((at = lower.indexOf(query, from)) >= 0) {
      fragment.append(text.slice(from, at));
      const mark = document.createElement("mark"); mark.textContent = text.slice(at, at + query.length);
      fragment.append(mark);
      from = at + query.length;
    }
    fragment.append(text.slice(from));
    return fragment;
  }
  function mountSearch(sidebar) {
    const box = document.createElement("div"); box.className = "search"; box.setAttribute("role", "search");
    const wrap = document.createElement("div"); wrap.className = "input-wrap";
    const input = document.createElement("input");
    input.type = "search"; input.name = "book-search"; input.placeholder = "搜索全书"; input.autocomplete = "off";
    input.setAttribute("aria-label", "搜索全书");
    const clear = button("清除搜索", "x", "clear-button");
    const results = document.createElement("div"); results.className = "results-panel";
    results.setAttribute("aria-live", "polite");
    wrap.append(input, clear); box.append(wrap, results);
    sidebar.insertBefore(box, sidebar.querySelector(".sidebar-nav"));
    const show = (nodes) => { results.replaceChildren(...nodes); sidebar.classList.toggle("searching", nodes.length > 0); };
    const message = (text) => { const p = document.createElement("p"); p.className = "search-message"; p.textContent = text; return p; };
    const run = async () => {
      const query = input.value.trim().toLowerCase();
      if (!query) { show([]); return; }
      let index;
      try { index = await loadSearchIndex(); } catch (_) { show([message("搜索暂时无法使用")]); return; }
      if (input.value.trim().toLowerCase() !== query) return;
      const nodes = [];
      for (const entry of index) {
        const at = entry.text.toLowerCase().indexOf(query);
        if (at < 0 && !entry.title.toLowerCase().includes(query)) continue;
        const link = document.createElement("a"); link.className = "matching-post";
        link.href = "#" + entry.route + "?id=" + encodeURIComponent(window.Docsify.slugify(entry.title));
        const title = document.createElement("h2"); title.append(highlight(entry.title, query));
        const chapter = document.createElement("small"); chapter.textContent = entry.chapter;
        const start = Math.max(0, Math.max(at, 0) - 40);
        const excerpt = (start > 0 ? "…" : "") + entry.text.slice(start, start + 140) + (start + 140 < entry.text.length ? "…" : "");
        const snippet = document.createElement("p"); snippet.append(highlight(excerpt, query));
        link.append(title, chapter, snippet);
        nodes.push(link);
        if (nodes.length === 40) break;
      }
      show(nodes.length ? nodes : [message("没有找到结果")]);
    };
    let timer = 0;
    input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 150); });
    clear.addEventListener("click", () => { input.value = ""; show([]); input.focus(); });
    results.addEventListener("click", (event) => {
      if (event.target.closest("a") && matchMedia("(max-width: 900px)").matches) {
        document.body.classList.remove("close"); menuState();
      }
    });
  }

  function mountViewer() {
    const dialog = document.createElement("dialog");
    dialog.className = "diagram-modal"; dialog.id = "diagram-modal";
    dialog.setAttribute("aria-labelledby", "diagram-modal-title");
    const head = document.createElement("div"); head.className = "diagram-modal-head";
    const title = document.createElement("h2"); title.id = "diagram-modal-title";
    const controls = document.createElement("div"); controls.className = "diagram-modal-controls";
    const minus = button("缩小图解", "minus");
    const plus = button("放大图解比例", "plus");
    const fit = button("适应窗口", "minimize-2");
    const close = button("关闭图解", "x");
    const output = document.createElement("output"); output.id = "diagram-zoom";
    output.setAttribute("aria-live", "polite");
    const download = document.createElement("a");
    download.id = "diagram-download"; download.className = "icon-button";
    download.title = "下载 SVG"; download.setAttribute("aria-label", "下载 SVG"); download.innerHTML = icon("download");
    minus.addEventListener("click", () => resizeViewer(viewerScale - .25));
    plus.addEventListener("click", () => resizeViewer(viewerScale + .25));
    fit.addEventListener("click", fitViewer);
    close.addEventListener("click", () => dialog.close());
    controls.append(minus, output, plus, fit, download, close);
    head.append(title, controls);
    const viewport = document.createElement("div"); viewport.className = "diagram-viewport";
    viewport.innerHTML = '<div class="diagram-canvas"></div>';
    dialog.append(head, viewport);
    dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener("close", () => {
      document.body.classList.remove("diagram-open"); viewerSvg = null;
      if (viewerFocus?.isConnected) viewerFocus.focus();
    });
    document.body.append(dialog);
  }
  async function openViewer(guide, trigger) {
    const dialog = document.getElementById("diagram-modal");
    viewerFocus = trigger;
    const path = innerWidth < 600 ? guide.mobile : guide.desktop;
    const svg = uniqueSvgIds(await loadSvg(path), "viewer-" + (++viewerSequence) + "-");
    dialog.querySelector("#diagram-modal-title").textContent = guide.title;
    const download = dialog.querySelector("#diagram-download");
    download.href = asset(path); download.download = path.split("/").pop();
    dialog.querySelector(".diagram-canvas").replaceChildren(svg);
    viewerSvg = svg;
    dialog.showModal(); document.body.classList.add("diagram-open");
    fitViewer();
  }
  function fitViewer() {
    if (!viewerSvg) return;
    const viewport = document.querySelector(".diagram-viewport");
    const box = viewerSvg.viewBox.baseVal;
    const width = Math.min(viewport.clientWidth - 40, (viewport.clientHeight - 40) * box.width / box.height);
    viewerSvg.dataset.fitWidth = String(Math.max(180, width));
    resizeViewer(1);
  }
  function resizeViewer(scale) {
    if (!viewerSvg) return;
    viewerScale = Math.max(.5, Math.min(3, scale));
    const width = Number(viewerSvg.dataset.fitWidth) * viewerScale;
    const box = viewerSvg.viewBox.baseVal;
    viewerSvg.style.width = width + "px";
    viewerSvg.style.height = width * box.height / box.width + "px";
    document.getElementById("diagram-zoom").textContent = Math.round(viewerScale * 100) + "%";
  }

  window.$docsify.plugins = [].concat(window.$docsify.plugins || [], function (hook, vm) {
    hook.mounted(mountChrome);
    hook.beforeEach((markdown, next) => {
      closeNote(); closeSettings(); noteContent.clear();
      routeVersion += 1;
      const version = routeVersion;
      preparationError = null;
      const main = document.getElementById("main");
      if (main) delete main.dataset.readerReady;
      resizeObservers.forEach((observer) => observer.disconnect()); resizeObservers = [];
      headings = [];
      document.getElementById("diagram-modal")?.close();
      manifestPromise.then(async (manifest) => {
        if (version !== routeVersion) { next(markdown); return; }
        const page = routePage(vm, manifest);
        const review = page ? await loadReview(page) : null;
        if (version !== routeVersion) { next(markdown); return; }
        let prepared = markdown;
        for (const edit of [...(review?.sourceEdits || [])].sort((a, b) => b.startLine - a.startLine)) {
          const lines = prepared.match(/[^\n]*\n|[^\n]+$/g) || [];
          const original = lines.slice(edit.startLine - 1, edit.endLine).join("");
          if (original !== edit.source) throw new Error("Footnote source changed; rebuild reviewed manifest");
          lines.splice(edit.startLine - 1, edit.endLine - edit.startLine + 1, "\n");
          prepared = lines.join("");
        }
        next(prepared);
      }).catch((error) => {
        preparationError = error; console.error(error); next(markdown);
      });
    });
    hook.doneEach(async () => {
      const version = routeVersion;
      const main = document.getElementById("main");
      if (!main) return;
      mountChrome();
      const manifest = await manifestPromise;
      if (version !== routeVersion) return;
      if (preparationError) throw preparationError;
      currentPage = routePage(vm, manifest);
      if (currentPage) { preferences.lastRoute = currentPage.route; persist(); }
      updateSidebar();
      currentGuide = currentPage ? manifest.guides[currentPage.id] : null;
      cleanTitle(main);
      reviewedContent(main, currentPage);
      classifyCaptions(main);
      classifyProse(main, currentPage);
      hideRepeatedCode(main);
      highlightOriginals(main);
      await applyCodeVariants(main, currentPage, version);
      if (version !== routeVersion) return;
      if (currentGuide) await insertGuide(main, currentGuide, version);
      for (const guide of currentPage?.sectionGuides || []) {
        if (version !== routeVersion) return;
        await insertGuide(main, guide, version);
      }
      if (version !== routeVersion) return;
      buildToc(main); footer(main, manifest, currentPage);
      applyPreferences();
      document.title = (currentPage?.title || "谷歌的软件工程") + " · Software Engineering at Google";
      main.dataset.readerReady = "true";
      if (matchMedia("(max-width: 900px)").matches) document.body.classList.remove("close");
      menuState(); updateScroll();
    });
  });
})();
