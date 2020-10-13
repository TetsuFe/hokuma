$(window).on('load', function(){
    // 未読のお知らせの数をバッジに表示する
    $.ajax({
      url: '/notification/ajax/unread_number/',
      type: 'GET',
      processData: false,
      contentType: false,
      dataType: 'json'
    })
    .done(function(data){
        if(data.notification_number!=0){
            $('.notification-badge').text(data.notification_number);
        }
    }).fail(function(){
    });

    // 未完了のTODDの数をバッジに表示する
    $.ajax({
      url: '/todo_list/ajax/undone_number/',
      type: 'GET',
      processData: false,
      contentType: false,
      dataType: 'json'
    })
    .done(function(data){
        if(data.undone_todo_number!=0){
            $('.todo-badge').text(data.undone_todo_number);
        }
    }).fail(function(){
    });
});
