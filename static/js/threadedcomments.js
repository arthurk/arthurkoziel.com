function show_reply_form(comment_id, url, person_name) {
    var comment_reply = $('#' + comment_id);
    var to_add = $( new Array(
    '<div class="response">',
    '<form method="POST" action="' + url + '">',
    '<fieldset><legend>Reply to ' + person_name + '</legend>',
    '<p><label for="id_name">Name</label><br><input id="id_name" type="text" name="name" maxlength="128" class="text"></p>',    
    '<div class="span-2">',
      '<label for="id_email">E-mail<br><span class="quiet">(optional)</span></label>',
    '</div>',
    '<div class="span-5 last">',
      '<input id="id_email" type="text" name="email" maxlength="75" class="text">',
    '</div>',
    '<hr class="space">',
    '<div class="span-2">',
      '<label for="id_website">Website <br><span class="quiet">(optional)</span></label>',
    '</div>',
    '<div class="span-5 last">',
      '<input id="id_website" type="text" name="website" maxlength="200" class="text">',
    '</div>',
    '<hr class="space">',
    '<p><label for="id_comment">Comment (<a href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> enabled)</label><br><textarea id="id_comment" rows="10" cols="40" name="comment"></textarea></p>',
    '<p><input type="submit" value="Submit"></p>',
    '</fieldset>',
    '</form>', 
    '</div>').join(''));
    to_add.css("display", "none");
    comment_reply.after(to_add);
    to_add.slideDown("fast", function() {
        comment_reply.replaceWith(new Array('<a id="',
        comment_id,'" href="javascript:hide_reply_form(\'',
        comment_id, '\',\'', url, '\',\'', person_name,
        '\')">Stop Replying</a>').join(''));
    });
}
function hide_reply_form(comment_id, url, person_name) {
    var comment_reply = $('#' + comment_id);
    comment_reply.next().slideUp("fast", function (){
        comment_reply.next('.response').remove();
        comment_reply.replaceWith(new Array('<a id="',
        comment_id,'" href="javascript:show_reply_form(\'',
        comment_id, '\',\'', url, '\',\'', person_name,
        '\')">Reply to this comment</a>').join(''));
    });
}