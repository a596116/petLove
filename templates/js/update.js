var url = location.href;
if(url.indexOf('?')!=-1)
    {
        var ary1 = url.split('?');
        var ary3 = ary1[1].split('=');
        var id = ary3[1];
    };
function initializeApp(data){ //初始化LIFF
    var userid = data.context.userid; //取得ID
    }
$(document).ready(function (){
    liff.init(function (data){ //初始化LIFF
        initializeApp(data);
      });
    
    let num = id;
    
    $.ajax({
    url: "https://script.google.com/macros/s/AKfycbzWqjtGT3gSBBCEQTuEUTmx_fiNPiAb-JJ_oimme5rtYaEJvmgzOXZNu21A5il1BGXw_w/exec",
    data: {
        "num":num,
    },
    success: function(na) {
        
        $('#sure').click(function (e){
        update();
        liff.sendMessages([
            {type: 'text',text: "更新完畢！"}
          ])
            .then(()=>{
              liff.closeWindow();
            })
        });
        var data = na.split(',');
        
        document.getElementById("petphoto").src = data[5];
        document.getElementById("name").innerHTML = '主人姓名：' + data[0] + '<img id="updatename"  src = "https://upload.cc/i1/2021/04/10/jVFiI0.png" style="display: inline-block;"  />';
        document.getElementById("phone").innerHTML = '主人手機：' + data[1] +'<img id="updatephone"  src = "https://upload.cc/i1/2021/04/10/jVFiI0.png" style="display: inline-block;"  />';
        document.getElementById("email").innerHTML = '主人信箱：' + data[2] +'<img id="updateemail"  src = "https://upload.cc/i1/2021/04/10/jVFiI0.png" style="display: inline-block;"  />';
        document.getElementById("petname").innerHTML = '寵物名字：' + data[3] +'<img id="updatepetname"  src = "https://upload.cc/i1/2021/04/10/jVFiI0.png" style="display: inline-block;"  />';
        
        
        function update(){
            if ($('#newname').val() != undefined && $('#newname').val() != ''){
                data[0] = $('#newname').val();
            };
            if ($('#newphone').val() != undefined && $('#newphone').val() != ''){
                data[1] = $('#newphone').val();
            };
            if ($('#newemail').val() != undefined && $('#newemail').val() != ''){
                data[2] = $('#newemail').val();
            };
            if ($('#newpetname').val() != undefined && $('#newpetname').val() != ''){
                data[3] = $('#newpetname').val();
            };
            if ($('#sel_room').val() != '種類'){
                data[4] = $('#sel_room').val();
            };
            if (document.getElementById("petphoto").src == data[4]){
                data[5] =  document.getElementById("petphoto").src ;
            };
            $.ajax({
                url: "https://script.google.com/macros/s/AKfycbzWqjtGT3gSBBCEQTuEUTmx_fiNPiAb-JJ_oimme5rtYaEJvmgzOXZNu21A5il1BGXw_w/exec",
                data: {
                    "newname": data[0],
                    "newphone": data[1],
                    "newemail": data[2],
                    "newpetname": data[3],
                    "newhow": data[4],
                    "newphoto":data[5],
                    "num":num,
                },
              });
          };
        
        $('#updatename').click(function (e){
            document.getElementById("name").innerHTML = '主人姓名：' + '<input type="text" id="newname" name="newname"  class="form-control"  value="" style="font-size:15px;width: 130px;width:140px">';
            });
        
        $('#updatephone').click(function (e){
            document.getElementById("phone").innerHTML = '主人手機：' + '<input type="text" id="newphone" name="newphone"  class="form-control"  value="" style="font-size:15px;width: 130px;width:140px">';
            });
        $('#updateemail').click(function (e){
            document.getElementById("email").innerHTML = '主人信箱：' + '<input type="text" id="newemail" name="newemail"  class="form-control"  value="" style="font-size:15px;width: 130px;width:140px">';
            });
        $('#updatepetname').click(function (e){
            document.getElementById("petname").innerHTML = '寵物名字：' + '<input type="text" id="newpetname" name="newpetname"  class="form-control"  value="" style="font-size:15px;width: 130px;width:140px">';
            });
        
    },
    
    });
    
});