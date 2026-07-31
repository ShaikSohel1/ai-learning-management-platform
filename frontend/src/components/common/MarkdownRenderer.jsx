import React, { useState } from "react";
import { Copy, Check, Terminal } from "lucide-react";

export function MarkdownRenderer({ content = "" }) {
  const [copiedCode, setCopiedCode] = useState(null);

  if (!content) return null;

  const handleCopy = (codeText, index) => {
    navigator.clipboard.writeText(codeText);
    setCopiedCode(index);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  // Simple, safe Markdown Parser for AI Responses (Handles Code Blocks, Bold, Lists, Headers, Quotes)
  const parseMarkdown = (text) => {
    // Split by code blocks ```
    const codeBlockRegex = /```([a-zA-Z0-9]*)\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;
    let blockCount = 0;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Text before code block
      if (match.index > lastIndex) {
        parts.push({
          type: "text",
          content: text.substring(lastIndex, match.index),
        });
      }

      // Code block
      parts.push({
        type: "code",
        language: match[1] || "code",
        code: match[2].trim(),
        id: blockCount++,
      });

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < text.length) {
      parts.push({
        type: "text",
        content: text.substring(lastIndex),
      });
    }

    return parts;
  };

  const renderFormattedText = (rawText) => {
    const lines = rawText.split("\n");
    return lines.map((line, lineIdx) => {
      if (!line.trim()) return <div key={lineIdx} style={{ height: "8px" }} />;

      // Header 3 or 2
      if (line.startsWith("### ")) {
        return (
          <h4 key={lineIdx} style={{ fontSize: "1.05rem", fontWeight: 700, margin: "14px 0 6px 0", color: "var(--text-primary)" }}>
            {formatInline(line.replace("### ", ""))}
          </h4>
        );
      }
      if (line.startsWith("## ")) {
        return (
          <h3 key={lineIdx} style={{ fontSize: "1.2rem", fontWeight: 800, margin: "16px 0 8px 0", color: "var(--text-primary)" }}>
            {formatInline(line.replace("## ", ""))}
          </h3>
        );
      }

      // Bullet lists
      if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
        return (
          <li key={lineIdx} style={{ marginLeft: "18px", marginBottom: "4px", color: "var(--text-primary)" }}>
            {formatInline(line.trim().substring(2))}
          </li>
        );
      }

      // Numbered list
      if (/^\d+\.\s/.test(line.trim())) {
        const itemText = line.trim().replace(/^\d+\.\s/, "");
        return (
          <li key={lineIdx} style={{ marginLeft: "18px", marginBottom: "4px", color: "var(--text-primary)", listStyleType: "decimal" }}>
            {formatInline(itemText)}
          </li>
        );
      }

      return (
        <p key={lineIdx} style={{ marginBottom: "8px", lineHeight: 1.6, color: "var(--text-primary)" }}>
          {formatInline(line)}
        </p>
      );
    });
  };

  const formatInline = (str) => {
    // Replace **bold** with <strong> and `code` with inline badge
    const elements = [];
    const inlineRegex = /(\*\*.*?\*\*|`.*?`)/g;
    let last = 0;
    let m;

    while ((m = inlineRegex.exec(str)) !== null) {
      if (m.index > last) {
        elements.push(str.substring(last, m.index));
      }
      const matchStr = m[0];
      if (matchStr.startsWith("**") && matchStr.endsWith("**")) {
        elements.push(
          <strong key={m.index} style={{ fontWeight: 700, color: "var(--text-primary)" }}>
            {matchStr.slice(2, -2)}
          </strong>
        );
      } else if (matchStr.startsWith("`") && matchStr.endsWith("`")) {
        elements.push(
          <code
            key={m.index}
            style={{
              background: "var(--color-primary-light)",
              color: "var(--color-primary)",
              padding: "2px 6px",
              borderRadius: "4px",
              fontSize: "0.85rem",
              fontFamily: "var(--font-mono)",
            }}
          >
            {matchStr.slice(1, -1)}
          </code>
        );
      }
      last = m.index + matchStr.length;
    }

    if (last < str.length) {
      elements.push(str.substring(last));
    }

    return elements.length > 0 ? elements : str;
  };

  const blocks = parseMarkdown(content);

  return (
    <div className="markdown-body" style={{ fontSize: "0.94rem", lineHeight: 1.6 }}>
      {blocks.map((block, idx) => {
        if (block.type === "text") {
          return <React.Fragment key={idx}>{renderFormattedText(block.content)}</React.Fragment>;
        }

        if (block.type === "code") {
          return (
            <div
              key={idx}
              style={{
                margin: "14px 0",
                borderRadius: "var(--radius-md)",
                overflow: "hidden",
                border: "1px solid var(--border-color)",
                background: "#0c0c0e",
              }}
            >
              {/* Header Bar */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "8px 14px",
                  background: "rgba(255,255,255,0.04)",
                  borderBottom: "1px solid rgba(255,255,255,0.06)",
                  fontSize: "0.78rem",
                  color: "#a1a1aa",
                  fontFamily: "var(--font-mono)",
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <Terminal size={13} color="var(--color-primary)" />
                  {block.language || "code"}
                </span>

                <button
                  onClick={() => handleCopy(block.code, block.id)}
                  style={{
                    background: "transparent",
                    border: "none",
                    color: copiedCode === block.id ? "var(--color-success)" : "#a1a1aa",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                    fontSize: "0.76rem",
                    fontWeight: 600,
                  }}
                >
                  {copiedCode === block.id ? <Check size={13} /> : <Copy size={13} />}
                  {copiedCode === block.id ? "Copied!" : "Copy"}
                </button>
              </div>

              {/* Code Snippet Box */}
              <pre
                style={{
                  padding: "14px 16px",
                  margin: 0,
                  overflowX: "auto",
                  color: "#f4f4f5",
                  fontSize: "0.85rem",
                  fontFamily: "var(--font-mono)",
                  lineHeight: 1.5,
                }}
              >
                <code>{block.code}</code>
              </pre>
            </div>
          );
        }

        return null;
      })}
    </div>
  );
}

export default MarkdownRenderer;
