/**
 * Created by zhaopengya on 17-4-21.
 */
/**
 * Created by Administrator on 2015/3/20.
 */

document.write('<link href="mop-lqs.css" rel="stylesheet"/>');
document.write('<script src="jquery-1.9.1.min.js"><\/script>');
//杞藉叆涓�
document.onreadystatechange = subSomething;
function subSomething(){
    if(document.readyState == "complete"){
        Mopload();
    }
}
function initevent()
{
    jQuery.event.add();
}
//鑾峰彇闅忔満鏁�
function getRandom(n){
    return Math.floor(Math.random()*n+1)
}
function addfourstlye(obj,name,value)
{
    var four_list=["-webkit-","-moz-","-o-",""];
    for(var i=0;i<four_list.length;i++)
    {
        obj.css(four_list[i]+name,value);
    }
}

function Mopload()
{
    var load_name_list=["rotating-plane","double-bounce","wave","wandering-cubes","pulse","chasing-dots","three-bounce","circle","cube-grid","run-ball","fading-circle"];
    var default_load="rotating-plane";
    var default_index=0;
   $("[class^=mop-load]").each(function(index){
        var _mop_html=$(this).html().trim();
        var _mop_class=$(this).attr("class");
        var _temp=_mop_class.split("mop-load-");
       if(_temp.length<2)
       {
           return;
       }
        var arr='<div class="mop-load-div">';
       if(_temp[1].trim()*1<load_name_list.length)
        {
            arr+='<div class="mop-css-'+_temp[1].trim()+'">'
        }else if(_temp[1].trim()=="x")
        {
            arr+='<div class="mop-css-x">';
        }else
        {
            return;
        }
        if(_mop_html=="")
        {
            _mop_html="Loading鈥︹€�"
        }else
        {
            $(this).html(_mop_html);
        }
        arr+='</div><div class="mop-load-text" >'+_mop_html+'</div></div>';
         $(this).html(arr);
       //addfourstlye($(this),"transition","height 2s linear 0s;");
       $(this).css("text-align","center");
       //$(this).find(".mop-load-div").hide();
    })
    $("[class^=mop-css]").each(function(index){
        var _mop_class=$(this).attr("class");
        var _temp=_mop_class.split("mop-css-");
        if(_temp=="mop-css")
        {
            $(this).addClass(default_load);
        }
        if(_temp[1].trim()=="x")
        {
            var rand=getRandom(load_name_list.length-1);
            $(this).addClass(load_name_list[rand]);
        }else  if(_temp[1]*1<load_name_list.length)
        {
            $(this).addClass(load_name_list[_temp[1]]);
        }else
        {
            return;
        }
    });
    $(".double-bounce").each(function(index)
    {
        var arr='<div class="double-bounce1"></div><div class="double-bounce2"></div>';
        $(this).append(arr);
    });
    $(".wave").each(function(index)
    {
        var arr='<div class = "rect1" ></div><div class = "rect2" ></div><div class = "rect3" ></div><div class = "rect4" ></div><div class = "rect5" ></div>';
        $(this).append(arr);
    });
    $(".wandering-cubes").each(function(index)
    {
        var arr='<div class="cube1"></div><div class="cube2"></div>';
        $(this).append(arr);
    });
    $(".chasing-dots").each(function(index)
    {
        var arr='<div class="dot1"></div><div class="dot2"></div>';
        $(this).append(arr);
    });
    $(".three-bounce").each(function(index)
    {
        var arr='<div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div>';
        $(this).append(arr);
    });
    $(".circle").each(function(index)
    {
        var arr='<div class="spinner-container container1"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div>';
        arr+='<div class="spinner-container container2"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div>';
        arr+='<div class="spinner-container container3"><div class="circle1"></div><div class="circle2"></div><div class="circle3"></div><div class="circle4"></div></div>'
        $(this).append(arr);
    });
    $(".cube-grid").each(function(index)
    {
        var arr='<div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div><div class="sk-cube"></div>';
        $(this).append(arr);
    });
    $(".run-ball").each(function(index)
    {
        var arr='<span class="sk-inner-circle"></span>';
        $(this).append(arr);
    });
    $(".fading-circle").each(function(index)
    {
        var arr='<div class="sk-circle1 sk-circle"></div><div class="sk-circle2 sk-circle"></div><div class="sk-circle3 sk-circle"></div><div class="sk-circle4 sk-circle"></div><div class="sk-circle5 sk-circle"></div><div class="sk-circle6 sk-circle"></div>';
        arr+='<div class="sk-circle7 sk-circle"></div><div class="sk-circle8 sk-circle"></div><div class="sk-circle9 sk-circle"></div><div class="sk-circle10 sk-circle"></div><div class="sk-circle11 sk-circle"></div><div class="sk-circle12 sk-circle"></div>';
        $(this).append(arr);
    });
}