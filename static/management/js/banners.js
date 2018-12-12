
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
            'url':'/manage/add_banner/',
            'data':{
                'name':name,
                'image_url':image_url,
                'link_url':link_url,
                'priority':priority
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