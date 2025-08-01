document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner les éléments nécessaires
    const burgerMenu = document.querySelector('.burger-menu');
    const mainNav = document.querySelector('.main-nav');
    
    // Ajouter l'écouteur d'événement pour le burger menu
    burgerMenu.addEventListener('click', function() {
        // Toggle les classes active
        burgerMenu.classList.toggle('active');
        mainNav.classList.toggle('active');
    });
    
    // Fermer le menu quand on clique sur un lien
    const navLinks = document.querySelectorAll('.main-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            burgerMenu.classList.remove('active');
            mainNav.classList.remove('active');
        });
    });
    
    // Fermer le menu quand on clique en dehors
    document.addEventListener('click', function(event) {
        const isClickInsideBurger = burgerMenu.contains(event.target);
        const isClickInsideNav = mainNav.contains(event.target);
        
        if (!isClickInsideBurger && !isClickInsideNav && mainNav.classList.contains('active')) {
            burgerMenu.classList.remove('active');
            mainNav.classList.remove('active');
        }
    });
});
