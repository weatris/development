function func()
{
    var name_value=$("#name").val();
    var surname_value=$("#surname").val();
    var username_value=$("#username").val();
    var password_value1=$("#password1").val();
    var password_value2=$("#password2").val();
    var email_value=$("#email").val();
    $.ajax({
        url:'/sign_up',
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
            if (resp['message']=='Success'){
                alert(resp['message']);
                window.location.href='/menu';
            }
            document.getElementById("message").innerHTML="<h1 style='color:crimson;font-size: 22px;'>"+resp['message']+"</h1>";
            console.log(resp);
        }
    });
}