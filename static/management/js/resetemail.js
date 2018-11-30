
$(function() {

    $("#captcha-btn").click(function (event) {
            event.preventDefault();
            var email = $("input[name='email']").val();

            if(!email) {
                bbsalert.alertInfoToast("Please input email");
                return;
            }

            base_ajax.get({
                'url': '/manage/email_captcha/',
                'data': {
                    'email': email,
                },

                'success': function (data) {
                    console.log('success')
                    if (data['code'] == 200) {
                        bbsalert.alertSuccessToast('Succeed to send email, please check');
                        //oldpwdNode.val("");
                        //newpwdNode.val("");
                        //newpwd2Node.val("");

                    } else {
                        bbsalert.alertInfo(data['message']);
                    }
                },

                'fail': function (error) {
                    bbsalert.alertNetworkError();
                }
            });
     });
});


$(function() {

    $("#confirm-btn").click(function (event) {
        event.preventDefault();
        var emailEle = $("input[name='email']");
        var captchaEle = $("input[name='captcha']");
        var email = emailEle.val();
        var captcha = captchaEle.val();

         base_ajax.post({
                'url': '/manage/resetemail/',
                'data': {
                    'email': email,
                    'captcha':captcha
                },

                'success': function (data) {
                    if (data['code'] == 200) {
                        console.log("success");
                        bbsalert.alertSuccessToast('Succeed to modify email');
                        emailEle.val("");
                        captchaEle.val("");

                    } else {
                        console.log("error");
                        bbsalert.alertInfo(data['message']);
                    }
                },

                'fail': function (error) {
                    bbsalert.alertNetworkError();
                }
         });
    });

});