$(document).ready(function () {

    $("#signup-form").mouseenter(function () {
        $(this).css({ "background": "#ffffff" })
    })
    $("#signup-form").mouseleave(function () {
        $(this).css({ "background": "#0275d8" })
    })


    $("#signup-form").validate({
        rules: {
            username: {
                required : true,
                minlength : 4,
                alpha : true,
                noSpace : true
            }
        }
    })
})