document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const compressButton = document.getElementById('compressButton');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    const spinner = document.getElementById('spinner');
    const traceLink = document.getElementById('traceLink');
    // The metaLink is no longer used.
    // const metaLink = document.getElementById('metaLink'); 
    const errorSection = document.getElementById('errorSection');

    compressButton.addEventListener('click', async () => {
        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select a file first.');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // --- UI Updates: Show spinner, hide old results ---
        resultsSection.style.display = 'block';
        resultsContent.style.display = 'none';
        errorSection.style.display = 'none';
        spinner.style.display = 'block';

        try {
            const response = await fetch('/compress', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.details || 'An unknown error occurred.');
            }

            // --- Populate the single download link ---
            traceLink.href = result.trace_url;
            traceLink.download = file.name + '.ccc.trace';
            
            // --- Hide the meta link parent element --- 
            const metaLinkContainer = document.getElementById('metaLink').parentElement;
            if (metaLinkContainer) {
                metaLinkContainer.style.display = 'none';
            }

            // --- UI Updates: Show results ---
            resultsContent.style.display = 'block';

        } catch (error) {
            console.error('Compression failed:', error);
            errorSection.innerHTML = `<strong>Error:</strong> ${error.message}`;
            errorSection.style.display = 'block';
        } finally {
            spinner.style.display = 'none';
        }
    });
});
