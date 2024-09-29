// Función para mostrar una sección y ocultar las demás
function showSection(section) {
  // Oculta todas las secciones con una transición de opacidad
  document.querySelectorAll("section").forEach((sec) => {
    if (sec.id !== section + "-section") {
      sec.style.opacity = 0;
      sec.style.pointerEvents = "none";
    }
  });

  setTimeout(() => {
    document.querySelectorAll("section").forEach((sec) => {
      if (sec.id !== section + "-section") {
        sec.style.display = "none";
      }
    });

    const newSection = document.getElementById(section + "-section");
    newSection.style.display = "block";
    newSection.style.pointerEvents = "auto";

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        newSection.style.opacity = 1;
      });
    });
  }, 300);

  document.querySelectorAll(".navbar-right a").forEach((link) => {
    link.classList.toggle(
      "selected",
      link.getAttribute("onclick") === `showSection('${section}')`
    );
  });
}

// Función para cargar la sección principal por defecto
document.addEventListener("DOMContentLoaded", () => {
  const mainSection = document.getElementById("main-section");
  mainSection.style.display = "block";
  mainSection.style.opacity = 1;
  document
    .querySelector(`.navbar-right a[onclick="showSection('main')]`)
    .classList.add("selected");
});

// Función para establecer el tema
function applyDarkThemeToAudio() {
  const audioPlayer = document.querySelector(".audio-player");
  audioPlayer.style.backgroundColor = "#333";

  audioPlayer.style.color = "#000";
  audioPlayer.style.border = "1px solid #222";
  audioPlayer.style.borderRadius = "8px";
  audioPlayer.style.padding = "10px";
}

// Función para aplicar el tema claro al reproductor de audio
function applyLightThemeToAudio() {
  const audioPlayer = document.querySelector(".audio-player");
  audioPlayer.style.backgroundColor = "#f0f0f0";
  audioPlayer.style.color = "#000000";
  audioPlayer.style.border = "1px solid #aaa";
  audioPlayer.style.borderRadius = "8px";
  audioPlayer.style.padding = "10px";
}

// Función para establecer el tema en general y también cambiar el tema del reproductor de audio
function setTheme(theme) {
  const themeToggle = document.getElementById("theme-toggle");
  const icon = themeToggle.querySelector("i");

  if (theme === "light") {
    document.body.classList.add("light-theme");
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
    applyLightThemeToAudio();
  } else {
    document.body.classList.remove("light-theme");
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
    applyDarkThemeToAudio();
  }
  localStorage.setItem("theme", theme);
}

// Cargar el tema al iniciar la página
const savedTheme = localStorage.getItem("theme") || "dark";
setTheme(savedTheme);

// Cambiar el tema al hacer clic en el botón
document.getElementById("theme-toggle").addEventListener("click", () => {
  const newTheme = document.body.classList.contains("light-theme")
    ? "dark"
    : "light";
  setTheme(newTheme);
});
