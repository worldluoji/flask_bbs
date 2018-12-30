
$(function () {
   $('.delete-post-btn').click(function (event) {
       var self = $(this);
       var tr = self.parent().parent();

       var post_id = tr.attr('post-id');

       bbsalert.alertConfirm({
            "msg":"Are you sure to delete this post?",
            'confirmCallback': function() {
                base_ajax.post({
                    'url':'/manage/del_post/',
                    'data':{
                        'post_id':post_id,
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

                });
            }
        });
   });
});

