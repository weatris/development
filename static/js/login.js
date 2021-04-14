$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
            data : {
                name : $('#name').value(),
                email : $('#password').value()
            },
            type : 'GET',
            url : '/login'
        })
        .done(function(data) {
            if (data.error) {
                alert('no');
                var t =document.getElementById('meta');
                t.text="Enter correct password/name";
            }
            else {
                window.location.href = 'menu.html';
            }
        });
        event.preventDefault();
    });
});

