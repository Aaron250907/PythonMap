/* ==========================================================
   Smooth Scroll
========================================================== */
function smoothScrollTo(selector) {
    const el = document.querySelector(selector);
    if (!el) return;

    const headerOffset = 70;
    const top = el.getBoundingClientRect().top + window.scrollY - headerOffset;

    window.scrollTo({
        top: top,
        behavior: "smooth"
    });
}

/* ==========================================================
   MAIN SCRIPT
========================================================== */
document.addEventListener("DOMContentLoaded", () => {

    /* =============================
       NAV SMOOTH SCROLL
    ============================== */
    const navLinks = document.querySelectorAll(".main-nav a");
    const nav = document.querySelector(".main-nav");
    const navToggle = document.querySelector(".nav-toggle");

    navLinks.forEach(link => {
        link.addEventListener("click", e => {
            e.preventDefault();
            const target = link.getAttribute("href");
            smoothScrollTo(target);
            nav.classList.remove("open");
        });
    });

    if (navToggle) {
        navToggle.addEventListener("click", () => {
            nav.classList.toggle("open");
        });
    }

    /* =============================
       SCROLL ANIMATIONS
    ============================== */
    const animated = document.querySelectorAll(".animate-on-scroll");
    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    animated.forEach(el => observer.observe(el));

    /* =============================
       INTERACTIVE MAP POPUP
    ============================== */
    const popup = document.getElementById("country-popup");
    const popupTitle = document.getElementById("popup-title");
    const popupScore = document.getElementById("popup-score");
    const popupButton = document.getElementById("popup-button");

    const countryData = {
        portugal: { name: "Portugal", score: "CPI Score: ~63", target: "#portugal" },
        india: { name: "India", score: "CPI Score: ~39", target: "#india" },
        pakistan: { name: "Pakistan", score: "CPI Score: ~28", target: "#pakistan" }
    };

    const markers = document.querySelectorAll(".svg-marker");

    markers.forEach(marker => {
        marker.addEventListener("click", e => {
            e.stopPropagation();

            const key = marker.dataset.country;
            const info = countryData[key];
            if (!info) return;

            // Fill popup content
            popupTitle.textContent = info.name;
            popupScore.textContent = info.score;

            // Position popup next to marker (account for scroll)
            const rect = marker.getBoundingClientRect();
            popup.style.left = rect.left + window.scrollX + 40 + "px";
            popup.style.top = rect.top + window.scrollY + "px";
            popup.style.display = "block";

            popupButton.onclick = () => {
                smoothScrollTo(info.target);
            };
        });
    });

    // Close popup if clicked outside
    document.addEventListener("click", e => {
        if (!e.target.closest("#country-popup") &&
            !e.target.closest(".svg-marker")) {
            popup.style.display = "none";
        }
    });
});
