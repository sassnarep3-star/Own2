(function(){
  var q=document.getElementById('q'),fv=document.getElementById('fv'),fs=document.getElementById('fs'),cl=document.getElementById('claims'),cnt=document.getElementById('count');
  var rows=[].slice.call(document.querySelectorAll('table.t tbody tr[data-q]'));
  function apply(){
    var t=(q.value||'').toLowerCase().trim(),v=fv.value,s=fs.value,n=0;
    rows.forEach(function(r){
      var ok=(!t||r.getAttribute('data-q').indexOf(t)>-1)&&(!v||r.getAttribute('data-v')===v)&&(!s||r.getAttribute('data-s')===s);
      r.hidden=!ok; if(ok)n++;
    });
    cnt.textContent=n+' of '+rows.length+' shown';
  }
  [q,fv,fs].forEach(function(e){e.addEventListener('input',apply)});
  cl.addEventListener('change',function(){document.body.classList.toggle('show-claims',cl.checked)});
  if(location.hash){var el=document.getElementById(location.hash.slice(1));if(el&&el.hidden){q.value='';fv.value='';fs.value='';apply()}}
  apply();
})();
