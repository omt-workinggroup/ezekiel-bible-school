const root = document.documentElement;
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

// Header shadow
const onScroll = () => root.classList.toggle("is-scrolled", scrollY > 8);
addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Reveal sections as they scroll in. Only elements that start below the fold
// are hidden, so nothing visible on load flickers.
if ("IntersectionObserver" in window && !reduceMotion) {
  const targets = document.querySelectorAll(
    ".section-head, .tile, .feature > *, .columns > *, .location__grid > *, .prose-split > *, " +
      ".people li, .amenities li, .events li, .steps li, .programmes, .timetable, .cta__inner"
  );
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -10% 0px" }
  );

  root.classList.add("js");
  targets.forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight) return;
    const siblings = [...el.parentElement.children].filter((c) => c.matches(el.tagName));
    el.style.transitionDelay = `${Math.min(siblings.indexOf(el), 4) * 70}ms`;
    el.classList.add("reveal");
    io.observe(el);
  });
}

// Mobile menu
const burger = document.querySelector(".burger");
const menu = document.getElementById("menu");
const header = document.querySelector(".header");
const label = burger.querySelector(".burger__label");
const desktop = window.matchMedia("(min-width: 64em)");
const outside = document.querySelectorAll("main, .footer, .notice");

function openMenu() {
  menu.style.setProperty("--menu-top", `${header.getBoundingClientRect().bottom}px`);
  root.classList.add("menu-open");
  burger.setAttribute("aria-expanded", "true");
  label.textContent = "Close";
  outside.forEach((el) => (el.inert = true));
  menu.querySelector("a").focus({ preventScroll: true });
}

function closeMenu({ restoreFocus = true } = {}) {
  if (!root.classList.contains("menu-open")) return;
  root.classList.remove("menu-open");
  burger.setAttribute("aria-expanded", "false");
  label.textContent = "Menu";
  outside.forEach((el) => (el.inert = false));
  if (restoreFocus) burger.focus({ preventScroll: true });
}

burger.addEventListener("click", () => {
  root.classList.contains("menu-open") ? closeMenu() : openMenu();
});

menu.addEventListener("click", (e) => {
  if (e.target.closest("a")) closeMenu({ restoreFocus: false });
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeMenu();
});

desktop.addEventListener("change", (e) => {
  if (e.matches) closeMenu({ restoreFocus: false });
});

// Hero slideshow
const slides = document.querySelectorAll(".hero__slide");

if (slides.length > 1 && !reduceMotion) {
  let current = 0;
  setInterval(() => {
    slides[current].classList.remove("is-active");
    current = (current + 1) % slides.length;
    slides[current].classList.add("is-active");
  }, 7000);
}

// Student stories
const voices = document.querySelector(".voices__slides")?.closest(".voices");

if (voices) {
  const slides = voices.querySelectorAll(".voices__slide");
  const current = voices.querySelector("[data-current]");
  const bar = voices.querySelector(".voices__progress span");
  let index = 0;
  let timer;

  const show = (next) => {
    slides[index].classList.remove("is-active");
    slides[index].hidden = true;
    index = (next + slides.length) % slides.length;
    slides[index].hidden = false;
    slides[index].classList.add("is-active");
    current.textContent = String(index + 1).padStart(2, "0");
  };

  const restart = () => {
    clearTimeout(timer);
    bar.classList.remove("is-running");
    if (reduceMotion) return;
    void bar.offsetWidth;
    bar.classList.add("is-running");
    timer = setTimeout(() => { show(index + 1); restart(); }, 8000);
  };

  voices.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-dir]");
    if (!btn) return;
    show(index + Number(btn.dataset.dir));
    restart();
  });

  let startX = null;
  voices.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
  voices.addEventListener("touchend", (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) { show(index + (dx < 0 ? 1 : -1)); restart(); }
    startX = null;
  });

  restart();
}

// Count up the numbers strip when it comes into view
const counters = document.querySelectorAll("[data-count]");

if (counters.length && "IntersectionObserver" in window && !reduceMotion) {
  const fmt = new Intl.NumberFormat("en-GB");
  const run = (el) => {
    const target = Number(el.dataset.count);
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min((now - start) / 1600, 1);
      el.textContent = fmt.format(Math.round(target * (1 - Math.pow(1 - t, 4))));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const co = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { run(entry.target); co.unobserve(entry.target); }
    });
  }, { threshold: 0.6 });
  counters.forEach((el) => co.observe(el));
}

// Programme filter
const filter = document.querySelector(".filter");

if (filter) {
  const buttons = filter.querySelectorAll("button");
  const rows = document.querySelectorAll(".programmes tbody tr");

  filter.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const { group } = btn.dataset;
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    rows.forEach((row) => {
      row.hidden = group !== "all" && row.dataset.group !== group;
    });
  });
}

// Curriculum: highlight the level in view
const levelNav = document.querySelector(".curriculum__nav");

if (levelNav && "IntersectionObserver" in window) {
  const links = new Map([...levelNav.querySelectorAll("a")].map((a) => [a.hash.slice(1), a]));
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((a) => a.removeAttribute("aria-current"));
      links.get(entry.target.id)?.setAttribute("aria-current", "true");
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  document.querySelectorAll(".level").forEach((el) => spy.observe(el));
}

// Enquiry form
// TODO: post to Formspree or /api/enquiry once the admissions inbox is set up.
const form = document.getElementById("enquiry-form");

if (form) {
  const status = form.querySelector(".form__status");
  const programme = new URLSearchParams(location.search).get("programme");
  if (programme) form.elements.programme.value = programme;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const invalid = [...form.querySelectorAll("[required]")].filter((field) => {
      const bad = !field.value.trim() || !field.checkValidity();
      field.setAttribute("aria-invalid", String(bad));
      return bad;
    });

    if (invalid.length) {
      status.className = "form__status is-error";
      status.textContent = "Please complete the highlighted fields.";
      invalid[0].focus();
      return;
    }

    const name = form.elements.name.value.trim().split(/\s+/)[0];
    status.className = "form__status is-sent";
    status.textContent = `Thank you, ${name}. We'll reply within two working days.`;
    form.reset();
  });

  form.addEventListener("input", (e) => e.target.removeAttribute("aria-invalid"));
}

document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});
