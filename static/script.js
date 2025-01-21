document.getElementById("url-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const originalUrl = document.getElementById("original-url").value;
    const customAlias = document.getElementById("custom-alias").value;
    const expiryDate = document.getElementById("expiry-date").value;

    const dataToSend = { original_url: originalUrl };
    if (customAlias) dataToSend.custom_alias = customAlias;
    if (expiryDate) dataToSend.expiry_date = expiryDate;

    const response = await fetch("/shorten", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
    });

    const data = await response.json();

    if (response.ok) {
        const shortenedUrlElement = document.createElement("a");
        shortenedUrlElement.href = `${location.origin}/${data.shortened_url}`;
        shortenedUrlElement.target = "_blank";
        shortenedUrlElement.innerText = `${location.origin}/${data.shortened_url}`;

        document.getElementById("result").innerHTML = "Shortened URL: ";
        document.getElementById("result").appendChild(shortenedUrlElement);

        const qrResponse = await fetch(`/qrcode/${data.shortened_url}`);
        if (qrResponse.ok) {
            const qrImageBlob = await qrResponse.blob();
            const qrImageURL = URL.createObjectURL(qrImageBlob);
            const imgElement = document.createElement("img");
            imgElement.src = qrImageURL;
            imgElement.alt = "QR Code";
            document.getElementById("qrcode-container").innerHTML = '';
            document.getElementById("qrcode-container").appendChild(imgElement);
        } else {
            document.getElementById("qrcode-container").innerText = "Error generating QR code";
        }
    } else {
        document.getElementById("result").innerText = "Error shortening URL";
        document.getElementById("qrcode-container").innerHTML = '';
    }
});