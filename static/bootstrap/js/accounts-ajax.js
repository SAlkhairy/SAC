$(document).ready(function() {

        // JQuery code to be added in here.
        $('#favourites').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/accounts/post_favourite/', {post_id: catid}, function(data){
               $('#favourite_count').html(data);
               $('#favourite').hide();
           });
});
