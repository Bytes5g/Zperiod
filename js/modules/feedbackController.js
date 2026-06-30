const LOCAL_SUGGESTIONS_KEY = "zperiod_local_suggestions";

export const SUCCESS_ICON_SVG =
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';

export async function submitSuggestion(text, options = {}) {
  const trimmed = text?.trim();
  if (!trimmed) return false;

  const { source = "Zperiod" } = options;
  const sourceLabel = source ? ` from ${source}` : "";

  try {
    const existing = JSON.parse(localStorage.getItem(LOCAL_SUGGESTIONS_KEY) || "[]");
    existing.push({
      text: trimmed,
      source: source || "Zperiod",
      createdAt: new Date().toISOString(),
      preview: `📬 New Suggestion${sourceLabel}: ${trimmed}`,
    });
    localStorage.setItem(LOCAL_SUGGESTIONS_KEY, JSON.stringify(existing));
    return true;
  } catch {
    return false;
  }
}

export function flashSentState(button, options = {}) {
  if (!button) return;

  const {
    successClass = "sent",
    duration = 1000,
    originalHTML,
    successHTML,
    onReset,
  } = options;

  button.classList.add(successClass);
  if (successHTML) {
    button.innerHTML = successHTML;
  }

  window.setTimeout(() => {
    button.classList.remove(successClass);
    if (originalHTML) {
      button.innerHTML = originalHTML;
    }
    if (typeof onReset === "function") onReset();
  }, duration);
}
