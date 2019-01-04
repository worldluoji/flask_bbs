
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


$(function() {
   $('.hightlight-post-btn').click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('post-id');
       var highlight = parseInt(tr.attr('high-light'));
       var url = "";

       console.log(highlight);
       if(highlight) {
           url = "/manage/unlight_post/";
       }else {
           url = "/manage/light_post/";
       }

       base_ajax.post({
           'url': url,
           'data':{
               'post_id':post_id
           },
           'success': function (data) {
               if(data['code'] == 200) {
                   bbsalert.alertSuccessToast('Option successfully')
                   setTimeout(function () {
                       window.location.reload();
                   },500);
               } else {
                   bbsalert.alertInfo(data['message']);
               }
           },
           'fail': function (error) {
               bbsalert.alertNetworkError();
           }

       })

   });
});

