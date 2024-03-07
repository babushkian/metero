const ed = document.querySelector(".table");
ed.addEventListener("click", (e) => {
    t = e.target;
    if (t.closest(".del-rec")) {
        const date = t.closest("tr").firstElementChild.innerText;
        if (!confirm(`Внимение! Запись от ${date} будет удалена!`)) {
            e.preventDefault();
        }
    }
});
