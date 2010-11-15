// site
function ajaxResponseInfo(basename, status, xhr, data, where) {
  if (xhr) {
    status += ':' + xhr.readyState + ':' + xhr.status;
    if (xhr.statusText)
      status += ':' + xhr.statusText;
    if (xhr.responseText && !(xhr.statusText && xhr.responseText.contains(xhr.statusText))) 
      status += ':' + xhr.responseText;
    }
  if (data)
    status += ':' + data;
  if (where)
    status = where + '.' + status;
  return basename + '.' + status;
};

// extending older JS runtimes with native methods

if (!Array.prototype.forEach)
{
  Array.prototype.forEach = function(fun /*, thisp */)
  {
    "use strict";

    if (this === void 0 || this === null)
      throw new TypeError();

    var t = Object(this);
    var len = t.length >>> 0;
    if (typeof fun !== "function")
      throw new TypeError();

    var thisp = arguments[1];
    for (var i = 0; i < len; i++)
    {
      if (i in t)
        fun.call(thisp, t[i], i, t);
    }
  };
}

// ======================= actual game =======================


var id = '';

var login = $('#login');
var question = $('#question');

var header = $('#question strong');
var answers = $('#question ul');
var combatants = $('#question .combatants');

$(document).ready(function() {
	
	$('#login').bind('submit',function(e) {
		var nick = $('#nick').dom[0].value;
		if (!nick) window.alert('Please enter your nickname!');
		else {
			$.post('/login/'+nick, function(data) { data = JSON.parse(data); id = data.session; getQuestion(); });
			e.preventDefault();
		}
		return false;
	});

});

function render(data) {
	header.html(data.question);
	var html='';
	data.answers.forEach(function(item, offset) {
		html+='<li><a href="#">'+offset+': '+item+'</a></li>';
	});
	answers.html(html);
	html='';
	data.combatants.forEach(function(item, offset) {
		html+='<li>'+item.name+'</li>';
	});
	combatants.html(html);
};

function getQuestion() {
	$.post('/question/'+id, function(data) {
		data = JSON.parse(data);
        login.hide();
        question.show();
		render(data);
	});
}