$(document).on('submit', 'form.delete_talk_form',function() {
    $.ajax({
    'url':$(this).attr('action'),
        'type':'POST',
        'data':{
            'talk_id': $(this).children('input[name="talk_id"]').val(),
        },
        'dataType':'json',
        'success':function(response){  // 通信が成功したら動く処理で、引数には返ってきたレスポンスが入る
            let talk_id = response.talk_id;
            $('div[id='+talk_id+']').remove();
        },
        'cache': false,
    });
    return false;
});
