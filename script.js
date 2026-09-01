document.querySelectorAll('[data-year]').forEach((el)=>{el.textContent=new Date().getFullYear();});

const root=document.documentElement;
const themeMeta=document.querySelector('meta[name="theme-color"]');
const savedTheme=localStorage.getItem('portfolio-theme');
const systemDark=window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme=savedTheme||(systemDark?'dark':'light');

function applyTheme(theme){
  root.dataset.theme=theme;
  root.style.colorScheme=theme;
  if(themeMeta)themeMeta.setAttribute('content',theme==='dark'?'#111315':'#f3f0e8');
  document.querySelectorAll('[data-theme-toggle]').forEach((button)=>{
    const dark=theme==='dark';
    button.textContent=dark?'☀︎':'◐';
    button.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');
    button.setAttribute('title',dark?'Light mode':'Dark mode');
  });
}

applyTheme(initialTheme);

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
    localStorage.setItem('portfolio-theme',next);
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
const setHeader=()=>{if(header)header.classList.toggle('scrolled',window.scrollY>16)};
setHeader();
window.addEventListener('scroll',setHeader,{passive:true});

const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduced||!('IntersectionObserver'in window)){
  document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));
}else{
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}
    });
  },{threshold:.08,rootMargin:'0px 0px -30px 0px'});
  document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
}
