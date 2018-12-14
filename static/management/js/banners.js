
$(function() {
    $('#set-banner-btn').click(function(event) {
        event.preventDefault();
        var diag = $("#banner-dialog");
        var name_ele = $("input[name=name]");
        var image_url_ele = $("input[name=image_url]");
        var link_url_ele = $("input[name=link_url]");
        var priority_ele = $("input[name=priority]");

        var name = name_ele.val();
        var image_url = image_url_ele.val();
        var link_url = link_url_ele.val();
        var priority = priority_ele.val();
        var submitType = $(this).attr('data-type');
        var url = '';
        var banner_id = $(this).attr("data-id");

        if(submitType == 'edit') {
            url = '/manage/edit_banner/';
        }else{
            url = '/manage/add_banner/';
        }

        if(!name) {
            bbsalert.alertInfoToast("Please Input banner name");
            return;
        }

        if(!image_url) {
            bbsalert.alertInfoToast("Please Input Image url");
            return;
        }

        if(!link_url)　{
            bbsalert.alertInfoToast("Please Input link url");
            return;
        }

        if(!priority) {
             bbsalert.alertInfoToast("Please Input priority");
             return;
        }
        
        base_ajax.post({
            'url':url,
            'data':{
                'name':name,
                'image_url':image_url,
                'link_url':link_url,
                'priority':priority,
                'banner_id':banner_id
            },
            'success':function(data){
                diag.modal("hide");
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
        
        
    });

});

$(function () {
    $('.edit-banner-btn').click(function(event) {
        var diag = $("#banner-dialog");
        diag.modal("show");
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var name_ele = diag.find("input[name=name]");
        var image_url_ele = diag.find("input[name=image_url]");
        var link_url_ele = diag.find("input[name=link_url]");
        var priority_ele = diag.find("input[name=priority]");
        var saveBtn = diag.find("#set-banner-btn");

        name_ele.val(name);
        image_url_ele.val(image_url);
        link_url_ele.val(link_url);
        priority_ele.val(priority);

        saveBtn.attr("data-type",'edit');
        saveBtn.attr("data-id",tr.attr('data-id'));

    });
});


$(function() {
    $('.delete-banner-btn').click(function (event) {

        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');

        bbsalert.alertConfirm({
            "msg":"Are you sure to delete this banner?",
            'confirmCallback': function() {
                base_ajax.post({
                    'url':'/manage/del_banner/',
                    'data':{
                        'banner_id':banner_id,
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
        })

    });
});