export const handleCopyMarkdown = async (html, isAiMessage = false) => {
  if (!isAiMessage) {
    return navigator.clipboard.writeText(html);
  }

  const div = document.createElement("div");
  div.innerHTML = html;

  const clean = (str) =>
    str
      .replace(/\n{3,}/g, "\n\n")
      .replace(/[ \t]+\n/g, "\n")
      .trim();

  const convertNode = (node) => {
    let md = "";

    for (let child of node.childNodes) {
      if (child.nodeType === 3) {
        md += child.textContent.replace(/\s+/g, " ");
      } else if (child.nodeType === 1) {
        const tag = child.tagName.toLowerCase();

        switch (tag) {
          case "h1":
            md += `# ${clean(child.innerText)}\n\n`;
            break;

          case "h2":
            md += `## ${clean(child.innerText)}\n\n`;
            break;

          case "h3":
            md += `### ${clean(child.innerText)}\n\n`;
            break;

          case "h4":
            md += `#### ${clean(child.innerText)}\n\n`;
            break;

          case "p":
            md += `${clean(child.innerText)}\n\n`;
            break;

          case "strong":
          case "b":
            md += `**${clean(child.innerText)}**`;
            break;

          case "ul": {
            const items = child.querySelectorAll(":scope > li");
            items.forEach((li) => {
              md += `- ${clean(li.innerText)}\n`;
            });
            md += `\n`;
            break;
          }

          case "ol": {
            const items = child.querySelectorAll(":scope > li");
            items.forEach((li, index) => {
              md += `${index + 1}. ${clean(li.innerText)}\n`;
            });
            md += `\n`;
            break;
          }

          case "li":
            md += `- ${clean(child.innerText)}\n`;
            break;

          case "br":
            md += `\n`;
            break;

          case "hr":
            md += `---\n\n`;
            break;

          case "table": {
            const rows = child.querySelectorAll("tr");
            rows.forEach((row, rowIndex) => {
              const cells = Array.from(row.children).map((c) =>
                clean(c.innerText)
              );
              md += `| ${cells.join(" | ")} |\n`;
              if (rowIndex === 0) {
                md += `| ${cells.map(() => "---").join(" | ")} |\n`;
              }
            });
            md += "\n";
            break;
          }

          default:
            md += convertNode(child);
            break;
        }
      }
    }

    return md;
  };

  let md = clean(convertNode(div));

  md = clean(
    md
      .replace(/\n[ \t]+-/g, "\n-")
      .replace(/\n[ \t]+#/g, "\n#")
      .replace(/[ \t]+\*/g, "*")
      .replace(/\n{3,}/g, "\n\n")
  );

  try {
    await navigator.clipboard.writeText(md);
  } catch (e) {
     console.error("An error occurred:", e);
    const ta = document.createElement("textarea");
    ta.value = md;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
};