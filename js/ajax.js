var ENTER_KEY = 13;
var READY_STATE_COMPLETE = 4;
var HTTP_STATUS_OK = 200;

function makeAjaxCall(args, opt_callback) {
  var rpcUrl = '/ajax';
  var params = [];
  for (var key in args) {
    params.push(encodeURIComponent(key) + '=' + encodeURIComponent(args[key]));
  }

  var req = new XMLHttpRequest();
  req.open('POST', rpcUrl, true);
  req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  if (opt_callback) {
    req.onreadystatechange = function() {
      if (req.readyState == READY_STATE_COMPLETE &&
          req.status == HTTP_STATUS_OK) {
        opt_callback(req.responseText);
      }
    };
  }
  req.send(params.join('&'));
}

function textKeyPress(e) {
  if (e.keyCode == ENTER_KEY) {
    postRemark();
  }
}

function postRemark() {
  var remark = document.getElementById('remark-input').value.trim();
  document.getElementById('remark-input').value = '';

  if (!remark) {
    return;
  }

  makeAjaxCall({'remark': remark, 'action': 'post'});
}

function poll() {
  var writeRemarks = function(response) {
    var chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML += response;
    chatWindow.scrollTop = chatWindow.scrollHeight; 

    setTimeout(poll, 500);
  };

  makeAjaxCall({'action': 'read'}, writeRemarks);
}
