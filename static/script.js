const chatBox = document.getElementById("chat-box");
const questionInput = document.getElementById("question");

function addMessage(message, sender) {

    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add(sender);

    div.innerHTML = message;

    chatBox.appendChild(div);

    // Auto Scroll
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
}

async function askQuestion() {

    const question = questionInput.value.trim();

    if (!question) return;

    addMessage(question, "user");

    questionInput.value = "";

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        addMessage(data.answer, "bot");

    }
    catch(error){

        addMessage("❌ Error connecting to AI", "bot");

        console.error(error);
    }
}

questionInput.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        askQuestion();
    }

});
