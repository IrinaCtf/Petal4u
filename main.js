let poems = [];

async function loadPoems() {
    const response = await fetch('data/poems.json');
    poems = await response.json();
}

function startPoetry() {
    const input = document.getElementById('userInput').value.trim();
    if (!input) return;
    let results = [];

    poems.forEach(poem => {
        poem.content.forEach(line => {
            if (line.includes(input)) {
                results.push(`《${poem.title}》${poem.author}：${line}`);
            }
        });
    });

    const resultArea = document.getElementById('resultArea');
    if (results.length === 0) {
        resultArea.innerHTML = "No matching verse found. Try another character or phrase.";
    } else {
        const randomLine = results[Math.floor(Math.random() * results.length)];
        resultArea.innerHTML = randomLine;
    }
}

window.onload = loadPoems;
