$(document).ready(function() { 
  $("#name_button").click(function() {  

var phone_number = $("input#phone_number").val();  
alert(dataString);
//alert (dataString);return false;  
      $.ajax({  
      type: "PUT",  
      url: "/users",
      data: dataString,
      success: function() {  
        $('#wine_form').html("<div id='message'></div>");  
        $('#message').html("<h2>Thanks! We have your favorite wine</h2>")  
        .hide()  
        .fadeIn(1500, function() {  
          $('#message').append("<p>Congrats!</p>");  
        });  
      }  
    });  
    return false;     
  });
});