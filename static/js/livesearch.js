$(document).ready(function(){
    $('#query').autocomplete({
        source : []
        select : function(event,ui){
            event.preventDefault();
            $('#query').val(ui.item.label);
            window.location.href = ui.item.value;
        },
        focus: function(event,ui){
            $('#query').val(ui.item.label);
        },
        minLength: 3,
        delay: 500,
    });
    $('input#query').keyup(function(){
        var query = $(this).val();

        if(query.length>3){
            dataString = 'q='+query;
            $.ajax({
                type : "POST",
                url : "/api/v1/ajaxsearch/",
                data : dataString,
                success : function(response){
                    var availableHints = [];
                    for (var i in response.posts){
                        availableHints.push({
                            value: "/view_post/"+ response.posts[i].id,
                            label: response.posts[i].title
                        });
                    }
                    $('#query').autocomplete({
                        source: availableHints,
                    });
                }
            });
        }
    });
});