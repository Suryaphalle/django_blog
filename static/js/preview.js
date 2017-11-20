//preview panel
    let $id_title = document.querySelector('#id_title');
    let $id_text = document.querySelector('#id_text');

    $id_title.addEventListener("input",function(event){
        let $new_post_title = document.querySelector('#new_post_title');
        $new_post_title.textContent = event.target.value;
    }, false);

    $id_text.addEventListener("input",function(event){
        let $new_post_content = document.querySelector('#new_post_content');
        $new_post_content.textContent = event.target.value;
    }, false);
