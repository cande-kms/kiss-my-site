import gsap from 'gsap';

(function(){

  const panels   = gsap.utils.toArray('.panel');
  const dots      = gsap.utils.toArray('.dot');
  const navLinks  = gsap.utils.toArray('.nav-links a');
  const total     = panels.length;
  const kbHint    = document.getElementById('kbHint');

  let current = 0;
  let isAnimating = false;
  const DURATION = 0.6;           // section transition duration
  const LOCK_BUFFER = 60;         // ms after tween completes before we accept new input

  // ---------- initial layout ----------
  // place every panel off-stage except the first; panels stack with z-index by recency
  gsap.set(panels, { yPercent: (i) => i === 0 ? 0 : 100, zIndex: (i) => i === 0 ? 2 : 1 });

  // entrance animation for panel 0 content on load
  function introTimeline(panelEl){
    const contentBlock = panelEl.querySelector('.panel-content, .panel-content--logos');
    const fg = panelEl.querySelector('.panel-fg');
    const bg = panelEl.querySelector('.panel-bg .gradient');
    const pulseSpanEl = panelEl.querySelector('.pulse-line span');

    const tl = gsap.timeline({
      onComplete: () => {
        // same safety net as goTo(): guarantee the resting state regardless
        // of what happened during the tweens.
        if (contentBlock) gsap.set(contentBlock, { opacity:1, y:0 });
        if (fg) gsap.set(fg, { opacity:1, scale:1 });
        if (bg) gsap.set(bg, { opacity:1 });
        if (pulseSpanEl) gsap.set(pulseSpanEl, { left:'130%' });
      }
    });

    if (bg) tl.from(bg, { opacity:0, duration:1.1, ease:'power2.out' }, 0);
    if (fg) tl.from(fg, { opacity:0, scale:0.92, duration:0.9, ease:'power3.out' }, 0.05);
    if (contentBlock) tl.from(contentBlock, { opacity:0, y:24, duration:0.8, ease:'power3.out' }, 0.15);
    if (pulseSpanEl) tl.fromTo(pulseSpanEl, { left:'-30%' }, { left:'130%', duration:0.9, ease:'power2.inOut' }, 0.1);

    return tl;
  }

  introTimeline(panels[0]);
  updateUI(0);

  // ---------- ambient floating animation for client/partner logo chips ----------
  function startLogoFloat(){
    document.querySelectorAll('.logo-float').forEach((el, i) => {
      const amplitude = 5 + (i % 4) * 1.4;        // 5–9.2px of vertical drift
      const dir = i % 2 === 0 ? -1 : 1;
      gsap.to(el, {
        y: amplitude * dir,
        duration: 2.8 + (i % 6) * 0.35,            // 2.8–4.55s per half-cycle
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true,
        delay: (i % 9) * 0.18
      });
    });
  }
  startLogoFloat();

  // ---------- core transition ----------
  function goTo(index, direction){
    if (isAnimating) return;
    if (index < 0 || index > total - 1) return;
    if (index === current) return;

    isAnimating = true;
    document.body.classList.add('is-locking');

    const fromPanel = panels[current];
    const toPanel    = panels[index];
    const dir = direction || (index > current ? 1 : -1); // 1 = next (incoming from bottom), -1 = prev (incoming from top)

    // The whole text block (whichever shell this panel uses) animates as ONE
    // unit — not as a dozen individually-timed tweens. This is intentionally
    // simple: fewer moving parts means there's no fractional-offset timing
    // that can leave one element stranded mid-animation if anything ever
    // interrupts the timeline.
    const contentBlock = toPanel.querySelector('.panel-content, .panel-content--logos');
    const fg = toPanel.querySelector('.panel-fg');
    const bg = toPanel.querySelector('.panel-bg .gradient');
    const pulseSpan = toPanel.querySelector('.pulse-line span');

    // Kill any tween still running on anything we're about to touch, on both
    // the incoming and outgoing panel. Removes any chance of GSAP's
    // overwrite-management leaving a stale/partial tween in place.
    gsap.killTweensOf([toPanel, fromPanel, contentBlock, fg, bg, pulseSpan].filter(Boolean));

    gsap.set(toPanel, { yPercent: dir === 1 ? 100 : -100, zIndex: 3 });
    gsap.set(fromPanel, { zIndex: 2 });
    if (contentBlock) gsap.set(contentBlock, { opacity:0, y:24 });
    if (fg) gsap.set(fg, { opacity:0, scale:0.92 });
    if (bg) gsap.set(bg, { opacity:0 });
    if (pulseSpan) gsap.set(pulseSpan, { left:'-30%' });

    const tl = gsap.timeline({
      defaults: { ease: 'power2.out' },
      onComplete: () => {
        gsap.set(fromPanel, { zIndex:1 });
        // Safety net: whatever happened during the tweens, force the panel
        // that just became current to its fully-visible resting state.
        if (contentBlock) gsap.set(contentBlock, { opacity:1, y:0 });
        if (fg) gsap.set(fg, { opacity:1, scale:1 });
        if (bg) gsap.set(bg, { opacity:1 });
        if (pulseSpan) gsap.set(pulseSpan, { left:'130%' });
        setTimeout(() => { isAnimating = false; document.body.classList.remove('is-locking'); }, LOCK_BUFFER);
      }
    });

    tl.to(toPanel,   { yPercent: 0, duration: DURATION }, 0);
    tl.to(fromPanel, { yPercent: dir === 1 ? -100 : 100, duration: DURATION }, 0);
    if (bg) tl.to(bg, { opacity:1, duration: DURATION * 0.9, ease:'power2.out' }, 0.05);
    if (fg) tl.to(fg, { opacity:1, scale:1, duration: DURATION * 0.85, ease:'power3.out' }, 0.12);
    if (contentBlock) tl.to(contentBlock, { opacity:1, y:0, duration: DURATION * 0.8, ease:'power3.out' }, DURATION * 0.2);
    if (pulseSpan) tl.to(pulseSpan, { left:'130%', duration: DURATION * 0.7, ease:'power2.inOut' }, DURATION * 0.3);

    current = index;
    updateUI(current);
    hideHint();
  }

  function updateUI(index){
    dots.forEach((d,i) => d.classList.toggle('is-active', i === index));
    navLinks.forEach((l) => {
      if (l.dataset.group === 'services'){
        // "Services" nav link stays highlighted across all service panels (indices 1–12)
        l.classList.toggle('is-active', index >= 1 && index <= 12);
      } else {
        l.classList.toggle('is-active', parseInt(l.dataset.go,10) === index);
      }
    });
    history.replaceState(null, '', '#panel-' + index);
  }

  function hideHint(){
    if (kbHint && !kbHint.classList.contains('is-hidden')){
      kbHint.classList.add('is-hidden');
    }
  }

  // ---------- WHEEL ----------
  // A single physical trackpad/wheel gesture fires MANY 'wheel' events, and on
  // some trackpads (esp. macOS two-finger swipes) that stream can keep going
  // for well over a second. A fixed-time cooldown after the transition is a
  // guess that can still be shorter than a real gesture — when that happens,
  // the tail of the SAME swipe re-triggers the next panel immediately, and the
  // user only ever sees backgrounds blur past, never a settled headline.
  //
  // Fix: track gesture state directly. We accept the FIRST wheel event of a
  // gesture (triggers goTo), then ignore everything else until the stream of
  // wheel events actually goes quiet for GESTURE_SILENCE ms — i.e. until the
  // user's hand has actually left the trackpad/wheel, not just until our
  // transition animation finished.
  let wheelGestureActive = false;
  let wheelSilenceTimer = null;
  const GESTURE_SILENCE = 220; // ms of no wheel events = gesture considered over

  function armGestureReset(){
    clearTimeout(wheelSilenceTimer);
    wheelSilenceTimer = setTimeout(() => { wheelGestureActive = false; }, GESTURE_SILENCE);
  }

  window.addEventListener('wheel', (e) => {
    e.preventDefault();
    if (Math.abs(e.deltaY) < 8) return; // ignore trackpad noise / micro events

    armGestureReset(); // any wheel event (accepted or not) pushes the silence timer out

    if (isAnimating || wheelGestureActive) return; // mid-transition, or still inside an already-handled gesture
    wheelGestureActive = true;

    if (e.deltaY > 0) goTo(current + 1, 1);
    else goTo(current - 1, -1);
  }, { passive:false });

  // ---------- TOUCH ----------
  let touchStartY = null;
  window.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
  }, { passive:true });

  window.addEventListener('touchmove', (e) => {
    e.preventDefault(); // prevent native scroll/bounce while swiping panels
  }, { passive:false });

  window.addEventListener('touchend', (e) => {
    if (touchStartY === null || isAnimating) return;
    const touchEndY = e.changedTouches[0].clientY;
    const delta = touchStartY - touchEndY;
    const THRESHOLD = 50;

    if (Math.abs(delta) > THRESHOLD){
      if (delta > 0) goTo(current + 1, 1);
      else goTo(current - 1, -1);
    }
    touchStartY = null;
  }, { passive:true });

  // ---------- KEYBOARD ----------
  function isTypingInField(target){
    if (!target) return false;
    const tag = target.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || target.isContentEditable;
  }

  window.addEventListener('keydown', (e) => {
    if (isAnimating) return;
    if (isTypingInField(e.target)) return; // let the user type normally inside the Contact form
    if (['ArrowDown','PageDown',' '].includes(e.key)){
      e.preventDefault();
      goTo(current + 1, 1);
    } else if (['ArrowUp','PageUp'].includes(e.key)){
      e.preventDefault();
      goTo(current - 1, -1);
    } else if (e.key === 'Home'){
      e.preventDefault();
      goTo(0, -1);
    } else if (e.key === 'End'){
      e.preventDefault();
      goTo(total - 1, 1);
    }
  });

  // ---------- CLICK: dots + nav links ----------
  function bindGoTriggers(els){
    els.forEach((el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const target = parseInt(el.dataset.go, 10);
        if (Number.isNaN(target)) return;
        goTo(target, target > current ? 1 : -1);
      });
    });
  }
  // All elements with data-go not already covered by dots/navLinks
  const extraGoTriggers = document.querySelectorAll('[data-go]:not(.dot):not(.nav-links a):not(.nav-logo)');
  bindGoTriggers(dots);
  bindGoTriggers(navLinks);
  bindGoTriggers(extraGoTriggers);

  // ---------- prevent default page scroll entirely ----------
  document.addEventListener('scroll', (e) => { window.scrollTo(0,0); });

  // ---------- CONTACT FORM ----------
  // Visual-only for now: shows a local confirmation state on submit.
  // TODO: replace with a real fetch()/POST to a backend, serverless function,
  // or form service of choice.
  const contactForm   = document.getElementById('contactForm');
  const contactSubmit = document.getElementById('contactSubmit');
  const contactStatus = document.getElementById('contactStatus');

  if (contactForm){
    const submitDefaultHTML = contactSubmit.innerHTML;
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!contactForm.checkValidity()){
        contactForm.reportValidity();
        return;
      }

      contactSubmit.disabled = true;
      contactSubmit.textContent = 'Sending…';

      setTimeout(() => {
        contactStatus.classList.add('is-visible');
        contactSubmit.disabled = false;
        contactSubmit.innerHTML = submitDefaultHTML;
        contactForm.reset();
      }, 600);
    });
  }

})();
