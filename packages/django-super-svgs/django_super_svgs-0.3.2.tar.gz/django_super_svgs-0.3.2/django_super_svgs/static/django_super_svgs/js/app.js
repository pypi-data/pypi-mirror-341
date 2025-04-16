(function (root, factory) {
  if (typeof define === "function" && define.amd) {
    define([], factory);
  } else if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.app = root.app || factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  return (function () {
    "use strict";

    var app = {
      version: "0.1.0",
      copysvg: copySvg,
      activeaside: activeAside,
      deactivateaside: deactivateAside,
      scrolltotop: scrollToTop,
      toggletheme: toggleTheme,
    };

    //====================================================================
    // Utilities
    //====================================================================
    function scrollToTop(event) {
      const container = document.querySelector("body .svg-deck");
      container.scrollTo({ top: 0, behavior: "smooth" });
    }

    function asideActive() {
      const aside = document.querySelector(".aside");
      if (aside) {
        aside.classList.add("active");
      }
    }

    function asideDeactivate() {
      const aside = document.querySelector(".aside");
      if (aside) {
        aside.classList.remove("active");
      }
    }

    function toggleTheme() {
      const ts = document.querySelector(".theme-swticher");
      const newtheme = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = newtheme;

      if (ts) {
        ts.classList.toggle("rotated");
      }

      localStorage.setItem("django_super_svgs_theme", newtheme);
    }

    //==========================================================================================
    // public API
    //==========================================================================================
    function copySvg(el) {
      if (!el) {
        return;
      }
      const style = window.getComputedStyle(el, null);
      const text = el.querySelector(".svg-name");
      const default_text = text.innerText;
      const svg_type = el.getAttribute("data-type");

      navigator.clipboard.writeText(
        "{% svg " + svg_type + " " + default_text + " %}",
      );
      el.classList.add("selected");

      setTimeout(() => {
        el.classList.remove("selected");
        text.innerText = default_text;
      }, 500);
    }

    function activeAside() {
      asideActive();
    }

    function deactivateAside() {
      asideDeactivate();
    }

    //====================================================================
    // Initialization
    //====================================================================
    var isReady = false;
    document.addEventListener("DOMContentLoaded", function () {
      isReady = true;
    });

    function ready(fn) {
      if (isReady || document.readyState === "complete") {
        fn();
      } else {
        document.addEventListener("DOMContentLoaded", fn);
      }
    }

    // initialize the document
    ready(function () {
      var body = document.body;
      const container = document.querySelector("body .svg-deck");
      const scroll_btn = document.querySelector(".scroll-to-top");

      if (container) {
        container.onscroll = (e) => {
          if (container.scrollTop >= 50) {
            scroll_btn.classList.add("active");
          } else {
            scroll_btn.classList.remove("active");
          }
        };
      }

      setTimeout(function () {
        body.dispatchEvent(new Event("app:load", { bubbles: true }));
        body = null;
      }, 0);
    });

    return app;
  })();
});
