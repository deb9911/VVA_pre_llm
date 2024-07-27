async function updateVoice() {
    const voice = document.getElementById('voice-select').value;
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...config, current_voice: voice }),
    });
    const data = await response.json();
    alert(data.message);
    fetchConfig();
}

async function addCommand() {
    const keyword = document.getElementById('new-command-keyword').value;
    const action = document.getElementById('new-command-action').value;
    const response = await fetch('/api/commands', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword, action }),
    });
    const data = await response.json();
    alert(data.message);
    fetchConfig();
}

async function fetchConfig() {
    const response = await fetch(apiUrl);
    const data = await response.json();
    document.getElementById('current-voice').innerText = data.current_voice;
    const voiceSelect = document.getElementById('voice-select');
    voiceSelect.innerHTML = '';
    data.voices.forEach(voice => {
        const option = document.createElement('option');
        option.value = voice;
        option.text = voice;
        voiceSelect.add(option);
    });
    const commandsList = document.getElementById('commands-list');
    commandsList.innerHTML = '';
    data.commands.forEach((cmd, index) => {
        const li = document.createElement('li');
        li.innerText = `${cmd.keyword}: ${cmd.action}`;
        commandsList.appendChild(li);
    });
}

fetchConfig();

