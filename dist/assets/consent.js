// Cookie banner and consent-gated Google Analytics 4.
// Nothing is sent to Google until the visitor clicks "Accept". The choice is kept in
// localStorage (not a cookie). "Cookie settings" buttons ([data-cookie-settings]) reopen
// the banner; declining after accepting removes the Analytics cookies and reloads the page.
(() => {
  const MEASUREMENT_ID = "G-BN36B66LGS";
  const STORAGE_KEY = "mr-consent";
  const POLICY_URL = "/privacy.html#analytics";

  const readChoice = () => {
    try {
      const value = window.localStorage.getItem(STORAGE_KEY);
      return value === "granted" || value === "denied" ? value : null;
    } catch {
      return null;
    }
  };

  const saveChoice = (value) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch {
      // Storage unavailable: the choice applies to this page view only.
    }
  };

  let analyticsLoaded = false;

  const loadAnalytics = () => {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() {
      window.dataLayer.push(arguments);
    };
    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    window.gtag("js", new Date());
    window.gtag("config", MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
    document.head.appendChild(script);
  };

  const removeAnalyticsCookies = () => {
    const names = document.cookie
      .split(";")
      .map((part) => part.split("=")[0].trim())
      .filter((name) => name === "_ga" || name.startsWith("_ga_"));
    const host = window.location.hostname;
    const domains = ["", host, `.${host}`, `.${host.split(".").slice(-2).join(".")}`];
    for (const name of names) {
      for (const domain of domains) {
        const domainPart = domain ? `; domain=${domain}` : "";
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/${domainPart}`;
      }
    }
  };

  let banner = null;

  const closeBanner = () => {
    if (!banner) return;
    banner.remove();
    banner = null;
  };

  const decide = (value) => {
    const previous = readChoice();
    saveChoice(value);
    closeBanner();
    if (value === "granted") {
      loadAnalytics();
    } else if (previous === "granted" || analyticsLoaded) {
      removeAnalyticsCookies();
      window.location.reload();
    }
  };

  const openBanner = (focus) => {
    if (banner) {
      if (focus) banner.querySelector("button").focus();
      return;
    }
    banner = document.createElement("section");
    banner.className = "consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Cookie preferences");
    banner.innerHTML = `
      <p class="consent-eyebrow"><span class="status-light" aria-hidden="true"></span>Cookies / Analytics</p>
      <p class="consent-text">We would like to use Google Analytics cookies to count visits and see which pages are read. Nothing is sent until you accept. You can change your mind at any time under “Cookie settings”. <a href="${POLICY_URL}">Read the details</a>.</p>
      <div class="consent-actions">
        <button type="button" class="consent-button" data-consent="denied">Decline</button>
        <button type="button" class="consent-button" data-consent="granted">Accept</button>
      </div>`;
    banner.addEventListener("click", (event) => {
      const button = event.target.closest("[data-consent]");
      if (button) decide(button.dataset.consent);
    });
    document.body.appendChild(banner);
    if (focus) banner.querySelector("button").focus();
  };

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-cookie-settings]")) openBanner(true);
  });

  const start = () => {
    const choice = readChoice();
    if (choice === "granted") loadAnalytics();
    else if (choice === null) openBanner(false);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
