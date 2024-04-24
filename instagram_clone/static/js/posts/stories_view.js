// JavaScript
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById('story-modal');
    var span = document.getElementsByClassName("close")[0];

    var storiesCards = document.querySelectorAll('.stories-card');
    storiesCards.forEach(function(card) {
        card.addEventListener('click', function(event) {
            event.preventDefault();
            var storyId = this.getAttribute('data-story-id');
            var url = this.getAttribute('data-detail-url');

            fetch(url)
            .then(response => response.json())
            .then(data => {
                var imageSrc = data.image.url;
                document.getElementById("modal-image").src = imageSrc;
                modal.style.display = "block";
            })
            .catch(error => console.log('Error:', error));
        });
    });

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
