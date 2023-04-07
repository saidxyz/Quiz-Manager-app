jQuery(document).ready(function(){
jQuery(document).on("click","a.previous",function(){
    var a = jQuery(".question-item.active").prev();
  
    if(a.hasClass("question-item")){
        jQuery(".question-item.active").removeClass("active");
        a.addClass("active");
    }
})
jQuery(document).on("click","a.next",function(){
    var a = jQuery(".question-item.active").next();
    
    if(a.hasClass("question-item")){
        jQuery(".question-item.active").removeClass("active");
        a.addClass("active");
    }else{
        jQuery(".question-list").hide();
        jQuery(".submit-your-quiz").show();
    }
})


})