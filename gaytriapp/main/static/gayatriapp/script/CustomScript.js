$(document).ready(function(){
    $(".addbtn").click(function(){
        $.ajax({
            url: "/samples/",
            success: function(data){
                $('#addcontent').text(data.message);
            }
        });
    });

});


