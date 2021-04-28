// function func()
// {
//     var x = document.getElementById("field");
//     x.style.display = "block";
//     x = document.getElementById("confirm");
//     x.style.display = "none";
// }
function CheckPassword()
{
    var check=$("#check").val();
    $.ajax({
        url:'/user',
        type:'post',
        data:{'check':check},
        success: function(resp)
        {
            if(resp['message']=='Success'){
                func();
                document.getElementById("message").innerHTML ='<h1>Update User Data</h1>';
            }
            else
                document.getElementById("message").innerHTML ='<h1 style="color:crimson;font-size:16px;">Access denied</h1>';
        }
    });
}
function ChangeData()
{
    var name_value=$("#name").val();
    var surname_value=$("#surname").val();
    var username_value=$("#username").val();
    var password_value1=$("#password1").val();
    var password_value2=$("#password2").val();
    var email_value=$("#email").val();
    $.ajax({
        url:'/change_user_data',
        type:'post',
        data:{'name':name_value,
            'surname':surname_value,
            'username':username_value,
            'password1':password_value1,
            'password2':password_value2,
            'email':email_value,
        },
        success: function(resp)
        {
            if(resp['message']=='Success')
                window.location.href='/menu';
            else
                document.getElementById("message").innerHTML ='<h1 style="color:crimson;font-size:16px;">'+resp["message"]+'</h1>';
        }
    });
}