document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');

    document.querySelectorAll('.post_container').forEach(el => {
      el.addEventListener('click', function(e) {
        if (e.target.closest('button, a')) return;
        window.location.href = el.dataset.href;
      });
    });

    // Charger l'état initial des likes pour chaque bouton
    likeButtons.forEach(button => {
        const postId = button.dataset.postId;

        // Récupérer l'état initial
        fetch(`/blog/like-status/${postId}/`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                const icon = button.querySelector('.like-icon');
                const count = button.querySelector('.like-count');

                if (data.liked) {
                    icon.textContent = '💙';
                    button.dataset.liked = 'true';
                } else {
                    icon.textContent = '🤍';
                    button.dataset.liked = 'false';
                }
                count.textContent = data.likes_count;
            })
            .catch(error => {
                console.error('Erreur lors du chargement de l\'état des likes:', error);
            });

        // Gérer les clics
        button.addEventListener('click', function() {
          const postId = this.dataset.postId;

          fetch(`/blog/like/${postId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
                  'Content-Type': 'application/json',
              },
          })
          .then(response => response.json())
          .then(data => {
              // Mettre à jour l'icône
              const icon = this.querySelector('.like-icon');
              const count = this.querySelector('.like-count');

              if (data.liked) {
                  icon.textContent = '💙';
                  this.dataset.liked = 'true';
              } else {
                  icon.textContent = '🤍';
                  this.dataset.liked = 'false';
              }

              // Mettre à jour le compteur
              count.textContent = data.likes_count;
          })
          .catch(error => {
              console.error('Erreur:', error);
          });
        });
    });
});

// Fonction pour récupérer le token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}