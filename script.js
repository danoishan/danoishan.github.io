document.querySelectorAll('[data-year]').forEach((el)=>{el.textContent=new Date().getFullYear();});
const header=document.querySelector('.site-header');
const setHeader=()=>{if(header)header.classList.toggle('scrolled',window.scrollY>16)};
setHeader();window.addEventListener('scroll',setHeader,{passive:true});
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduced||!('IntersectionObserver'in window)){document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));}else{const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}})},{threshold:.08,rootMargin:'0px 0px -30px 0px'});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));}
