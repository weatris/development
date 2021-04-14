var dt = new Date();
var temp = new Date();
var months = [
'January',
 'February',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'September',
 'October',
 'November',
 'December'
 ];
var current_day;
var prev_id=123;
var chosen_events=[];
function start()
{
dt.setDate(1);
var day=dt.getDay();

var EndDate = new Date(dt.getFullYear(),dt.getMonth()+1,0).getDate();
var prevDate = new Date(dt.getFullYear(),dt.getMonth(),0).getDate();

var today=new Date().getDate();
document.getElementById("date").innerHTML=dt.toDateString();
document.getElementById("month").innerHTML=months[dt.getMonth()];
var cells="";
for (var x=day;x>0;x--)
    cells+="<div  class='prev_date' onclick=moveDate('prev');>" + (prevDate-x+1) +"</div>";

for (var i=1;i<=EndDate;i++)
{
if( i==today)
    {
    if(dt.getMonth()==temp.getMonth()&&dt.getYear()==temp.getYear())
        cells+="<div id="+i+" class='today' onclick=GetEventsForDay("+i+") >" +i +"</div>";
    else
        cells+="<div id="+i+" style='border:2px solid black;' onclick=GetEventsForDay("+i+") >" +i +"</div>";
    }
else
    cells+="<div id="+i+" onclick=GetEventsForDay("+i+") >" +i +"</div>";
}

document.getElementsByClassName("days")[0].innerHTML=cells;
}

function moveDate(param)
{
if(param=='next')
    dt.setMonth(dt.getMonth()+1);
else
    dt.setMonth(dt.getMonth()-1);
start();
GetEventsForDay(date=current_day)
}

function func(id)
{
    var x = document.getElementById(id);
    if(x.style.display == "block")
        x.style.display = "none";
    else
        x.style.display = "block";
    }

function GetEventsForDay(date=current_day)
{
try{document.getElementById(prev_id).style.borderColor = "HoneyDew";}
catch{
console.log('no day chosen');}
document.getElementById(date).style.borderColor = "crimson";
prev_id=date;
var month = dt.getMonth()+1;
var year = dt.getFullYear();
chosen_events=[];
current_day=date;
$.ajax({
        url:'/get_events',
        type:'post',
        data:{'day':date,
            'month':month,
            'year':year},
        success: function(user_events)
        {
            var x = document.getElementById('ManageEvents');
            x.style.display = "block";
            var tmp = document.getElementById('tableData');
            var temp="";
            if (!user_events['message']){
                try {
                    var temp_array =user_events['user_list'];
                    temp_array.sort(function (a, b) {
                        return parseInt(a['time']) - parseInt(b['time']) ;
                        });
                    for (var key in temp_array){
                        var arr=temp_array[key];
                        temp+="<tr id="+key+"00 onclick='GetClickedEvent(this.id)'><td>"+arr['name']+"</td><td>"+arr['time']+"</td><td>"+arr['description']+"</td></tr>";
                    }
                    tmp.innerHTML=temp;
                    }
                catch(error) {
                    console.log(error);
                    temp+="<tr><td>new event</td><td>hour</td><td>a few words</td></tr>";
                    tmp.innerHTML=temp;
            }
            }
            else{
                temp+="<tr><td>new event</td><td>hour</td><td>a few words</td></tr>";
                tmp.innerHTML=temp;
            }
        }
    });
}
function ShowAddEvent()
{
    var x = document.getElementById('AddEvent');
    if(x.style.display=='none')
        x.style.display='block';
    else
        x.style.display='none';
    document.getElementById("mes_add").innerHTML='<h1>Create new Event</h1>';
    document.getElementById("name").value = "";
    document.getElementById("time").value = "";
    document.getElementById("desc").value = "";
    document.getElementById("date_").value =current_day+'/'+(dt.getMonth()+1)+'/'+dt.getFullYear();
}

function AddEvent()
{
    var name = $("#name").val();
    var time = $("#time").val();
    var date = $("#date_").val();
    var desc = $("#desc").val();
    $.ajax({
        url:'/add_event',
        type:'post',
        data:{'name':name,'time':time,'date':date,'desc':desc},
        success: function(resp)
        {
            console.log(resp);
            if (resp['message']=='Success') {
                ShowAddEvent();
                GetEventsForDay();
            }
            else if (resp['message']=='Invalid data')
                document.getElementById("mes_add").innerHTML ='<h1 style="color:crimson;">Enter data</h1>';
            else
                document.getElementById("mes_add").innerHTML ='<h1 style="color:crimson;">Enter correct data</h1>';
        }
    });
}

function ShowUpdateEvent()
{
    if(chosen_events.length!=0) {
        var x = document.getElementById('UpdateEvent');
        if (x.style.display == 'none')
            x.style.display = 'block';
        else
            x.style.display = 'none';
        var table = document.getElementById(chosen_events[0]);
        document.getElementById("mes_up").innerHTML = '<h1>Update Event</h1>';
        document.getElementById("up_name").value = table.cells[0].innerHTML;
        document.getElementById("up_time").value = table.cells[1].innerHTML;
        document.getElementById("up_desc").value = table.cells[2].innerHTML;
        document.getElementById("up_date").value = current_day + '/' + (dt.getMonth() + 1) + '/' + dt.getFullYear();
    }
}

function UpdateEvent()
{
        var name = $("#up_name").val();
        var time = $("#up_time").val();
        var date = $("#up_date").val();
        var desc = $("#up_desc").val();
        var get_event = document.getElementById(chosen_events[0]);
        $.ajax({
            url:'/update_event',
            type:'post',
            data:{'name':name,
                'time':time,
                'date':date,
                'desc':desc,
                'get_name':get_event.cells[0].innerHTML,
                'get_time':get_event.cells[1].innerHTML,
                'get_desc':get_event.cells[2].innerHTML
            },
            success: function(resp)
            {
                console.log(resp);
                if (resp['message']=='Success'){
                    ShowUpdateEvent();
                    GetEventsForDay();
                }

                else if (resp['message']=='Invalid data')
                    document.getElementById("mes_up").innerHTML ='<h1 style="color:crimson;font-size: 14px;">Enter data</h1>';
                else
                    document.getElementById("mes_up").innerHTML ='<h1 style="color:crimson;font-size: 14px;">Enter correct date</h1>';
            }
        });
}

function ShowDeleteEvent()
{
    if(chosen_events.length!=0) {
        var x = document.getElementById('DeleteEvent');
        if (x.style.display == 'none')
            x.style.display = 'block';
        else
            x.style.display = 'none';
    }
}


function DeleteEvent()
{
    var names=[];
    for (var a of chosen_events){
        var temp = document.getElementById(a);
        names.push(temp.cells[0].innerHTML);
    }
    $.ajax({
        url:'/delete_event',
        type:'post',
        data:{'names':names,
            'date':current_day + '/' + (dt.getMonth() + 1) + '/' + dt.getFullYear(),
        },
        success: function(resp)
        {
            console.log(resp);
            if (resp['message']=='Success'){
                ShowDeleteEvent();
                GetEventsForDay();
            }
            else
                document.getElementById("mes_del").innerHTML ='<h1 style="color:crimson;font-size: 14px;">Error !</h1>';
        }
    });
}

function GetClickedEvent(id)
{
    var table = document.getElementById(id);
    if(table.style.backgroundColor != "lightgreen"){
        table.style.backgroundColor = "lightgreen";
        chosen_events.push(id);
    }
    else{
        table.style.backgroundColor = "white";
        chosen_events.splice(chosen_events.indexOf(id),1);
    }
    //console.log(chosen_events);
}

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