// Contact buttons: the support address is never in the page source as text.
// It is rebuilt from character codes only when a visitor clicks a [data-contact] button,
// then opened as a mailto: link with an optional subject (data-subject).
(() => {
  const ADDRESS_CODES = [115, 117, 112, 112, 111, 114, 116, 64, 109, 97, 115, 115, 114, 101, 97, 99, 116, 105, 111, 110, 46, 97, 112, 112];

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-contact]");
    if (!button) return;
    const address = String.fromCharCode(...ADDRESS_CODES);
    const subject = button.dataset.subject;
    window.location.href = subject
      ? `mailto:${address}?subject=${encodeURIComponent(subject)}`
      : `mailto:${address}`;
  });
})();
