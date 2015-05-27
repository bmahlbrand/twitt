$('#loginform').submit(function(e) {
    if ($.trim($("#username").val()) === "" || $.trim($("#password").val()) === "") {
        e.preventDefault();
        console.log('shit');
    }
});