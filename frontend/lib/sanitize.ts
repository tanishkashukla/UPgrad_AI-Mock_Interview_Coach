/** Never show raw strategist JSON in the chat UI */
export function isJsonLike(text: string): boolean {
  const t = text?.trim() ?? "";
  return t.startsWith("{") && t.includes("competencies_to_assess");
}

export function normalizeQuestion(text: string, role?: string): string {
  const t = (text ?? "").trim();
  if (!t || isJsonLike(t)) {
    return (
      "Thanks for joining today. To start — what draws you to this role, " +
      "and what would success look like in your first six months?"
    );
  }
  return t;
}
