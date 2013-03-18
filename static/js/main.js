$(document).ready(function () {
  $('nav li a').click(function () {
	$('li.sibling ul').slideUp('normal');	
	$(this).next().slideDown('normal');
  });
  
  $("li.sibling ul").hide();

});
