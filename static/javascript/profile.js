select_user_data();
function select_user_data(){
  $.ajax({
    url:"/select_data_post_tutorias",
    cache:false,
    success:function(result){
      console.log(result);

   }

  });
}
