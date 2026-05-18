document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("cookie-consent-banner");
  const modal = document.getElementById("cookie-consent-modal");
  const acceptButton = document.getElementById("cookie-consent-accept");
  const essentialButton = document.getElementById("cookie-consent-essential");
  const settingsButton = document.getElementById("cookie-consent-settings");
  const closeButton = document.getElementById("cookie-consent-close");
  const acceptModalButton = document.getElementById("cookie-consent-accept-modal");
  const essentialModalButton = document.getElementById("cookie-consent-essential-modal");
  const consentCookieName = "edw_cookie_consent";

  function hasAcceptedCookies() {
    return document.cookie
      .split(";")
      .map((part) => part.trim())
      .some((part) => part.startsWith(`${consentCookieName}=`));
  }

  function getConsentCookie() {
    const match = document.cookie
      .split(";")
      .map((part) => part.trim())
      .find((part) => part.startsWith(`${consentCookieName}=`));
    return match ? match.split("=")[1] : "";
  }

  function setConsentCookie(value) {
    const maxAge = 60 * 60 * 24 * 365;
    document.cookie = `${consentCookieName}=${value}; Path=/; Max-Age=${maxAge}; SameSite=Lax`;
  }

  function showModal() {
    if (!modal) {
      return;
    }
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("overflow-hidden");
  }

  function hideModal() {
    if (!modal) {
      return;
    }
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("overflow-hidden");
  }

  function hideBanner() {
    if (banner) {
      banner.classList.add("hidden");
    }
  }

  function finalizeConsent(value) {
    setConsentCookie(value);
    hideBanner();
    hideModal();
  }

  if (!banner) {
    return;
  }

  if (hasAcceptedCookies()) {
    hideBanner();
    hideModal();
    return;
  }

  banner.classList.remove("hidden");

  if (acceptButton) {
    acceptButton.addEventListener("click", function () {
      finalizeConsent("accepted");
    });
  }

  if (essentialButton) {
    essentialButton.addEventListener("click", function () {
      finalizeConsent("essential_only");
    });
  }

  if (settingsButton) {
    settingsButton.addEventListener("click", function () {
      showModal();
    });
  }

  if (closeButton) {
    closeButton.addEventListener("click", function () {
      hideModal();
    });
  }

  if (acceptModalButton) {
    acceptModalButton.addEventListener("click", function () {
      finalizeConsent("accepted");
    });
  }

  if (essentialModalButton) {
    essentialModalButton.addEventListener("click", function () {
      finalizeConsent("essential_only");
    });
  }

  if (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        hideModal();
      }
    });
  }

  const cookieSettingsLinks = document.querySelectorAll("[data-cookie-settings]");
  cookieSettingsLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      if (!hasAcceptedCookies() && !getConsentCookie()) {
        banner.classList.remove("hidden");
      }
      showModal();
    });
  });
});
