let npcCounter = 0;

function nextStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));

    // Show the selected step
    document.getElementById('step-' + stepNumber).classList.add('active');
}

function addNPC() {
    npcCounter++;
    const npcHTML = `
    <div class="card mb-3 p-3 border border-primary rounded">
      <h5>NPC ${npcCounter}</h5>
      
      <div class="mb-3">
        <label>Name</label>
        <input type="text" class="form-control" name="npc_name[]" required>
      </div>

      <div class="mb-3">
        <label>Appearance</label>
        <input type="text" class="form-control" name="npc_appearance[]" required>
      </div>

      <div class="mb-3">
        <label>Characteristics</label>
        <input type="text" class="form-control" name="npc_characteristics[]" required>
      </div>

      <div class="mb-3">
        <label>Back Story</label>
        <textarea class="form-control" name="npc_backstory[]" required></textarea>
      </div>

      <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeNPC(this)">Delete NPC</button>
    </div>
  `;

    document.getElementById('npcContainer').insertAdjacentHTML('beforeend', npcHTML);
}

function removeNPC(button) {
    button.closest('.card').remove();
}

function collectNPCs() {
    const npcList = [];

    // Collect all NPC cards
    document.querySelectorAll('#npcContainer .card').forEach(card => {
        const npc = {
            name: card.querySelector('input[name="npc_name[]"]').value,
            appearance: card.querySelector('input[name="npc_appearance[]"]').value,
            characteristics: card.querySelector('input[name="npc_characteristics[]"]').value,
            backstory: card.querySelector('textarea[name="npc_backstory[]"]').value
        };
        npcList.push(npc);
    });

    return npcList;
}

const form = document.getElementById('createGameForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission

    const data = {
        world_name: form.elements['world_name'].value,
        world_genre: form.elements['world_genre'].value,
        world_detail: form.elements['world_detail'].value,
        npcs: collectNPCs(),
        scene_prologue: form.elements['scene_prologue'].value,
        scene_opening_line: form.elements['scene_opening_line'].value,
        scene_goal: form.elements['scene_goal'].value,
        scene_fail_when: form.elements['scene_fail_when'].value,
        scene_ending_line: form.elements['scene_ending_line'].value
    };

    console.log('Data:', data);

    try {
        const response = await fetch('/create_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Game Created:', result);
            window.location.href = '/';
        } else {
            console.error('Failed to create game');
        }

    } catch (error) {
        console.error('Error:', error);
    }
});