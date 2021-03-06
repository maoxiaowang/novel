/** csrf */
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = $.cookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  }
);


/** string format */
String.prototype.format = function () {
  var values = arguments;
  return this.replace(/{(\d+)}/g, function (match, index) {
    if (values.length > index) {
      return values[index];
    } else {
      return "";
    }
  });
};


/** Reconnecting Websocket */
!function (a, b) {
  "function" == typeof define && define.amd ? define([], b) : "undefined" != typeof module && module.exports ? module.exports = b() : a.ReconnectingWebSocket = b()
}(this, function () {
  function a(b, c, d) {
    function l(a, b) {
      var c = document.createEvent("CustomEvent");
      return c.initCustomEvent(a, !1, !1, b), c
    }

    var e = {
      debug: !1,
      automaticOpen: !0,
      reconnectInterval: 1e3,
      maxReconnectInterval: 3e4,
      reconnectDecay: 1.5,
      timeoutInterval: 2e3
    };
    d || (d = {});
    for (var f in e) this[f] = "undefined" != typeof d[f] ? d[f] : e[f];
    this.url = b, this.reconnectAttempts = 0, this.readyState = WebSocket.CONNECTING, this.protocol = null;
    var h, g = this, i = !1, j = !1, k = document.createElement("div");
    k.addEventListener("open", function (a) {
      g.onopen(a)
    }), k.addEventListener("close", function (a) {
      g.onclose(a)
    }), k.addEventListener("connecting", function (a) {
      g.onconnecting(a)
    }), k.addEventListener("message", function (a) {
      g.onmessage(a)
    }), k.addEventListener("error", function (a) {
      g.onerror(a)
    }), this.addEventListener = k.addEventListener.bind(k), this.removeEventListener = k.removeEventListener.bind(k), this.dispatchEvent = k.dispatchEvent.bind(k), this.open = function (b) {
      h = new WebSocket(g.url, c || []), b || k.dispatchEvent(l("connecting")), (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "attempt-connect", g.url);
      var d = h, e = setTimeout(function () {
        (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "connection-timeout", g.url), j = !0, d.close(), j = !1
      }, g.timeoutInterval);
      h.onopen = function () {
        clearTimeout(e), (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "onopen", g.url), g.protocol = h.protocol, g.readyState = WebSocket.OPEN, g.reconnectAttempts = 0;
        var d = l("open");
        d.isReconnect = b, b = !1, k.dispatchEvent(d)
      }, h.onclose = function (c) {
        if (clearTimeout(e), h = null, i) g.readyState = WebSocket.CLOSED, k.dispatchEvent(l("close")); else {
          g.readyState = WebSocket.CONNECTING;
          var d = l("connecting");
          d.code = c.code, d.reason = c.reason, d.wasClean = c.wasClean, k.dispatchEvent(d), b || j || ((g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "onclose", g.url), k.dispatchEvent(l("close")));
          var e = g.reconnectInterval * Math.pow(g.reconnectDecay, g.reconnectAttempts);
          setTimeout(function () {
            g.reconnectAttempts++, g.open(!0)
          }, e > g.maxReconnectInterval ? g.maxReconnectInterval : e)
        }
      }, h.onmessage = function (b) {
        (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "onmessage", g.url, b.data);
        var c = l("message");
        c.data = b.data, k.dispatchEvent(c)
      }, h.onerror = function (b) {
        (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "onerror", g.url, b), k.dispatchEvent(l("error"))
      }
    }, 1 == this.automaticOpen && this.open(!1), this.send = function (b) {
      if (h) return (g.debug || a.debugAll) && console.debug("ReconnectingWebSocket", "send", g.url, b), h.send(b);
      throw"INVALID_STATE_ERR : Pausing to reconnect websocket"
    }, this.close = function (a, b) {
      "undefined" == typeof a && (a = 1e3), i = !0, h && h.close(a, b)
    }, this.refresh = function () {
      h && h.close()
    }
  }

  return a.prototype.onopen = function () {
  }, a.prototype.onclose = function () {
  }, a.prototype.onconnecting = function () {
  }, a.prototype.onmessage = function () {
  }, a.prototype.onerror = function () {
  }, a.debugAll = !1, a.CONNECTING = WebSocket.CONNECTING, a.OPEN = WebSocket.OPEN, a.CLOSING = WebSocket.CLOSING, a.CLOSED = WebSocket.CLOSED, a
});


/** blockUI */
// let blockUIOptions = {
//   message: '<div class="spinner-border avatar-sm text-primary m-2" role="status"></div>',
//   centerX: true, // <-- only effects element blocking (page block controlled via css above)
//   centerY: true,
//   overlayCSS: {
//     backgroundColor: '#000',
//     opacity: 0.25,
//     // cursor: 'wait'
//     display: 'block',
//     'z-index': 1000
//   },
//   css: {
//     padding: 0,
//     margin: 0,
//     width: '30%',
//     top: '40%',
//     left: '35%',
//     textAlign: 'center',
//     // color: '#000',
//     // border: '3px solid #aaa',
//     // backgroundColor: '#fff',
//     // cursor: 'wait'
//   },
//   fadeIn: 200,
//   fadeOut: 400,
// };
// $.blockUI.defaults = blockUIOptions;

$.extend($.validator.messages, {
  required: '这个字段是必填项',
  remote: '请修复这个字段',
  email: '请输入一个正确的电子邮件地址',
  url: '请输入一个正确的URL地址',
  date: '请输入一个正确的日期',
  dateISO: '请输入一个正确的日期( ISO )',
  number: '请输入一个可用的数字',
  digits: '请输入纯数字',
  //creditcard: gettext('Please enter a valid credit card number.'),
  equalTo: '确保输入相同的值',
  maxlength: $.validator.format('请输入最多{0}个字符'),
  minlength: $.validator.format('请输入最少{0}个字符'),
  rangelength: $.validator.format('请输入介于{0}到{1}长度之间的字符'),
  //range: $.validator.format(gettext('Please enter a value between {0} and {1}.')),
  max: $.validator.format('请输入不超过{0}的值'),
  min: $.validator.format('请输入不小于{0}的值')
});
$.each($('form'), function (i, item) {
  let $form = $(item);
  let validator = $form.validate({
    errorPlacement: function (error, element) {
      error.appendTo(element.parent().parent())
    },
    errorClass: 'errorlist d-block'
  });
  $form.submit(function (e) {
    // validate
    if (!validator.form()) {
      return false
    }
  })
});
