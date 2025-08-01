document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const resultDiv = document.getElementById('result');
    const downloadLink = document.getElementById('downloadLink');
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        downloadLink.href = data.download_link;
        downloadLink.textContent = `Download ${data.download_link.split('/').pop()}`;
        resultDiv.classList.remove('hidden');
    } catch (error) {
        alert('Conversion failed: ' + error.message);
    }
});
