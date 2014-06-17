/* Functions for handling asynchronous calls to the server. */

var ENTER_KEY = 13; // Int for determining if a key press was enter.
var HTTP_STATUS_OK = 200; // HTTP status code indicating that a load worked.
var READY_STATE_COMPLETE = 4; // Int for determining if an AJAX call is done.
var RPC_URL = '/ajax'; // Relative server path where AJAX call should be made.


/*
 * Makes an asynchronous call to the server with the given arguments. If
 * provided, opt_callback should be a function to be called if and when the
 * server call returns successfully.
 */
function makeAjaxCall(args, opt_callback) {
  // Make URL parameters from the provided argument dictionary.
  var params = [];
  for (var key in args) {
    params.push(encodeURIComponent(key) + '=' + encodeURIComponent(args[key]));
  }

  // Create a new AJAX request object.
  var req = new XMLHttpRequest();
  req.open('POST', RPC_URL, true);
  req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

  // If a callback function was provided, set it up to trigger when the call
  // returns succesfully.
  if (opt_callback) {
    req.onreadystatechange = function() {
      if (req.readyState == READY_STATE_COMPLETE &&
          req.status == HTTP_STATUS_OK) {
        opt_callback(req.responseText);
      }
    };
  }

  // Issue the AJAX request with the defined parameters.
  req.send(params.join('&'));
}


/*
 * Handle keyboard key presses, namely to make the enter key trigger posting a
 * remark.
 */
function textKeyPress(e) {
  if (e.keyCode == ENTER_KEY) {
    postRemark();
  }
}


/* Posts a remark to the server. */
function postRemark() {
  // Get the contents of the text entry field then empty it.
  var remark = document.getElementById('remark-input').value.trim();
  document.getElementById('remark-input').value = '';

  if (!remark) {
    return;
  }

  // Issue the AJAX request with the remark text and the right action key.
  makeAjaxCall({'remark': remark, 'action': 'post'});
}


/* Polls the server for new remarks. */
function poll() {
  // Create a callback function to be run when the remarks are returned.
  var writeRemarks = function(response) {
    // Get the chat window page element and append the response to it. The
    // response will already be formatted HTML.
    var chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML += response;

    // Scroll so that the most recent messages are in view.
    chatWindow.scrollTop = chatWindow.scrollHeight; 

    // Wait 500ms then poll the server again.
    setTimeout(poll, 500);
  };

  // Issue the AJAX request with the callback function and the right action key.
  makeAjaxCall({'action': 'read'}, writeRemarks);
}
