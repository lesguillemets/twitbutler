(function(){
  window.addEventListener('load', emphCmd);
  
  function emphCmd(){
    var loc = window.location.href;
    if (/.*commands\.html#.*$/.test(loc)){
      var cmd = loc.split("#")[1];
      var cmdElm = document.getElementById(cmd);
      if (cmdElm !== null){
        cmdElm.style.backgroundColor = "#eeeeaa";
      }
    }
  }
})();
