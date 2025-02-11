document.getElementById("sendButton").addEventListener("click", function() {
    let textInput = document.getElementById("textInput").value;
    let responseType = document.getElementById("responseType").value;
    let sendButton = document.getElementById("sendButton");
    let loader = document.querySelector(".loader");
    
    if (!textInput.trim() || !responseType) {
        alert("Please, fill the text input and select the response type.");
        return;
    }

    let mediaSection = document.getElementById("mediaSection");
    let gifElement = document.getElementById("responseGif");
    let imageElement = document.getElementById("responseImage");

    mediaSection.classList.add("hidden");
    gifElement.classList.add("hidden");
    imageElement.classList.add("hidden");

    gifElement.src = "";
    imageElement.src = "";

    sendButton.disabled = true;

    loader.classList.remove("hidden");

    let endpoint = responseType === "image" 
        ? "http://localhost:8000/generate"
        : "http://localhost:8001/generate";

    fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000"
        },
        body: JSON.stringify({ prompt: textInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error({ status: response.status, error: response.statusText });
        }
        return response.blob();
    })
    .then(blob => {
        loader.classList.add("hidden");

        if (responseType === "gif" && blob.type === "image/gif") {
            const gifUrl = URL.createObjectURL(blob);
            gifElement.src = gifUrl;
            gifElement.classList.remove("hidden");
        } else if (responseType === "image" && blob.type === "image/png") {
            const imageUrl = URL.createObjectURL(blob);
            imageElement.src = imageUrl;
            imageElement.classList.remove("hidden");
        } else {
            alert("Error: Invalid response type or no data found, please try again.");
        }
        mediaSection.classList.remove("hidden");
    })
    .catch(error => {
        console.error("Error:", error);
        loader.classList.add("hidden");
    })
    .finally(() => {
        sendButton.disabled = false;
    });
});
