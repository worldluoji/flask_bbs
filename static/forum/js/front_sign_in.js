
$(function() {
    $('#signin-btn').click(function(event) {
        event.preventDefault();
        var telephone_ele = $("input[name=telephone]");
        var password_ele = $("input[name=password]");
        var remember_ele = $("input[name=remember]");

        var telephone = telephone_ele.val()
        var password = password_ele.val()
        var remember = remember_ele.val()

        base_ajax.post({
            "url":"/forum/signin/",

            "data":{
                "telephone":telephone,
                "password":password,
                "remember":remember
            },

            "success": function(data) {
                 if(data['code'] == 200) {

                    var return_to = $("#return-to-span").text();
                    if(return_to) {
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }

                }else {
                    bbsalert.alertInfo(data['message']);
                }
            },

            "fail": function(error) {
                bbsalert.alertNetworkError();
            }

        })
    })
})