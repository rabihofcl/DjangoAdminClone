$(document).ready(function(){
    $('#signin-form').validate({
        rules: {
            username: {
                required : true,
                alpha : true,
                minlength: 4,
                noSpace : true
            }
        }
    })
})