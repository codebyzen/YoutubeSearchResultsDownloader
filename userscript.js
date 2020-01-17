// ==UserScript==
// @name       Youtube Link Collector
// @namespace  http://tampermonkey.net/
// @version    0.1
// @description  Copy Links from YouTube search
// @include    /https?:\/\/*/
// @copyright  2020+, DSD&A
// @grant      unsafeWindow
// @grant      GM_registerMenuCommand
// @run-at     document-end
// ==/UserScript==

GM_registerMenuCommand('Run this now', function() {
    main_func()
}, 'r');


function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    }

function main_func() {
    var yj = [];
    var old_ytp_div = document.querySelector('#ytp_div');
    if (old_ytp_div !== null) old_ytp_div.remove();
    document.querySelectorAll('a#video-title').forEach(item=>{
        yj.push(item);
    });
    download('list.txt',yj.join("\n"));
}