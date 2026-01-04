// Legion AI - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('queryForm');
    const queryInput = document.getElementById('queryInput');
    const consoleBody = document.getElementById('console');
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    // Focus on input
    queryInput.focus();
    
    // Handle form submission
    queryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        if (!query) return;
        
        // Add user query to console
        addConsoleMessage(`USER: ${query}`, 'user-message');
        addConsoleMessage('SYSTEM: Processing query...', 'system-message');
        
        // Clear input
        queryInput.value = '';
        
        // Disable input while processing
        queryInput.disabled = true;
        
        try {
            // Send query to server
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                addConsoleMessage(`SYSTEM: Found ${data.results.length} results`, 'system-message');
                displayResults(data.results);
            } else {
                addConsoleMessage(`ERROR: ${data.message}`, 'error-message');
            }
        } catch (error) {
            addConsoleMessage(`ERROR: ${error.message}`, 'error-message');
        } finally {
            // Re-enable input
            queryInput.disabled = false;
            queryInput.focus();
        }
    });
    
    // Add message to console
    function addConsoleMessage(message, className = '') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `console-message ${className}`;
        
        // Add prompt for system messages
        if (className === 'system-message') {
            messageDiv.innerHTML = `<span class="prompt">SYSTEM:</span> ${message.replace('SYSTEM: ', '')}`;
        } else if (className === 'user-message') {
            messageDiv.innerHTML = `<span class="prompt">USER:</span> ${message.replace('USER: ', '')}`;
        } else if (className === 'error-message') {
            messageDiv.innerHTML = `<span class="prompt">ERROR:</span> ${message.replace('ERROR: ', '')}`;
        } else {
            messageDiv.textContent = message;
        }
        
        consoleBody.appendChild(messageDiv);
        
        // Scroll to bottom
        consoleBody.scrollTop = consoleBody.scrollHeight;
    }
    
    // Display search results
    function displayResults(results) {
        if (results.length === 0) {
            resultsContent.innerHTML = '<p>No results found.</p>';
            resultsSection.style.display = 'block';
            return;
        }
        
        resultsContent.innerHTML = '';
        
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            resultItem.innerHTML = `
                <div class="result-title">${escapeHtml(result.title)}</div>
                <div class="result-url">${escapeHtml(result.url)}</div>
                <div class="result-snippet">${escapeHtml(result.snippet)}</div>
            `;
            
            resultsContent.appendChild(resultItem);
        });
        
        resultsSection.style.display = 'block';
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Check server status on load
    checkStatus();
    
    async function checkStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            if (data.status === 'online') {
                console.log('Legion AI Online:', data);
            }
        } catch (error) {
            console.error('Status check failed:', error);
        }
    }
    
    // Add some terminal effects
    let cursorVisible = true;
    setInterval(() => {
        const cursor = document.querySelector('.cursor');
        if (cursor) {
            cursor.style.opacity = cursorVisible ? '1' : '0';
            cursorVisible = !cursorVisible;
        }
    }, 500);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+L to clear console
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            clearConsole();
        }
    });
    
    function clearConsole() {
        consoleBody.innerHTML = `
            <div class="console-message system-message">
                <span class="prompt">SYSTEM:</span> Console cleared.<br>
                <span class="prompt">></span> <span class="cursor">_</span>
            </div>
        `;
    }
});
