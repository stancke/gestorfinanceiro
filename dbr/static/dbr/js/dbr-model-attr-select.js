(function ($) {

    // Based in http://hceint.wordpress.com/2011/04/09/hiding-option-groups-optgroups-in-chrome-and-internet-explorer-with-jquery/
    $.fn.hideOptionGroup = function() {
	$(this).hide();
	$(this).children().each(function(){
	    $(this)
		.attr("disabled", true)
//		.attr("selected", false)
		.hide();
	});
	$(this).appendTo($(this).parent());
    };
    
    $.fn.showOptionGroup = function() {
	$(this).show();    
	$(this).children().each(function(){
	    $(this).attr("disabled", false).show();
	});
	$(this).prependTo($(this).parent());
    };

     var update_selects = function(model_name) {
	 // Deactivate all selects and hide all options
	 $(".dbr-model-attr").attr("disabled", true)
	     .attr("title", "Please choose a model before setting this option");
	 $(".dbr-model-attr optgroup").each(function (index) {
	     $(this).hideOptionGroup();
	 });
	 if (model_name) {
	     var model_name_label = model_name.split(".")[1];
	     // Show options that match the model label and activate the selects
	     $(".dbr-model-attr optgroup[label=" + model_name_label + "]")
		 .each(function (index) {
		     $(this).showOptionGroup();
		 });
	     $(".dbr-model-attr").attr("disabled", false)
		 .attr("title", "");
	 };
     };

     $(function () {
	   // Bind the change event in the model select to the field selects updater
	   $("#id_model").change(
	       function () {
		   update_selects($(this).val());
	       }
	   );

	   // Handle the addition of new inlines using livequery (https://github.com/brandonaaron/livequery)
	   // It's currently not working due to errors with livequery
	   // $(".add-row a").livequery(
	   //     'click',
	   //     update_selects($("#id_model").val())
	   // );

	   // Fire the event when the document is loaded to handle edition of existant reports
	   $("#id_model").change();
       });
 })(django.jQuery);