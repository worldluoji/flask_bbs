

$(function() {
    $('#captha-image').click(function(event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = param_opt.setParam(src,'imagecode',Math.random())
        self.attr('src',newsrc)
    })

})