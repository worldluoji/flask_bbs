
$(function() {
    $('#add-board-btn').click(function(event) {
        event.preventDefault();
        bbsalert.alertOneInput({
            'text':'请输入板块的名称',
            'placeholder':'板块名称',
            'confirmCallback':function(inputValue) {
                base_ajax.post({
                    'url':'/manage/add_board/',

                    'data':{
                      'board_name':inputValue
                    },

                    'success':function (data) {
                        if(data['code'] == 200) {
                            window.location.reload();
                        }else {
                            bbsalert.alertInfo(data['message']);
                        }
                    },

                    'fail':function(error) {
                        bbsalert.alertNetworkError();
                    }

                })
            }

        });

    });
});


$(function () {
    $('.edit-board-btn').click(function(event) {

        var self = $(this);
        var tr = self.parent().parent();
        var board_name = tr.attr("board-name");
        var board_id = tr.attr("board-id");

        bbsalert.alertOneInput({
            'text':'请输入板块的名称',
            'placeholder':board_name,
            'confirmCallback':function(inputValue) {
                base_ajax.post({
                    'url':'/manage/edit_board/',

                    'data':{
                      'board_name':inputValue,
                      'board_id':board_id,
                    },

                    'success':function (data) {
                        if(data['code'] == 200) {
                            window.location.reload();
                        }else {
                            bbsalert.alertInfo(data['message']);
                        }
                    },

                    'fail':function(error) {
                        bbsalert.alertNetworkError();
                    }

                })
            }

        });

    });
});


$(function () {
   $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr("board-id");
        bbsalert.alertConfirm({
            "msg":"Are you sure to delete this banner?",
            'confirmCallback': function() {
                base_ajax.post({
                    'url':'/manage/del_board/',
                    'data':{
                        'board_id':board_id,
                    },
                    'success':function(data){
                        if(data['code'] == 200) {
                            window.location.reload();
                        }else {
                            bbsalert.alertInfo(data["message"]);
                        }
                    },
                    'fail':function (error) {
                        bbsalert.alertNetworkError();
                    }

                })
            }
        });
   });
});

