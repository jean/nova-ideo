function get_data(select){
    var i=0;
    var data = []
    $(select).find("option").each(function()
    {
        // log the value and text of each option
        data.push({'id': $(this).val(), 'text': $(this).text()});
    });

    return data
}


/* init items: start*/
function get_values(items){
    var values = {}
    var items = item.find('.controllable-item');
    for(i in items){
       var item = $($(items[i]).find('.actions').first())
       var oid = item.data('id');
       var title = item.data('title')
       values[oid] = title             
    };
    return values
}


function get_selecteds(select){
    var values = {}
    var selected_values = select.select2('val')
    var datas = get_data(select)
    for(i in selected_values){
       values[i] = datas[i]             
    };
    return values
}


function init_values(){
  var related_ideas = $('div.controllable-items');
  for (c in related_ideas){
      var targetform =  $('#'+$(related_ideas[c]).data('target'));
      var target = $(targetform.find('.controlled-items'));
      var selected_values = get_selecteds(target)
      for (v in selected_values){
          $(related_ideas[c]).append(get_tag(v, selected_values[v], '', ''));
      }
      var values = get_values($(related_ideas[c]))
  }

};

/* init items: end*/


function get_tag(oid, title, body, disabled){
    return "<div class=\"panel controllable-item\">"+
        "<div class=\"panel-heading\">"+
        "<a  href=\"#panel-element-"+oid+"\" data-parent=\"#panel-controllableitems\" data-toggle=\"collapse\" class=\"panel-title\">"+
        "<span class=\"glyphicon glyphicon-plus\"> </span>  "+title+"</a>"+
        "<span class=\"actions pull-right\" data-id=\""+oid+"\">"+
        "<span title=\"Retirer de la liste\" class=\""+disabled+"del-item\"></span></span></div>"+
        "<div class=\"panel-collapse collapse\" id=\"panel-element-"+oid+"\" style=\"height: auto;\">"+
        "<div class=\"panel-body\">"+body+"</div></div></div>"
}

function init_delitem(){
  $('.del-item').on('click', function(){
      var controllable = $($(this).parents('.controllable-items').first());
      var targetform =  $('#'+controllable.data('target'));
      var target = $(targetform.find('.controlled-items'));
      var itemtodel = $($(this).parents('.actions').first()).data('id');
      var event = jQuery.Event( "delItem" );
      $(this).parents('.controllable-item').first().remove();
      event.itemid = itemtodel;
      target.trigger(event);
      last_items = controllable.find(('.controllable-item')); 
      if (last_items.length == 1){
          var last = $($(last_items[0]).find('.del-item'));
          last.removeClass('del-item');
          last.addClass('disabled-del-item');
          last.unbind("click")
      }
  });
};


$(document).ready(function(){
  init_delitem();
  $('.controlled-items').on('delItem', function(event){
        var todel = -1;
        var selected_values = $(this).select2('val');
        for( o in selected_values)
        {
          if(selected_values[o] == event.itemid){todel=selected_values[o]}
         };
        if (todel != -1){
          new_selected_values = jQuery.grep(selected_values, function(value) {
             return value != todel;
          });
          $(this).select2('val', new_selected_values);
        }
  });

  $('.controlled-items').on('AddItem', function(event){
        var exists = false;
        var selected_values = $(this).select2('val');
        for( o in selected_values)
        {
          if(selected_values[o] == event.itemid){exists = true}
         };
        if (!exists){
            $(this).append($('<option>', {value: String(event.itemid), 
                                          text: event.itemtitle}));
        };
        var new_selected_values = selected_values;
        if (new_selected_values == null){
               new_selected_values = []
        };
        new_selected_values.push(String(event.itemid)); 
        $(this).select2("val", new_selected_values);
         
  });


   $('.new-idea-control').click(function(){
        var form = $($(this).parents('form').first());
        var select_field = $(form.find('select.search-idea-form').first());
        if (this.checked) {
            form.find('.new-idea-form').removeClass('hide-bloc');
            select_field.prop("disabled", true);         
        }else{
            form.find('.new-idea-form').addClass('hide-bloc');
            select_field.prop("disabled", false);
        }
    });



    $(document).on('click','.add-idea-form button.ajax-button', function( event ) {
        var button = $(this);
        var form = $(button.parents('form.add-idea-form').first());
        var ideas_managment = $($(form).parents('.panel-body').first());
        var related_ideas = $(ideas_managment.find('div.controllable-items'));
        var isnewidea = $(form.find('.new-idea-control'))[0].checked;
        var targetform =  $('#'+related_ideas.data('target'));
        var target = $(targetform.find('.controlled-items'));
        var danger_messages_container = $($(related_ideas.parents('div').first()).find('#messagedanger'));
        var dict_post = {};
        if (isnewidea)
         {
            newideaform = form.find('.new-idea-form');
            var title = newideaform.find('input[name="title"]').val();
            if (title=='')
            {
               danger_messages_container.text( novaideo_translate("The title is required!") ).show().fadeOut( 6000 );
               return
            }
            var text = newideaform.find('textarea[name="text"]').val();
            if (text=='')
            {
               danger_messages_container.text( novaideo_translate("The abstract is required!") ).show().fadeOut( 6000 );
               return
            }

            var keywords = $(newideaform.find('select[name="keywords"]')).select2('val');
            if (keywords.length == 0)
            {
               danger_messages_container.text( novaideo_translate("Keywords are required!")).show().fadeOut( 6000 );
               return
            }

            dict_post = {'title': title,
                         'text': text,
                         'keywords': keywords,
                         'op': 'creat_idea'};
         }else{
            oid = $($(form).find('select.search-idea-form')).select2('val');
            var new_items = related_ideas.find('span[data-id=\"'+oid+'\"]');
            if (new_items.length>0)
            {
               danger_messages_container.text( novaideo_translate("Idea already exist!") ).show().fadeOut( 6000 );
               return
            }
            if (oid == "")
            {
               danger_messages_container.text( novaideo_translate("Please select a valid idea!") ).show().fadeOut( 6000 );
               return
            }
            dict_post = {'oid': oid,
                         'op': 'get_idea'};
         };
         var url = $(form).data('url');
         button.addClass('disabled');
         $.get(url, dict_post, function(data) {
             if(data){
               button.removeClass('disabled'); 
               var event = jQuery.Event( "AddItem" );
               event.itemid = data['oid'];
               event.itemtitle = data['title'];
               target.trigger(event)
               var last_items = related_ideas.find(('.controllable-item'));
               var disabled_items =  related_ideas.find(('.disabled-del-item'));
               if (disabled_items.length >0){
                   var last = $($(disabled_items[0]));
                   last.removeClass('disabled-del-item');
                   last.addClass('del-item');
                }
               var items =  related_ideas.find(('.del-item'));
               if (items.length >0){
                  related_ideas.append(get_tag(data['oid'], data['title'], data['body'], ''));
                }else{
                   related_ideas.append(get_tag(data['oid'], data['title'], data['body'], 'disabled-'));
               }
               init_delitem();
               if (isnewidea){
                  newideaform.find('input[name="title"]').val('');
                  newideaform.find('textarea[name="text"]').val('');
                  $(newideaform.find('select[name="keywords"]')).select2('val', []);
               }else{
                 $($(form).find('select.search-idea-form')).select2('val', '')
               }
             }else{
                danger_messages_container.text( novaideo_translate("The idea is not added!") ).show().fadeOut( 6000 );
             }
        });
   });
});

//TODO ajout nouvel idee: il faut l'ajouter aux selects
