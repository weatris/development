var chosen_friends=[];
function DeleteAccount()
{
    debugger;
    $.ajax({
        url:'/delete_account',
        type:'post',
        success: function(resp)
        {
            console.log(resp);
            if (resp['message']=='Success'){
                window.location.href='/';
            }
        }
    });
}
function ShowDeleteAccount()
{
    var x = document.getElementById('DeleteAccount');
    if (x.style.display == 'none')
        x.style.display = 'block';
    else
        x.style.display = 'none';
}
function  check()
{
    var x = document.getElementById('admin');
    if('{{ role }}'=='admin'){

        if (x.style.display == 'none')
            x.style.display = 'block';
    }
    else
        x.style.display = 'none';
}
function func(id)
{
    var x = document.getElementById(id);
    if(x.style.display == "block")
        x.style.display = "none";
    else
        x.style.display = "block";
}
function SelectFriend(id)
{
    var x = document.getElementById(id);
    if(x.style.backgroundColor=='aquamarine')
    {
        chosen_friends.splice(chosen_friends.indexOf(x.innerHTML));
        x.style.backgroundColor='white'
    }
    else
    {
        chosen_friends.push(x.innerHTML);
        x.style.backgroundColor='aquamarine';
    }
}
function Show_Fields(yes = false)
{
    var x = document.getElementById("field");
    var y = document.getElementById("confirm");
    document.getElementById("check_password").value='';
    if (yes){
        x.style.display = "none";
        y.style.display = "block";
    }
    else
    {
        x.style.display = "block";
        y.style.display = "none";
    }
}

function ShowManageAccount()
{
    func('back');
    func('ManageUser');
    Show_Fields(true)
}

function CheckPassword()
{
    var check=$("#check_password").val();
    $.ajax({
        url:'/user',
        type:'post',
        data:{'check':check},
        success: function(resp)
        {
            if(resp['message']=='Success'){
                Show_Fields();
                document.getElementById("user_name").value=resp['name'];
                document.getElementById("surname").value=resp['surname'];
                document.getElementById("email").value=resp['email'];

                document.getElementById("message").innerHTML ='<h1>Update User Data</h1>';
            }
            else
                document.getElementById("message").innerHTML ='<h1 style="color:crimson;">Access denied</h1>';
        }
    });
}
function ChangeData()
{
    var name_value=$("#user_name").val();
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
                func('ManageUser')
            else
                document.getElementById("message").innerHTML ='<h1 style="color:crimson;">'+resp["message"]+'</h1>';
        }
    });
}
function LogOut()
{
    debugger;
    console.log('logging out');
    $.ajax({
        url:'/log_out',
        type:'post',
        data:{},
        success: function(resp)
        {
            if (resp['message']=='Success')
                window.location.href='/';
        }
    });
}