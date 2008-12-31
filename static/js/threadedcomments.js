function show_reply_form(comment_id, url, person_name) {
    var comment_reply = $('#' + comment_id);
    var to_add = $( new Array(
    '<div class="response"><h4>Reply to ' + person_name + '</h4>',
    '<form method="POST" action="' + url + '" class="replyform">',
    '<p><label for="id_name">Name</label> <input id="id_name" type="text" name="name" maxlength="128"></p>',
    '<p><label for="id_website">Website (optional)</label> <input id="id_website" type="text" name="website" maxlength="200"></p>',
    '<p><label for="id_email">E-mail (optional)</label> <input id="id_email" type="text" name="email" maxlength="75"></p>',
    '<p><label for="id_comment">Comment</label> <textarea id="id_comment" rows="10" cols="40" name="comment"></textarea></p>',
    '<p><input type="submit" value="Submit Comment"></p>',
    '</form>', '</div>').join(''));
    to_add.css("display", "none");
    comment_reply.after(to_add);
    to_add.slideDown(function() {
        comment_reply.replaceWith(new Array('<a class="replylink" id="',
        comment_id,'" href="javascript:hide_reply_form(\'',
        comment_id, '\',\'', url, '\',\'', person_name,
        '\')">Stop Replying</a>').join(''));
    });
}
function hide_reply_form(comment_id, url, person_name) {
    var comment_reply = $('#' + comment_id);
    comment_reply.next().slideUp(function (){
        comment_reply.next('.response').remove();
        comment_reply.replaceWith(new Array('<a class="replylink" id="',
        comment_id,'" href="javascript:show_reply_form(\'',
        comment_id, '\',\'', url, '\',\'', person_name,
        '\')">Reply</a>').join(''));
    });
}