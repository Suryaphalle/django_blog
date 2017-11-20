console.log('app.js loaded');

$(document).ready(function(){
    $('.form-replies').hide();
    $('.comment-replies').hide();
    // $("button").click(function(){
    //     $("#login_title").animate({left: '250px'});
        
    // });

    //  $("#test_btn").click(function(){
    //     $("#id_username").val("suryakant");
    //     $("#id_email").val("suryakantjp@gmail.com");

    // });

    $('#id_email').change(function(){
      if (!this.value.includes('@'))
        {
            $(this).addClass('has-error')
        }
        else
        {
            $(this).addClass('has-success')
        } 
    });
    $('.card').mouseenter(function(event) {
        $(this).addClass('card-outline-danger');
        // $('.card-header').css('background-color','#c2ccce');
        // $('.card-title').css('text-color','white');
    });
    $('.card').mouseleave(function(event) {
        $(this).removeClass('card-outline-danger');
    
    });
    $('#search').autocomplete({
        minLength:2,
        source:function(req,add){
        let search = $('#search').val();
        let form_search_post = $('#form_search_post');
        let urlEndPoint = form_search_post.attr('data-url');
            $.ajax({
                url:  urlEndPoint,
                dataType : 'json',
                type : 'GET',
                data: {'start':search},
                success: function(data){
                    var suggetstions = [];
                    $.each(data,function(index,objects){
                        suggetstions.push(objects);
                    });
                    add(suggetstions);
                },
                error :function(err){
                    console.log(err);
                }
            });
        }
    });

    //reply section
    $('.button-reply').click(function(e){
        e.preventDefault();
        let $this_ = $(this);
        let $form_replies = $this_.closest('div').find('.form-replies');
        $($form_replies).toggle();

    });
    $('.button-view-replies').click(function(e){
        e.preventDefault();
        let $this_ = $(this);
        let $form_replies = $this_.closest('div').find('.form-replies');
        let $comment_replies = $this_.closest('div').find('.comment-replies');
        $($comment_replies).toggle();
        $($form_replies).toggle();
    });

    
    //comment form
    let $comment_form = $('#comment_form');
    $comment_form.submit(function(e){
        e.preventDefault();
        let $formData = $(this).serialize();
        let $thisUrl = window.location.href;
        let $error_message = $(this).find('.error-message');

        $.ajax({
            method : 'POST',
            url : $thisUrl,
            data : $formData,
            success : function(data, textStatus, jqxhr){
                $error_message.text(data.message);
                console.log(data.message);
                console.log(textStatus);
                console.log(jqxhr);
                document.querySelector('#comment_form').reset();
            },
            error: function(data, xhr, status, error){
                console.log(data.message);
                console.log(xhr);
                console.log(status);
                console.log(error);                
            },
        });
    });

    let $form_replies= $('.form-replies');
    $form_replies.submit(function(e){
        e.preventDefault();
        let $formData = $(this).serialize();
        let $thisUrl = window.location.href;
        let $error_message = $(this).find('error-message');
        let json_data = JSON.stringify($formData);

        $.ajax({
            method : 'POST',
            url : $thisUrl,
            data : $formData,
            success : function(data, textStatus, jqxhr){
                $error_message.text(data);
                console.log(data);
                console.log(textStatus);
                console.log(jqxhr);
                document.querySelector('.form-replies').reset();
            },
            error: function(data, xhr, textStatus, error){
                console.log(data.message);
                console.log(xhr);
                console.log(textStatus);
                console.log(error);                
            },
        });
    });

    //new post form
    let $new_post_form = $('#new_post_form');
    $new_post_form.submit(function(event){
        event.preventDefault();
        let $formData = $(this).serialize();
        let $thisUrl = window.location.href;
        let $error_message = $('#error');
        // console.log($formData);
        $.ajax({
            method : 'POST',
            url : $thisUrl,
            data : $formData,
            success : function(data , textStatus, jqxhr){
                $error_message.text(data.message);
                console.log(data.message);
                console.log(textStatus);
                console.log(jqxhr);
                document.querySelector('#new_post_form').reset();
            },
            error: function(data, xhr, status, error){
                console.log(data.message);
                console.log(xhr);
                console.log(status);
                console.log(error);
            },
        });
    });

    //contact form
    let $contact_form = $('.contact-form');
    $contact_form.submit(function(event){
        event.preventDefault();
        let $formData =$(this).serialize();
        let $thisUrl = $contact_form.attr('data-url') || window.location.href;
        let $error_message = $('#error');
        $.ajax({
            method: "POST",
            url: $thisUrl,
            data: $formData,
            success: function(data, textStatus, jqxhr){
                $error_message.text(data.message);
                console.log(data.message);
                console.log(textStatus);
                console.log(jqxhr);
                // $contact_form.reset();
                console.log($contact_form);
                document.querySelector(".contact-form").reset();
            },
            error: function(xhr, status, error){
                console.log(xhr);
                console.log(status);
                console.log(error);
            },

        });
    });
});