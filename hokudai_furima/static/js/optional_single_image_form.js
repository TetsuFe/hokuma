$(function(){
    for(var i=0;i<4;i++){
        if($('#img'+i).attr('src') != PLACEHOLDER_IMAGE){
            $("#edde"+i).html('<button type="button" id="rem'+i+'" onclick="resetImg('+i+');return false;">削除</button>');
        }
    }
})

function getImageOriginalWidth(element){
    var img = new Image();
    img.src = element.attr('src');
    var imageOriginaWidth = img.width;
    return imageOriginaWidth;
}

function getImageOriginalHeight(element){
    var img = new Image();
    img.src = element.attr('src');
    var imageOriginaHeight = img.height;
    return imageOriginaHeight;
}

function addImageFitDirectionName(sender_image_id){
    sender_image = $('#img'+sender_image_id)
    let width = getImageOriginalWidth(sender_image);
    let height = getImageOriginalHeight(sender_image);
    if(width >= height){
        sender_image.attr('class', 'width_larger')
    }else{
        sender_image.attr('class', 'height_larger');
    }
}

function fileget(imgfile,targetID){
    targetID=+targetID;
    if(!imgfile.files.length) return;
    var acceptimg = ['image/jpeg', 'image/png']

    var loop_count = 0;
    new Promise(function(res, rej) {
        // ループ処理（再帰的に呼び出し）
        function loop(i) {
            // 非同期処理なのでPromiseを利用
            return new Promise(function(resolve, reject) {

                var fr=new FileReader();
                fr.onload=function(e) {
                    if(acceptimg.indexOf(imgfile.files[loop_count].type)==-1){
                        alert("ファイル形式はjpegかpngにしてください。");
                    }else if(e.target.result.length>1024*1024*20){
                        alert("20MB以下の画像をアップロードできます。");
                    }else{
                        $("#img"+i).attr("src",e.target.result);
                        $("#base64_"+i).val(e.target.result);
                        $("#edde"+i).html('<button type="button" id="rem'+i+'" onclick="resetImg('+i+');return false;">削除</button>');
                        resolve(i+1);
                        $("input[name=image_"+targetID+"_exists]").val(1);
                    }
                }
                fr.readAsDataURL(imgfile.files[loop_count]);

            })
                .then(function(count) {
                    // ループを抜けるかどうかの判定
                    if (count < targetID+imgfile.files.length) {
                        loop_count+=1;
                        // 再帰的に実行
                        loop(count);
                    } else {
                        loop_count+=1;
                        // 抜ける（外側のPromiseのresolve判定を実行）
                        res();
                    }
                });
        }
        // 初回実行
        loop(targetID);
    }).then(function() {
        // ループ処理が終わったらここにくる
        addImageFitDirectionName(targetID);
    })
}

