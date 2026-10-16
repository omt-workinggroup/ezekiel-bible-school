const menuBtn = document.querySelector(".menu-btn");
const nav = document.getElementById("nav");

function setMenu(open) {
  menuBtn.setAttribute("aria-expanded", String(open));
  menuBtn.textContent = open ? "Close" : "Menu";
  nav.classList.toggle("is-open", open);
}

menuBtn.addEventListener("click", () => {
  setMenu(menuBtn.getAttribute("aria-expanded") !== "true");
});

nav.addEventListener("click", (e) => {
  if (e.target.closest("a")) setMenu(false);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && nav.classList.contains("is-open")) {
    setMenu(false);
    menuBtn.focus();
  }
});

// Programme filter
const filterBtns = document.querySelectorAll(".filter__btn");
const rows = document.querySelectorAll(".programmes tbody tr");

filterBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const mode = btn.dataset.mode;
    filterBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    rows.forEach((row) => {
      row.hidden = mode !== "all" && !row.dataset.modes.split(" ").includes(mode);
    });
  });
});

// Enquiry form
// No backend yet. Swap the handler for a fetch() to Formspree or an API route.
const form = document.getElementById("enquiry-form");
const status = form.querySelector(".form__status");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const invalid = [...form.querySelectorAll("[required]")].filter((field) => {
    const bad = !field.value.trim() || !field.checkValidity();
    field.setAttribute("aria-invalid", String(bad));
    return bad;
  });

  if (invalid.length) {
    status.className = "form__status is-error";
    status.textContent = "Please check the highlighted fields.";
    invalid[0].focus();
    return;
  }

  const firstName = form.elements.name.value.trim().split(/\s+/)[0];
  status.className = "form__status is-sent";
  status.textContent = `Thanks, ${firstName}. We'll be in touch within two working days.`;
  form.reset();
});

form.addEventListener("input", (e) => {
  if (e.target.getAttribute("aria-invalid") === "true") {
    e.target.removeAttribute("aria-invalid");
  }
});

document.querySelector("[data-year]").textContent = new Date().getFullYear();
