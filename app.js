'use strict';
const search=document.querySelector('#search'), evidence=document.querySelector('#evidence');
function filter(){const q=search.value.toLowerCase().trim();let count=0;document.querySelectorAll('tbody tr').forEach(row=>{row.hidden=!(row.dataset.search.includes(q)&&(!evidence.value||row.dataset.status===evidence.value));if(!row.hidden)count++;});document.querySelector('#result-count').textContent=count+' entries';document.querySelector('#empty').hidden=count>0;}
if(search){search.addEventListener('input',filter);evidence.addEventListener('change',filter);filter();}
