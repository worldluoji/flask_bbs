
$(function() {

    var ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/'
    });

    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var title_ele = $('input[name=title]');
        var board_ele = $("select[name=board]");
        var title = title_ele.val();
        var board_id = board_ele.val();
        var content = ue.getContent();

        base_ajax.post({
            'url':'/forum/ppost/',
            'data':{
                'title': title,
                'content': content,
                'board_id': board_id
            },
            'success': function(data) {
                if(data['code'] == 200) {
                    bbsalert.alertConfirm({
                        'msg': "文章发表成功",
                        'confirmText': "回到首页",
                        'cancelText': "再写一篇",
                        'confirmCallback' : function() {
                            window.location = '/forum/'
                        },
                        'cancelCallback': function() {
                            title_ele.val("");
                            ue.setContent("");
                        }
                    });
                }else {
                    bbsalert.alertInfo(data['message']);
                }
            },
            'fail': function(error) {
                bbsalert.alertNetworkError();
            }

        });
    });
});
