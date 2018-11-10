

$(function () {

    $("#submit").click(function (event) {
        event.preventDefault();
        var oldpwdNode = $("input[name=oldpwd]");
        var newpwdNode = $("input[name=newpwd]");
        var newpwd2Node = $("input[name=newpwd2]");

        var oldpwd = oldpwdNode.val();
        var newpwd = newpwdNode.val();
        var newpwd2 = newpwd2Node.val();
        /*
        *  AJAX csrf protect
        *  1. render a csrf-token in meta tag in template
        *  2. set X-CSRFtoken in ajax request head
        *
        * */
        base_ajax.post({
            'url': '/manage/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },

            'success': function (data) {
                console.log('success')
                if(data['code'] == 200) {
                    bbsalert.alertSuccessToast('You have succeed to modify the password')
                    oldpwdNode.val("");
                    newpwdNode.val("");
                    newpwd2Node.val("");

                }else{
                    var message = data['message'];
                    bbsalert.alertInfo(message);
                }
            },

            'fail': function (error) {
                console.log('fail')
                bbsalert.alertNetworkError();
            }
        });

        console.log("ajax finished");

    });

});