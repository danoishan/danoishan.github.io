document.querySelectorAll('[data-year]').forEach((el)=>{el.textContent=new Date().getFullYear();});

const root=document.documentElement;
const themeMeta=document.querySelector('meta[name="theme-color"]');
const getSavedTheme=()=>{try{return localStorage.getItem('portfolio-theme');}catch{return null;}};
const saveTheme=(theme)=>{try{localStorage.setItem('portfolio-theme',theme);}catch{}};
const systemDark=typeof window.matchMedia==='function'&&window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme=getSavedTheme()||(systemDark?'dark':'light');

function applyTheme(theme){
  const safeTheme=theme==='dark'?'dark':'light';
  root.dataset.theme=safeTheme;
  root.style.colorScheme=safeTheme;
  if(themeMeta)themeMeta.setAttribute('content',safeTheme==='dark'?'#111315':'#f3f0e8');
  document.querySelectorAll('[data-theme-toggle]').forEach((button)=>{
    const dark=safeTheme==='dark';
    button.textContent=dark?'☀︎':'◐';
    button.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');
    button.setAttribute('title',dark?'Light mode':'Dark mode');
    button.setAttribute('aria-pressed',String(dark));
  });
}

applyTheme(initialTheme);

document.querySelectorAll('.nav-links').forEach((nav)=>{
  if(!nav.hasAttribute('aria-label'))nav.setAttribute('aria-label','Primary navigation');
});

document.querySelectorAll('.nav').forEach((nav)=>{
  if(nav.querySelector('[data-theme-toggle]'))return;
  const button=document.createElement('button');
  button.type='button';
  button.className='theme-toggle';
  button.dataset.themeToggle='';
  const email=nav.querySelector('.nav-cta');
  if(email)nav.insertBefore(button,email);else nav.appendChild(button);
  button.addEventListener('click',()=>{
    const next=root.dataset.theme==='dark'?'light':'dark';
    saveTheme(next);
    applyTheme(next);
  });
});
applyTheme(root.dataset.theme||initialTheme);

const bestFitLabel=[...document.querySelectorAll('.section-head .label')].find((el)=>el.textContent.trim()==='Best fit');
if(bestFitLabel){
  const section=bestFitLabel.closest('.section');
  const actions=section?.querySelector('.hero-actions');
  if(section&&actions&&!section.querySelector('[data-adjacent-breadth]')){
    const row=document.createElement('div');
    row.className='quiet-row reveal';
    row.dataset.adjacentBreadth='';
    row.innerHTML='<span>Product roadmaps & prioritization</span><span>Brand, campaign & go-to-market support</span><span>Lifecycle & customer journey planning</span>';
    actions.parentNode.insertBefore(row,actions);
  }
}

const header=document.querySelector('.site-header');
const setHeader=()=>{if(header)header.classList.toggle('scrolled',window.scrollY>16);};
setHeader();
window.addEventListener('scroll',setHeader,{passive:true});

const reveals=[...document.querySelectorAll('.reveal')];
try{
  const reduced=typeof window.matchMedia==='function'&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced||!('IntersectionObserver' in window)){
    reveals.forEach((el)=>el.classList.add('visible'));
  }else{
    reveals.forEach((el)=>el.classList.add('reveal-pending'));
    const observer=new IntersectionObserver((entries)=>{
      entries.forEach((entry)=>{
        if(entry.isIntersecting){
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },{threshold:.08,rootMargin:'0px 0px -30px 0px'});
    reveals.forEach((el)=>observer.observe(el));
  }
}catch{
  reveals.forEach((el)=>{el.classList.remove('reveal-pending');el.classList.add('visible');});
}
