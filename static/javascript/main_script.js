
var id_page_global=id_page_global;
function init(id_page_global2){
  id_page_global=id_page_global2;
  return id_page_global;
}


//array for template
function array_template_load_tutorials(result,i,number,id_page){
  var templates_array=[
    ["<a href='/tutorials_to_see?id_page="+result[i][5]+"&id_articol="+result[i][4]+"' class='list-group-item'><i class='material-icons sho_position_icon'>arrow_right_alt</i>"+result[i][1]+"</a>"],/*+result[i][0]+"."*/
    [result[i][3]],
    [result[i][6]]

  ];

  return templates_array[number];
}


function array_template_programming_language(result,i,number_template){
  var templates_array2=[
    ["<div class='col-lg-6'><div class='weather-card one'><img class='html5_back' src='"+result[i][3]+"'/><div class='top'><div class='wrapper'><div class='mynav'><a href='javascript:;'><span class='lnr lnr-chevron-left'></span></a><a href='javascript:;'><span class='lnr lnr-cog'></span></a></div><a href='http://localhost:5000/tutorials_to_see?id_page="+result[i][4]+"&id_articol="+result[i][5]+"'><h1 class='heading'>"+result[i][1]+"</h1><h3 class='location'>"+result[i][2]+"</h3></a></div></div><div class='bottom'><div class='wrapper'><ul class='forecast'><a href='javascript:;'><span class='lnr lnr-chevron-up go-up'></span></a><li class='active'><span class='date'>Yesterday</span><span class='lnr lnr-sun condition'><span class='temp'>23<span class='deg'>0</span><span class='temp-type'>C</span></span></span></li><li><span class='date'>Tomorrow</span><span class='lnr lnr-cloud condition'><span class='temp'>21<span class='deg'>0</span><span class='temp-type'>C</span></span></span></li></ul></div></div></div></div>"],
    ["<div class='col-md-3'><div class='ibox'><div class='ibox-content product-box'><div class=''><img class='style_for_photo' src='"+result[i][3]+"'/></div><div class='product-desc'><span class='product-price'>  $"+result[i][7]+"</span><small class='text-muted'> "+result[i][6]+"</small><a href='#' class='product-name'> "+result[i][1]+"</a><div class='small m-t-xs'>"+result[i][2]+"</div><div class='m-t text-righ'><a href='http://localhost:5000/tutorials_to_see?id_page="+result[i][4]+"&id_articol="+result[i][5]+"' class='btn btn-xs btn-outline btn-primary'>Info <i class='fa fa-long-arrow-right'></i> </a></div></div></div></div></div>"],
    ["<li class='list-group-item' data-toggle='modal' data-target='mymodal_lang'><a href='http://localhost:5000/tutorials_to_see?id_page="+result[i][4]+"&id_articol="+result[i][5]+"'><img src='"+result[i][3]+"' style='width:50px;height:50px;'><span style='margin-left:13px;font-size:22px;margin-top:14px;'>"+result[i][1]+"</span></a></li>"]
  ];
  return templates_array2[number_template];
}

function array_template_load_profiles(result,i,number_in_array){

  var array_options=[
    [1,result[i][1]],
    [2,result[i][2]],
    [3,result[i][3]],
    [4,result[i][4]],
    [5,result[i][5]],
    [6,result[i][6]],
    [7,result[i][7]],
    [8,result[i][8]]
  ]
  
  return array_options[number_in_array][1];
}


//ajax function to load data from the database

function load_programming_languages(show_the_tutorials,number_template)
{

  $.ajax({
    url: "/select_programming_languages",
    cache:false,
    success: function(result){

      for(i = 0; i < result.length; i++){

          $(show_the_tutorials).append( array_template_programming_language(result,i,number_template));
      }

      }

    });

}







function load_tutorials(id_page,id_articol,show_the_tutorials,number,condidtion_mysql)
{

  $.ajax({
    url: "/select_from_tutorials?id_page="+id_page+"&id_articol="+id_articol+"&condidtion_mysql="+condidtion_mysql,
    cache:false,
    success: function(result){
      console.log(result);
      console.log(id_page);
      for(i = 0; i < result.length; i++){

          $(show_the_tutorials).append( array_template_load_tutorials(result,i,number,id_page));//"<a href='/tutorials_to_see?id_page={{id1}}&id_articol="+result[i][4]+"' class='list-group-item'>"+result[i][0]+"."+result[i][1]+"</a>" );
      }

      }

    });

}


function extract_user_data(number,show_the_data,what_to_show){

  $.ajax({
    url:"/select_user_data",
    cache:false,
    success:function(result){
      for(i=0;i<=result.length;i++){
          if(what_to_show==1){
              $(show_the_data).replaceWith(array_template_load_profiles(result,i,number));
          }else{
              document.getElementById("avatar_image").src = array_template_load_profiles(result,i,number);
          }
        }
      }





  });
}


function search_data(){
  var search_field_data=$('#search_field_data').val();
  console.log(search_field_data);
  $.ajax({
    url:"/search_all?search_parameter="+search_field_data,
    cache:false,
    success:function(result){
      console.log(result);
      if(search_field_data>0){
        $(".show_down").css({"display":"inline"});
       for(var i=0;i<=result.length-1;i++)
        {
            $(".show_data__prima").preppend("<li class='list_search_all__'>"+result[0][1]+"</li>");
       }
   }


      }





  });


}
