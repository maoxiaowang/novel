/**
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD
    define(['jquery'], factory);
  } else if (typeof exports === 'object') {
    // CommonJS
    factory(require('jquery'));
  } else {
    // Browser globals
    factory(jQuery);
  }
}(function ($) {

  var pluses = /\+/g;

  function encode(s) {
    return config.raw ? s : encodeURIComponent(s);
  }

  function decode(s) {
    return config.raw ? s : decodeURIComponent(s);
  }

  function stringifyCookieValue(value) {
    return encode(config.json ? JSON.stringify(value) : String(value));
  }

  function parseCookieValue(s) {
    if (s.indexOf('"') === 0) {
      // This is a quoted cookie as according to RFC2068, unescape...
      s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
    }

    try {
      // Replace server-side written pluses with spaces.
      // If we can't decode the cookie, ignore it, it's unusable.
      // If we can't parse the cookie, ignore it, it's unusable.
      s = decodeURIComponent(s.replace(pluses, ' '));
      return config.json ? JSON.parse(s) : s;
    } catch (e) {
    }
  }

  function read(s, converter) {
    var value = config.raw ? s : parseCookieValue(s);
    return $.isFunction(converter) ? converter(value) : value;
  }

  var config = $.cookie = function (key, value, options) {

    // Write

    if (value !== undefined && !$.isFunction(value)) {
      options = $.extend({}, config.defaults, options);

      if (typeof options.expires === 'number') {
        var days = options.expires, t = options.expires = new Date();
        t.setTime(+t + days * 864e+5);
      }

      return (document.cookie = [
        encode(key), '=', stringifyCookieValue(value),
        options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
        options.path ? '; path=' + options.path : '',
        options.domain ? '; domain=' + options.domain : '',
        options.secure ? '; secure' : ''
      ].join(''));
    }

    // Read

    var result = key ? undefined : {};

    // To prevent the for loop in the first place assign an empty array
    // in case there are no cookies at all. Also prevents odd result when
    // calling $.cookie().
    var cookies = document.cookie ? document.cookie.split('; ') : [];

    for (var i = 0, l = cookies.length; i < l; i++) {
      var parts = cookies[i].split('=');
      var name = decode(parts.shift());
      var cookie = parts.join('=');

      if (key && key === name) {
        // If second argument (value) is a function it's a converter...
        result = read(cookie, value);
        break;
      }

      // Prevent storing a cookie that we couldn't decode.
      if (!key && (cookie = read(cookie)) !== undefined) {
        result[name] = cookie;
      }
    }

    return result;
  };

  config.defaults = {};

  $.removeCookie = function (key, options) {
    if ($.cookie(key) === undefined) {
      return false;
    }

    // Must not alter options, thus extending a fresh object...
    $.cookie(key, '', $.extend({}, options, {expires: -1}));
    return !$.cookie(key);
  };

}));


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


/**
 * messages notify
 * */
let $messages = $('body > ul.messages');
if ($messages.length > 0) {
  setTimeout(function () {
    $.each($messages.find('li.message'), function (i, item) {
      let level = $(item).attr('data-level');
      let msg = $(item).text();
      notie.alert({ type: level, text: msg, time: 2 }) // Hides after 2 seconds
    });
  }, 100)

  // $messages.remove();
}

/**
 * ajax events
 */
let activeElement;
$(document).ajaxStart(
  function (e) {
    // blockTimeout = setTimeout($.blockUI, 300);
    try {
      activeElement = $(e.target.activeElement);
      // just a precautionary check
      if (!activeElement.hasClass('btn')) {
        return
      }
      activeElement.attr('disabled', true)
    } catch (ex) {
      console.log(ex);
    }
  }
).ajaxStop(
  function () {
    // clearTimeout(blockTimeout);
    // $.unblockUI();
    if (activeElement) {
      try {
        if (!activeElement.hasClass('btn')) {
          return
        }
        activeElement.removeAttr('disabled')
      } catch (ex) {
        console.log(ex);
      }
    }

  }
).ajaxSuccess(
  function (event, xhr, options) {
    if (xhr.responseJSON && options.type !== 'GET') {
      let res = xhr.responseJSON;
      if (!res.result) {
        $.each(res.messages, function () {
          let level = res.level;
          let msg = this;
          notie.alert({ type: level, text: msg, time: 2 })
        });
      }

    } else {

    }
  }
).ajaxError(
  function (event, xhr, options, exc) {
    let statusText = xhr.statusText;
    if (xhr.status === 0) {
      statusText = '已从服务器断开'
    }
    notie.alert({ type: 'error', text: statusText, time: 2 })
  }
);