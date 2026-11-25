(() => {
  const group = document.querySelector('.project-nav');
  const details = group.querySelector('details');
  const button = details.querySelector('summary');
  let timer;
  let pinned = false;
  const close = () => {
    clearTimeout(timer);
    details.open = false;
    pinned = false;
  };
  group.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') {
      clearTimeout(timer);
      details.open = true;
    }
  });
  group.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse' && !pinned && !details.contains(document.activeElement)) {
      timer = setTimeout(close, 180);
    }
  });
  button.addEventListener('click', event => {
    event.preventDefault();
    if (details.open && pinned) close();
    else { details.open = true; pinned = true; }
  });
  group.addEventListener('focusout', event => {
    if (!group.contains(event.relatedTarget)) close();
  });
  document.addEventListener('pointerdown', event => {
    if (!group.contains(event.target)) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && details.open) {
      if (details.contains(document.activeElement)) button.focus();
      close();
    }
  });
})();
