document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!confirm("Voulez-vous vraiment supprimer ce post ?")) {
        e.preventDefault()
      }
    })
  })
})
