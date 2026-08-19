/* Karakaş Hukuk Bürosu — behaviour only.
   Anything visual lives in styles.css; this file never injects styles. */
(function () {
  "use strict";

  /* ============================================================== config ==
     FORM_ACCESS_KEY: iletişim formunun gönderim anahtarı.

     Form web3forms.com üzerinden çalışır — sunucu gerektirmez, ücretsiz
     katmanı bu site için fazlasıyla yeterlidir. Kurulum:
       1. https://web3forms.com adresine avpinarkarakas@gmail.com ile kaydolun.
       2. E-posta ile gelen Access Key'i aşağıya yapıştırın.
     Anahtar girilene kadar form gönderilmez; ziyaretçiye e-posta ile yazması
     için hazır bir bağlantı sunulur, yani hiçbir talep kaybolmaz.
     ====================================================================== */
  var FORM_ACCESS_KEY = "BURAYA_WEB3FORMS_ACCESS_KEY";
  var FORM_ENDPOINT = "https://api.web3forms.com/submit";
  var CONTACT_EMAIL = "avpinarkarakas@gmail.com";

  var lang = document.documentElement.lang === "en" ? "en" : "tr";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var TXT = {
    tr: {
      required: "Lütfen zorunlu alanları doldurun.",
      email: "Lütfen geçerli bir e-posta adresi girin.",
      consent: "Devam etmek için aydınlatma metnini onaylamanız gerekiyor.",
      busy: "Gönderiliyor…",
      ok: "Mesajınız iletildi. En kısa sürede dönüş yapılacaktır.",
      error: "Mesaj gönderilemedi. Lütfen doğrudan e-posta ile yazın:",
      unconfigured: "Form servisi henüz bağlanmadı. Mesajınızı e-posta ile gönderin:",
      mailLabel: "E-posta ile gönder",
      mapLoading: "Harita yükleniyor…",
    },
    en: {
      required: "Please complete the required fields.",
      email: "Please enter a valid email address.",
      consent: "Please accept the privacy notice to continue.",
      busy: "Sending…",
      ok: "Your message has been sent. We will get back to you shortly.",
      error: "The message could not be sent. Please email us directly:",
      unconfigured: "The form service is not connected yet. Please email us:",
      mailLabel: "Send by email",
      mapLoading: "Loading map…",
    },
  }[lang];

  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");

  /* ------------------------------------------------ header scroll state -- */

  if (header) {
    var stuck = false;
    var hidden = false;
    var lastY = window.scrollY;
    var ghost = document.querySelector(".hero__ghost");
    var ticking = false;

    var syncHeader = function () {
      var y = window.scrollY;

      var nextStuck = y > 24;
      if (nextStuck !== stuck) {
        stuck = nextStuck;
        header.classList.toggle("is-stuck", stuck);
      }

      // Retreat on the way down, return on the way up — but never while the
      // mobile menu is open, and never over the hero.
      if (!reduceMotion) {
        var menuOpen = nav && nav.classList.contains("is-open");
        var nextHidden = !menuOpen && y > 320 && y > lastY + 4;
        if (y < lastY - 4 || menuOpen) nextHidden = false;
        if (nextHidden !== hidden) {
          hidden = nextHidden;
          header.classList.toggle("is-hidden", hidden);
        }

        // The monogram drifts at a fraction of the scroll rate.
        if (ghost && y < window.innerHeight * 1.4) {
          ghost.style.transform = "translate3d(0," + (y * -0.08).toFixed(1) + "px,0)";
        }
      }

      lastY = y;
      ticking = false;
    };

    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(syncHeader);
    };

    syncHeader();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* -------------------------------------------------------- mobile menu -- */
  if (toggle && nav) {
    var setMenu = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute(
        "aria-label",
        open
          ? lang === "en" ? "Close menu" : "Menüyü kapat"
          : lang === "en" ? "Open menu" : "Menüyü aç"
      );
    };

    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMenu(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });

    // Leaving the mobile breakpoint must not strand the menu in a stale state.
    var wide = window.matchMedia("(min-width: 1025px)");
    var onWide = function (event) {
      if (event.matches) setMenu(false);
    };
    if (wide.addEventListener) wide.addEventListener("change", onWide);
    else wide.addListener(onWide);
  }

  /* ------------------------------------------------------ scroll reveal -- */
  Array.prototype.forEach.call(
    document.querySelectorAll(".practice__grid .card"),
    function (card, i) {
      card.style.setProperty("--stagger", String(i % 6));
    }
  );

  var animated = document.querySelectorAll(".reveal, .rise, .draw");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(animated, function (el) {
      el.classList.add("is-in");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -6% 0px" }
    );

    Array.prototype.forEach.call(animated, function (el) {
      observer.observe(el);
    });
  }

  /* --------------------------------------------------------- contact form -- */
  var form = document.querySelector("[data-form]");

  if (form) {
    var status = form.querySelector(".form__status");
    var submit = form.querySelector('button[type="submit"]');

    var say = function (state, message, mailBody) {
      status.dataset.state = state;
      status.textContent = message;
      if (mailBody) {
        status.append(" ");
        var a = document.createElement("a");
        a.href =
          "mailto:" +
          CONTACT_EMAIL +
          "?subject=" +
          encodeURIComponent(mailBody.subject) +
          "&body=" +
          encodeURIComponent(mailBody.body);
        a.textContent = CONTACT_EMAIL;
        a.style.color = "inherit";
        a.style.textDecoration = "underline";
        status.append(a);
      }
    };

    var compose = function (data) {
      var subject =
        (lang === "en" ? "Website enquiry" : "Web sitesi iletişim talebi") +
        (data.get("konu") ? " — " + data.get("konu") : "");
      var body = [
        (lang === "en" ? "Name" : "Ad Soyad") + ": " + (data.get("ad_soyad") || ""),
        (lang === "en" ? "Email" : "E-posta") + ": " + (data.get("eposta") || ""),
        (lang === "en" ? "Phone" : "Telefon") + ": " + (data.get("telefon") || "-"),
        (lang === "en" ? "Subject" : "Konu") + ": " + (data.get("konu") || "-"),
        "",
        data.get("mesaj") || "",
      ].join("\n");
      return { subject: subject, body: body };
    };

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);

      // Honeypot: only a bot fills this in.
      if (data.get("website")) return;

      var name = (data.get("ad_soyad") || "").toString().trim();
      var email = (data.get("eposta") || "").toString().trim();
      var message = (data.get("mesaj") || "").toString().trim();

      if (!name || !email || !message) {
        say("error", TXT.required);
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        say("error", TXT.email);
        return;
      }
      if (!data.get("kvkk")) {
        say("error", TXT.consent);
        return;
      }

      if (FORM_ACCESS_KEY.indexOf("BURAYA_") === 0) {
        say("error", TXT.unconfigured, compose(data));
        return;
      }

      data.append("access_key", FORM_ACCESS_KEY);
      data.append("subject", compose(data).subject);
      data.append("from_name", "karakaslawfirm.com");

      submit.disabled = true;
      say("busy", TXT.busy);

      fetch(FORM_ENDPOINT, { method: "POST", body: data })
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          if (result && result.success) {
            form.reset();
            say("ok", TXT.ok);
          } else {
            say("error", TXT.error, compose(data));
          }
        })
        .catch(function () {
          say("error", TXT.error, compose(data));
        })
        .then(function () {
          submit.disabled = false;
        });
    });
  }

  /* ------------------------------------------------------------------ map -- */
  // Google is only contacted once the visitor asks for the map.
  var map = document.querySelector("[data-map]");

  if (map && map.dataset.src) {
    var button = document.createElement("button");
    button.type = "button";
    button.textContent = map.dataset.label || "Load map";

    var note = document.createElement("small");
    note.textContent = map.dataset.note || "";

    button.addEventListener("click", function () {
      button.disabled = true;
      button.textContent = TXT.mapLoading;

      var frame = document.createElement("iframe");
      frame.src = map.dataset.src;
      frame.loading = "lazy";
      frame.title = map.dataset.label || "Map";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      frame.allowFullscreen = true;

      frame.addEventListener("load", function () {
        map.classList.remove("map--idle");
        map.textContent = "";
        frame.removeAttribute("style");
        map.appendChild(frame);
      });

      // Keep it off-layout until it has actually loaded.
      frame.style.position = "absolute";
      frame.style.opacity = "0";
      frame.style.pointerEvents = "none";
      map.appendChild(frame);
    });

    map.append(button, note);
  }

  /* --------------------------------------------------------------- misc -- */
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
