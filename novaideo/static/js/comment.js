
function related_item_template(item){
   var markup = '<div class="clearfix">' +
                '<div class="col-sm-1">'
   if(item.icon){
      markup += '<span class=\"search-icon '+item.icon+'\"></span>'
   };
   markup += '</div>'+
             '<div clas="col-sm-10">' +
               '<div class="clearfix">' +
                  '<div class="col-sm-3">' + item.text + '</div>';
   if (item.description) {
      markup += '<div class="col-sm-8">' + item.description + '</div>';
    };
   markup += '</div></div></div>';
   return markup
};



try {
    select2_ajac_templates['related_item_template'] = related_item_template;
}
catch(err) {
}

function get_data(selecteds){
    var selecteds = jQuery.makeArray(selecteds);
    var result= [];
    for(i=0;i<selecteds.length; i++){
       result[i] = selecteds[i].id
    };
    return result
};

function init_select_association(){
    $('.select-associations').click(function(){
        var comments = $($($($(this).parents('.comments-scroll').first()).find('ul.commentulorigin').first()).children().filter("li[data-association='false']"));
        if (this.checked) {
            comments.addClass('hide-bloc')            
        }else{
           comments.removeClass('hide-bloc')
        }
    });
};

function replays_show(element){
    var replays = $($($($(element).parents('li').first()).children('ul:not(.replay-bloc)')).children('li'));
    if($(element).hasClass('closed')){
       replays.slideDown( );
       $($(element).find('span').first()).attr('class', 'glyphicon glyphicon-chevron-up');
       $(element).addClass('opened');
       $(element).removeClass('closed');
       $($(element).find('.comment-replay-message-closed').first()).removeClass('hide-bloc');
       $($(element).find('.comment-replay-message-opened').first()).addClass('hide-bloc');
    }else{
       replays.splice(-1,1);
       replays.slideUp();
       $($(element).find('span').first()).attr('class', 'glyphicon glyphicon-chevron-down');
       $(element).addClass('closed');
       $(element).removeClass('opened');
       $($(element).find('.comment-replay-message-closed').first()).addClass('hide-bloc');
       $($(element).find('.comment-replay-message-opened').first()).removeClass('hide-bloc');
    }

};

//TODO to remove
function init_comment_scroll(){
  var last_child = $('.comments-scroll ul.commentulorigin > .commentli:last-child');
  if (last_child.length > 0){
      var top = last_child.offset().top - $('.comments-scroll').offset().top  + last_child.height() + 10;
      if (top < 700){
       $('.comments-scroll').height(top)
      }
  }else{
       $('.comments-scroll').height(100)
  }
};

function get_form_replay_container(){
  return '<div class=\"replay-form-container\">'+
            '<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>'+
          '</div>'
}

function update_replay(url){
    var toreplay = $(this).closest('.replay-action').data('toreplay');
    var target = $(this).closest('.replay-action').data('target')+'-replay';
    if (Boolean(toreplay)){$(target).parent('ul.replay-bloc').removeClass('hide-bloc'); return false}
    var url = $(this).closest('.replay-action').data('updateurl');
    $.getJSON(url,{tomerge:'True', coordinates:'main'}, function(data) {
       var action_body = data['body'];
       if (action_body){
           $($(target).find('.media-body').first()).html(get_form_replay_container());
           var container = $($(target).find('.replay-form-container').first());
           container.append($(action_body));
           var replay_bloc = $($(target).parents('ul.replay-bloc').first());
           $(container.find('button.close').first()).on('click', function(){
              replay_bloc.css('display', 'none');
           });
           replay_bloc.slideDown()
           try {
                deform.processCallbacks();
            }
           catch(err) {};
        }else{
           location.reload();
           return false
        }
    });
    return false;
};


$(document).ready(function(){
    init_select_association();

    $(document).on('click', '.replay-action', update_replay);

    $(document).on('submit','.commentform', function( event ) {
        var button = $(this).find('button').last();
        var intention = $(this).find("select[name=\'intention\']").select2('val');
        var select_related_contents = $($(this).find("select[name='related_contents']").first());
        var related_contents = get_data(select_related_contents.select2('val'));
        var textarea = $(this).find('textarea');
        var comment = textarea.val();
        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.comments-scroll');
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var progress = parent.find('#progress');
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(button).addClass('disabled');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var values = $(this).serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 var content = $(data).find('.comments-scroll');
                 if (content){
                   var label = $($(content).parents(".panel").first()).find('.panel-heading span.action-message').html();
                   $($(target).parents(".panel").first()).find('.panel-heading span.action-message').html(label);
                   $(target).html($(content).html());
                   $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                   textarea.val('');
                   select_related_contents.parents('.controled-form').first().addClass('hide-bloc');
                   $($(select_related_contents.parents('.controled-form').first()).find("input[name='associate']").first()).prop('checked', false);
                   select_related_contents.select2('val', []);
                   init_select_association();
                  }else{
                     location.reload();
                     return false
                  };
                  $(button).removeClass('disabled');
              });
              progress.hide();
        }else{
           var errormessage = '';
           if (intention == ''){
               errormessage =  "intention";
           };
           if (comment == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
       event.preventDefault();
   });
  


    $('.commentform .control-form-button').on('click', function(event){
        var form = $($(this).parents('.ajax-form').find(".controled-form").first());
        var associate = $(form.find("input[name='associate']").first());
        if(!form.hasClass('hide-bloc')){
            associate.prop('checked', true)
        }else{
            associate.prop('checked', false)
        }
    });

    $(document).on('submit','.respondform', function( event ) {
        var formid = $(this).attr('id');
        var button = $(this).find('button')

        var intention = $(this).find("select[name=\'intention\']").select2('val');
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').get(1));
        var modal = $(parent).find('.modal.fade:has(form[id|=\''+formid+'\'])');
        var parentform = parent.find('.commentform');
        var urlparent = $(parentform).data('url');

        var target = parent.find('.comments-scroll');
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var progress = parent.find('#progress');
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(modal).modal('hide');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var values = $(this).serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                 $.post(urlparent, {}, function(data) {
                      var content = $(data).find('.comments-scroll');
                      if (content){
                         $(target).html($(content).html());
                         init_select_association();
                      }else{
                         location.reload();
                         return false
                       };
                     });
                 });
                 progress.hide();
        }else{
           var errormessage = '';
           if (intention == ''){
               errormessage =  "intention";
           };
           if (comment == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
      event.preventDefault();
   });

});
