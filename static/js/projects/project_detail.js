function copyCode(button) {
    const codeBlock = button.nextElementSibling.querySelector('code');
    const text = codeBlock.innerText;

    navigator.clipboard.writeText(text).then(function() {
        button.textContent = "Copied";
        setTimeout(() => button.textContent = "Copy", 1500);
    });
}
