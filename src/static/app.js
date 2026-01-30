document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('registration-form');
  const participantsList = document.getElementById('participants-list');

  // Hide bullet points via JS in case CSS is not enough
  participantsList.style.listStyleType = 'none';
  participantsList.style.paddingLeft = '0';

  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email })
    });
    if (response.ok) {
      loadParticipants();
      form.reset();
    } else {
      alert('Registration failed.');
    }
  });

  async function loadParticipants() {
    const response = await fetch('/participants');
    const participants = await response.json();
    participantsList.innerHTML = '';
    participants.forEach(function(participant) {
      const li = document.createElement('li');
      li.style.display = 'flex';
      li.style.alignItems = 'center';
      li.style.justifyContent = 'space-between';
      li.style.padding = '4px 0';
      // Hide bullet points for each li (in case CSS is not enough)
      li.style.listStyleType = 'none';

      const span = document.createElement('span');
      span.textContent = participant.name + ' (' + participant.email + ')';

      const deleteBtn = document.createElement('button');
      deleteBtn.innerHTML = '🗑️';
      deleteBtn.title = 'Unregister';
      deleteBtn.style.background = 'none';
      deleteBtn.style.border = 'none';
      deleteBtn.style.cursor = 'pointer';
      deleteBtn.style.fontSize = '1em';
      deleteBtn.style.marginLeft = '8px';
      deleteBtn.setAttribute('aria-label', 'Unregister ' + participant.name);
      deleteBtn.addEventListener('click', async function() {
        if (confirm('Unregister ' + participant.name + '?')) {
          const resp = await fetch('/unregister', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: participant.email })
          });
          if (resp.ok) {
            loadParticipants();
          } else {
            alert('Failed to unregister.');
          }
        }
      });

      li.appendChild(span);
      li.appendChild(deleteBtn);
      participantsList.appendChild(li);
    });
  }

  loadParticipants();
});
