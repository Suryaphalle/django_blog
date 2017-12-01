console.log('app.js loaded');

$(document).ready(function(){

  // using jQuery
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

    // let $api_post_comments_list_url = $('#comment_form').attr('data-api_post_comments_detail_url');
    // let $post_comment_list = function(api_post_comments_list_url){
    //     let $post_comments = $('#post_comments');
    //     console.log(api_post_comments_list_url);
    //     $.getJSON(api_post_comments_list_url,function(data){
    //             comment_list = data.results
    //             console.log('success');
    //             let items = []
    //             if(comment_list == 0){
    //                 $post_comments.html("<strong> No comments yet.</strong>");
    //             }
    //             else{
    //                 $.each(comment_list, function(key,val){
    //                     let post = comment_list[key]['post'];
    //                     let created_date = comment_list[key]['created_date'];
    //                     let content = comment_list[key]['text'];
    //                     let user = comment_list[key]['username'];
    //                     let replies_count = comment_list[key]['replies_count'];
    //                     let output = `
    //                     <div class="card comment-card">
    //                         <div class="card-header comments-header">
    //                         <h6>By:${user}. 
    //                             <small>Last Updated: ${ created_date }
    //                                    Replies: ${replies_count} </small></h6>
    //                         </div>
    //                         <div class="card-block">
    //                         <p class="card-text">${ content } </p>
    //                         <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}" >Reply</button> 
    //                        <button  class="btn btn-primary btn-sm button-view-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/post/comment/${comment_id}/detail/">View Replies</button> 
    //                        <ul class="comment-replies mt-2">
    //                         </ul>
    //                         </div>
    //                      </div>
    //                     `;
                        
    //                     items.push(output);
    //                 });
    //                 $post_comments.html(items);
    //             }
    //     });
    // };
    
    // $post_comment_list($api_post_detail_url);    

    let $api_post_detail_url = $('#post_title_id').attr('data-api_post_detail_url');
    let $post_single_comment = function(api_post_detail_url){
        let $post_comments = $('#post_comments');
        var items = []
    $.getJSON(api_post_detail_url,function(data){
        comment_list = data.comments;
        console.log(comment_list);
        let comment_count = data.comment_count;
        let $post_comment_id = $('#post_comment_id');

        $post_comment_id.text(comment_count);
        if(comment_list.length == 0){
          $post_comments.html("<strong> No comments yet.</strong>");

        }
        else{
        $.each(comment_list,function(key,val){
           if (comment_list[key].parent == null){
                let post = comment_list[key]['post'];
                let created_date = comment_list[key]['created_date'];
                let content = comment_list[key]['text'];
                let user = comment_list[key]['username'];
                let replies_count = comment_list[key]['replies_count'];
                let comment_id = comment_list[key]['id'];
                let post_id = comment_list[key]['post'];
                let output = `<div class="card comment-card">
                        <div class="card-header comments-header">
                        <h6>By:${user}. <small>Last Updated: ${ created_date } Replies: ${replies_count}</small></h6>
                           </div>
                           <div class="card-block">
                               <p class="card-text" data-user="${ user }">${ content } </p>
                               <button  class="btn btn-primary btn-sm button-reply comment-reply" data-toggle="modal" data-target="#replyModal" type="button" data-parent_id="${comment_id}" data-post_id = "${post_id}">Reply</button> 
                               <button  class="btn btn-primary btn-sm button-view-replies" data-toggle="comment-replies" type="button" data-comment_parent_id = ${ comment_id } data-comment_detail_url="/api/post/comment/${comment_id}/detail/">View Replies</button> 
                               <ul class="comment-replies mt-2">
                               </ul>
                           </div>
                       </div>
                   `;
                   items.push(output);         
               }
        });
        return $post_comments.prepend(items);
        }
        });
    };
    $post_single_comment($api_post_detail_url);


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
    
    //comment form
    let $comment_form = $('#comment_form');
    $comment_form.submit(function(e){
        e.preventDefault();
        let $formData = $(this).serialize();
        let $post_comments = $('#post_comments');
        let $api_post_comments_list_url = $(this).attr('data-api_post_comments_list_url');
        let $api_post_detail_url = $('#post_title_id').attr('data-api_post_detail_url');
        let urlEndPoint = $(this).attr('data-comment_post_url');
        let api_comment_create_url = $(this).attr('data-api_post_create_url');
        let $error_message = $(this).find('.error-message');
        console.log(api_comment_create_url);

        
        let ajaxCall = $.ajax({
            method: "POST",
            url: api_comment_create_url,
            data: $formData,
         });
        
        ajaxCall.done(function(data, textStatus, jqxhr){
            $error_message.text('Successfully posted comment');

            // $post_single_comment($api_post_detail_url);
                console.log(textStatus);
                console.log(jqxhr);
                document.querySelector("#comment_form").reset();
        });
        ajaxCall.fail(function(data, jqxhr, textStatus, errorThrown){
            console.log(data.message);
            console.log(jqxhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
    });


 // button view replies
  $(document.body).on("click", ".button-view-replies", function(e){
           e.preventDefault();
           let $this_ = $(this);
           let comment_detail_url = $this_.attr('data-comment_detail_url');
           let $replies_list_ul = $this_.next('.comment-replies');
           $view_btn_replies_text = $this_.text();
          
           if ($this_.text() == 'View Replies'){
                
               $this_.text('Hide Replies');
               $replies_list_ul.show('slow');
                console.log(comment_detail_url);
               $.getJSON(comment_detail_url, function(data) {
                console.log(data.replies);
                let replies_list = data.replies;
                // console.log(replies_list);
                var items = [];
                if (replies_list == 0){
                    $replies_list_ul.html('<strong> no replies yet!.</strong>');
                }
                else{
                    $.each(replies_list, function(key, val) {
                       let content = replies_list[key].text;
                       let user = replies_list[key].username;
                       let output = `<li> replied by: ${user} </br> content: ${content}</li>`;
                       items.push(output);
                   });
                   $replies_list_ul.html(items);
                }
            });
           }
           else{
               $this_.text('View Replies');
               $replies_list_ul.hide('slow');
           }
    });
 
 
 // reply button
 $(document.body).on("click", ".comment-reply", function(event){
       event.preventDefault();
       let $this_ = $(this);
       let comment_text = $this_.prev('p').attr('data-user');
       $("#replyModal #comment_text_content").text(comment_text);
       let parentId = $this_.attr("data-parent_id");
       console.log(parentId);
       let post_id = $this_.attr('data-post_id');
       console.log(post_id);  
       $("#replyModal textarea").after("<input type='hidden' value='" + parentId + "' name='parent' />");
       $("#replyModal textarea").after("<input type='hidden' value='" + post_id + "' name='post' />");
   });

    let $form_replies= $('.form-replies');
    $form_replies.submit(function(e){
        e.preventDefault();
        let $formData = $(this).serialize();
        let urlEndPoint = $(this).attr('data-comment_post_url');
        let $error_message = $(this).find('error-message');
        let json_data = JSON.stringify($formData);
        let api_comment_replies_url = $(this).attr('data-comment_replies_url');

        console.log(api_comment_replies_url);
        
        let ajaxCall = $.ajax({
            method: "POST",
            url: api_comment_replies_url,
            data: $formData,
        });
        ajaxCall.done(function(data, textStatus, jqxhr){
            console.log(data)
            $error_message.text('Successfully replied to comment ..!').fadeOut('slow');
            $('#replyModal').modal('hide');
            $('.form_replies').trigger('reset');
        });
        ajaxCall.fail(function(xhr, textStatus, error){
            console.log(xhr);
            console.log(textStatus);
            console.log(error);
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

    //like button

    // function updateText(btn, newCount, verb){
    //       btn.text(verb)
    // }

    // $(".like-btn").click(function(e){
    //     e.preventDefault()
    //     var this_ = $(this)
    //     var likeUrl = this_.attr("data-href")        
    //     var likeCount = parseInt(this_.attr("data-likes")) | 0
    //     var addLike = likeCount + 1
    //     var removeLike = likeCount - 1
    //     if (likeUrl){
    //        $.ajax({
    //         url: likeUrl,
    //         method: "GET",
    //         data: {},
    //         success: function(Ldata){
    //           //console.log(data)
    //           var newLikes;
    //           console.log(Ldata)
    //           if (Ldata.liked){
    //               updateText(this_, addLike, "Unlike")
    //           } else {
    //               updateText(this_, removeLike, "Like")
    //               // remove one like
    //           }
    //         }, error: function(error){              
    //           console.log("error")
    //         }
    //       })
    //     }
       
    //   });
 
     let $posts_status = $('.posts-status');
      $posts_status.change(function(event){
     let $this_ = $(this);
     let post_id = $this_.attr('data-post_id');
     let $form = $this_.closest('.form-post-status_update');
     let $td_approved = $this_.closest('td').prev('td');
    
     let post_update_url = $form.attr('data-post_update_url');
     let $formData = $form.serialize();
     console.log(post_update_url);

     if($this_.prop("checked")){
       console.log('checked ' + post_id);
       console.log($formData);
       let ajaxCall = $.ajax({
         method: "PUT",
         url:post_update_url ,
         data:{"approved":"True"},
       });
       ajaxCall.done(function(data, textStatus, jqxhr){
         console.log(data);
         $td_approved.text(data.approved);
         console.log(textStatus);
       });
       ajaxCall.fail(function(xhr, textStatus, error){
         console.log(error);
         console.log(xhr);
         console.log(textStatus);
       });
     }
     else{
       console.log('unchecked ' + post_id);
       console.log($formData);
       let ajaxCall = $.ajax({
         method: "PUT",
         url:post_update_url ,
         data:  {"approved":"False"},
       });

       ajaxCall.done(function(data, textStatus, jqxhr){
         $td_approved.text(data.approved);
         console.log(data);
       });
       ajaxCall.fail(function(xhr, textStatus, error){
         console.log(xhr);
         console.log(textStatus);
         console.log(error);
       });
     }
   });

});