const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.querySelector("#sidebar");
const main = document.querySelector(".main");

hamBurger.addEventListener("click", function () {
    sidebar.classList.toggle("expand");
    main.style.marginLeft = sidebar.classList.contains("expand") ? "260px" : "70px";
});
