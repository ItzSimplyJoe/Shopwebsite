$(document).ready(function() {
    $('#popup').hide();
    {% if login_failed %}
        $('#popup').show();
    {% endif %}
    $('#popup-close-button').click(function() {
        $('#popup').hide();
    });
});
