// lab-1.0.3.min.js
// http://labjs.com/
// https://github.com/getify/LABjs
(function(p){var q="string",w="head",H="body",Y="script",t="readyState",j="preloaddone",x="loadtrigger",I="srcuri",C="preload",Z="complete",y="done",z="which",J="preserve",D="onreadystatechange",ba="onload",K="hasOwnProperty",bb="script/cache",L="[object ",bv=L+"Function]",bw=L+"Array]",e=null,h=true,i=false,n=p.document,bx=p.location,bc=p.ActiveXObject,A=p.setTimeout,bd=p.clearTimeout,M=function(a){return n.getElementsByTagName(a)},N=Object.prototype.toString,O=function(){},r={},P={},be=/^[^?#]*\//.exec(bx.href)[0],bf=/^\w+\:\/\/\/?[^\/]+/.exec(be)[0],by=M(Y),bg=p.opera&&N.call(p.opera)==L+"Opera]",bh=("MozAppearance"in n.documentElement.style),u={cache:!(bh||bg),order:bh||bg,xhr:h,dupe:h,base:"",which:w};u[J]=i;u[C]=h;r[w]=n.head||M(w);r[H]=M(H);function Q(a){return N.call(a)===bv}function R(a,b){var c=/^\w+\:\/\//,d;if(typeof a!=q)a="";if(typeof b!=q)b="";d=(c.test(a)?"":b)+a;return((c.test(d)?"":(d.charAt(0)==="/"?bf:be))+d)}function bz(a){return(R(a).indexOf(bf)===0)}function bA(a){var b,c=-1;while(b=by[++c]){if(typeof b.src==q&&a===R(b.src)&&b.type!==bb)return h}return i}function E(v,k){v=!(!v);if(k==e)k=u;var bi=i,B=v&&k[C],bj=B&&k.cache,F=B&&k.order,bk=B&&k.xhr,bB=k[J],bC=k.which,bD=k.base,bl=O,S=i,G,s=h,l={},T=[],U=e;B=bj||bk||F;function bm(a,b){if((a[t]&&a[t]!==Z&&a[t]!=="loaded")||b[y]){return i}a[ba]=a[D]=e;return h}function V(a,b,c){c=!(!c);if(!c&&!(bm(a,b)))return;b[y]=h;for(var d in l){if(l[K](d)&&!(l[d][y]))return}bi=h;bl()}function bn(a){if(Q(a[x])){a[x]();a[x]=e}}function bE(a,b){if(!bm(a,b))return;b[j]=h;A(function(){r[b[z]].removeChild(a);bn(b)},0)}function bF(a,b){if(a[t]===4){a[D]=O;b[j]=h;A(function(){bn(b)},0)}}function W(b,c,d,g,f,m){var o=b[z];A(function(){if("item"in r[o]){if(!r[o][0]){A(arguments.callee,25);return}r[o]=r[o][0]}var a=n.createElement(Y);if(typeof d==q)a.type=d;if(typeof g==q)a.charset=g;if(Q(f)){a[ba]=a[D]=function(){f(a,b)};a.src=c}r[o].insertBefore(a,(o===w?r[o].firstChild:e));if(typeof m==q){a.text=m;V(a,b,h)}},0)}function bo(a,b,c,d){P[a[I]]=h;W(a,b,c,d,V)}function bp(a,b,c,d){var g=arguments;if(s&&a[j]==e){a[j]=i;W(a,b,bb,d,bE)}else if(!s&&a[j]!=e&&!a[j]){a[x]=function(){bp.apply(e,g)}}else if(!s){bo.apply(e,g)}}function bq(a,b,c,d){var g=arguments,f;if(s&&a[j]==e){a[j]=i;f=a.xhr=(bc?new bc("Microsoft.XMLHTTP"):new p.XMLHttpRequest());f[D]=function(){bF(f,a)};f.open("GET",b);f.send("")}else if(!s&&a[j]!=e&&!a[j]){a[x]=function(){bq.apply(e,g)}}else if(!s){P[a[I]]=h;W(a,b,c,d,e,a.xhr.responseText);a.xhr=e}}function br(a){if(a.allowDup==e)a.allowDup=k.dupe;var b=a.src,c=a.type,d=a.charset,g=a.allowDup,f=R(b,bD),m,o=bz(f);if(typeof d!=q)d=e;g=!(!g);if(!g&&((P[f]!=e)||(s&&l[f])||bA(f))){if(l[f]!=e&&l[f][j]&&!l[f][y]&&o){V(e,l[f],h)}return}if(l[f]==e)l[f]={};m=l[f];if(m[z]==e)m[z]=bC;m[y]=i;m[I]=f;S=h;if(!F&&bk&&o)bq(m,f,c,d);else if(!F&&bj)bp(m,f,c,d);else bo(m,f,c,d)}function bs(a){T.push(a)}function X(a){if(v&&!F)bs(a);if(!v||B)a()}function bt(a){var b=[],c;for(c=-1;++c<a.length;){if(N.call(a[c])===bw)b=b.concat(bt(a[c]));else b[b.length]=a[c]}return b}G={script:function(){bd(U);var a=bt(arguments),b=G,c;if(bB){for(c=-1;++c<a.length;){if(c===0){X(function(){br((typeof a[0]==q)?{src:a[0]}:a[0])})}else b=b.script(a[c]);b=b.wait()}}else{X(function(){for(c=-1;++c<a.length;){br((typeof a[c]==q)?{src:a[c]}:a[c])}})}U=A(function(){s=i},5);return b},wait:function(a){bd(U);s=i;if(!Q(a))a=O;var b=E(h,k),c=b.trigger,d=function(){try{a()}catch(err){}c()};delete b.trigger;var g=function(){if(S&&!bi)bl=d;else d()};if(v&&!S)bs(g);else X(g);return b}};if(v){G.trigger=function(){var a,b=-1;while(a=T[++b])a();T=[]}}return G}function bu(a){var b,c={},d={"UseCachePreload":"cache","UseLocalXHR":"xhr","UsePreloading":C,"AlwaysPreserveOrder":J,"AllowDuplicates":"dupe"},g={"AppendTo":z,"BasePath":"base"};for(b in d)g[b]=d[b];c.order=!(!u.order);for(b in g){if(g[K](b)&&u[g[b]]!=e)c[g[b]]=(a[b]!=e)?a[b]:u[g[b]]}for(b in d){if(d[K](b))c[d[b]]=!(!c[d[b]])}if(!c[C])c.cache=c.order=c.xhr=i;c.which=(c.which===w||c.which===H)?c.which:w;return c}p.$LAB={setGlobalDefaults:function(a){u=bu(a)},setOptions:function(a){return E(i,bu(a))},script:function(){return E().script.apply(e,arguments)},wait:function(){return E().wait.apply(e,arguments)}};(function(a,b,c){if(n[t]==e&&n[a]){n[t]="loading";n[a](b,c=function(){n.removeEventListener(b,c,i);n[t]=Z},i)}})("addEventListener","DOMContentLoaded")})(window); 

// detectmobilebrowser-20100630.js
// http://detectmobilebrowser.com/
(function(global, agent){global.is_mobile=/android|avantgo|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-/i.test(agent.substr(0,4))})(window, navigator.userAgent||navigator.vendor||window.opera);

// http://happyworm.com/blog/tag/labjs/
// http://msdn.microsoft.com/en-us/scriptjunkie/ff943568.aspx

// google cdn: http://code.google.com/apis/libraries/
// microsoft cdn: http://code.google.com/apis/libraries/

// jquery 1.4.2 cdn: //ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js
// jquery 1.4.3 cdn: //ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js
// jquery 1.4.4 cdn: //ajax.microsoft.com/ajax/jQuery/jquery-1.4.4.min.js # beware ms cookies
// jquery ui 1.8.6 cdn: //ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js
// jquery mobile 1.0a2 js cdn: //code.jquery.com/mobile/1.0a2/jquery.mobile-1.0a2.min.js # non-matching ssl certificate

$LAB.setGlobalDefaults({BasePath:'/js/'});

$LAB.cdn = function(LAB, cdn, local, loaded){return LAB.script(cdn).wait(function(){
  if (!loaded()) LAB.script(local).wait();});}

var L = $LAB

if (jQuery.browser.mobile)
  L = L
  .script('zepto-0.1.1.min.js').wait()
  .script('jquery.mobile-1.0a2.min.js')
  .script('/css/jquery.mobile-1.0a2.min.css')
  ;
else
  L = L
  .cdn('//ajax.microsoft.com/ajax/jQuery/jquery-1.4.4.min.js', 'jquery-1.4.4.min.js', function(){return (typeof window.jQuery !== 'undefined');})
  .cdn('//ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js', 'jquery-ui-1.8.6.custom.min.js', function(){return (typeof window.jQuery.ui !== 'undefined');})
  .script('/css/jquery-ui-1.8.6.custom.css')
  ;

// L = L.wait()
// .script('jquery-form-2.45.min.js')
// .script('validate-1.7.min')
// ;


// http://paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
// usage: log('inside coolFunc',this,arguments);
window.log = function(){
  log.history = log.history || []; 
  log.history.push(arguments);
  if (this.console) console.log(Array.prototype.slice.call(arguments));
  };

// site

String.prototype.contains = function(s, t) { return (s.indexOf(t) != -1); };
String.prototype.startswith = function(s, t) { return (s.indexOf(t) == 0); };
String.prototype.endswith = function(s, t) { return (s.lastIndexOf(t) == s.length - t.length); };

function htmlReplace(selector, regexp, replacement, ifempty, safe) {
  try {
    $(selector).html(function(i, html) {
      return html ? html.replace(regexp, replacement) : (ifempty ? ifempty : replacement);
      });
  } catch(e) {
    if (! safe) throw e;
    }
  };

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

/*
$(document).ready(function(){

  });
*/