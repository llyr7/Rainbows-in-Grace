function showSection(section) {
  // Oculta todas las secciones
  document.getElementById("main-section").style.display = "none";
  document.getElementById("thoughts-section").style.display = "none";
  document.getElementById("music-section").style.display = "none";

  // Muestra la sección seleccionada
  document.getElementById(section + "-section").style.display = "block";

  // Elimina la clase 'selected' de todos los enlaces
  let navLinks = document.querySelectorAll(".navbar-right a");
  navLinks.forEach((link) => link.classList.remove("selected"));

  // Agrega la clase 'selected' al enlace correspondiente
  document
    .querySelector(`.navbar-right a[onclick="showSection('${section}')"]`)
    .classList.add("selected");
}

const themeToggle = document.getElementById("theme-toggle");

// Función para establecer el tema
function setTheme(theme) {
  const icon = themeToggle.querySelector("i");
  if (theme === "light") {
    document.body.classList.add("light-theme");
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  } else {
    document.body.classList.remove("light-theme");
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
  }
  localStorage.setItem("theme", theme);
}

// Cargar el tema al iniciar la página
const savedTheme = localStorage.getItem("theme") || "dark";
setTheme(savedTheme);

// Cambiar el tema al hacer clic en el botón
themeToggle.addEventListener("click", () => {
  const newTheme = document.body.classList.contains("light-theme")
    ? "dark"
    : "light";
  setTheme(newTheme);
});

// Marcar la página activa en el navbar
document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname.split("/").pop();
  const navLinks = document.querySelectorAll(".navbar-right a");
  navLinks.forEach((link) => {
    if (link.getAttribute("href") === path) {
      link.classList.add("active");
    }
  });
});