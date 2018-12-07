

$(function() {
    $('#captha-image').click(function(event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = param_opt.setParam(src,'imagecode',Math.random())
        self.attr('src',newsrc)
    })

})


$(function() {
    $('#register-btn').click(function(event) {
        event.preventDefault();
        console.log("Enter in")
        var telephone_ele = $("input[name=telephone]");
        var username_ele = $("input[name=username]");
        var sms_captcha_ele = $("input[name=sms_captcha]");
        var password_ele = $("input[name=password]");
        var password_repeat_ele = $("input[name=password_repeat]");
        var graph_captcha_ele = $("input[name=graph_captcha]");

        var telephone = telephone_ele.val();
        var username = username_ele.val();
        var sms_captcha = sms_captcha_ele.val();
        var password = password_ele.val();
        var password_repeat = password_repeat_ele.val();
        var graph_captcha = graph_captcha_ele.val();

        base_ajax.post({
            'url':'/forum/signup/',

            'data':{
                'telephone':telephone,
                'sms_captcha':sms_captcha,
                'username':username,
                'password':password,
                'password_repeat': password_repeat,
                'graph_captcha':graph_captcha
            },

            'success':function (data) {
                if(data['code'] == 200) {

                    var return_to = $("#return-to-span").text();
                    console.log(return_to);
                    if(return_to) {
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }

                }else {
                    bbsalert.alertInfo(data['message']);
                }
            },

            'fail':function (error) {
                console.log(error["message"]);
                bbsalert.alertNetworkError();
            }

        })

    })
})