document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initUploadForms();
    initFileInputs();
    initAIChat();
    initPDFViewerCheck();
    loadDocuments();
    initDocumentSelector();
    // initAnalysisTriggers();

    // Get CSRF token for AJAX requests
    function getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!token) {
            console.error('CSRF token not found');
            return null;
        }
        return token.value;
    }

    // Add this to your scripts.js file (preferably near the top with other function definitions)
async function queryDocument(question, docId = null) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    try {
        // If document ID is provided, check analysis status first
        if (docId && docId !== '1000') { // '1000' is special ID for all documents mode
            const statusResp = await fetch(`/api/document/${docId}/status/`);
            if (!statusResp.ok) throw new Error('Failed to check document status');
            
            const { is_analyzed } = await statusResp.json();
            
            if (!is_analyzed) {
                const analyze = confirm("Document needs analysis first. Analyze now?");
                if (analyze) {
                    await analyzeDocument(docId);
                } else {
                    throw new Error("Document not analyzed");
                }
            }
        }
        
        // Send query to server
        const response = await fetch('/ask-ai/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                question: question,
                document_id: docId
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Query failed");
        }
        
        return await response.json();
    } catch (error) {
        console.error('Query error:', error);
        throw error;
    }
}

async function analyzeDocument(docId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    try {
        showLoading(true);
        const response = await fetch(`/analyze-pdf/${docId}/`, {
            method: 'POST',
            headers: { 
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Analysis failed");
        }
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(`Analysis complete: ${data.chunk_count} chunks created`, 'success');
            return data;
        } else {
            throw new Error(data.error || "Analysis failed");
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showAlert(`Analysis failed: ${error.message}`, 'error');
        throw error;
    } finally {
        showLoading(false);
    }
}

    // Initialize document selection dropdown
    function initDocumentSelector() {
        const documentSelector = document.getElementById('document-selector');
        const hiddenInput = document.getElementById('selected-document-id');
        
        if (documentSelector && hiddenInput) {
            // Set initial value
            hiddenInput.value = documentSelector.value;
            
            // Update on change
            documentSelector.addEventListener('change', function () {
                const selectedDocId = this.value;
                hiddenInput.value = selectedDocId;
                
                // Save selection to session
                fetch('/set-selected-document/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ document_id: selectedDocId })
                }).catch(err => console.error('Error saving document selection:', err));
            });
        }
    }

    // Initialize file upload forms
    function initUploadForms() {
        const uploadBtn = document.getElementById('upload-btn');
        const fileInput = document.getElementById('file-input');
        
        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', handleFileSelect);
        }

        const uploadForm = document.getElementById('upload-form');
        if (uploadForm) {
            uploadForm.addEventListener('submit', handleFormSubmit);
        }

        // Disable buttons during form submission
        document.querySelectorAll('.animated-form').forEach(form => {
            form.addEventListener('submit', function (e) {
                const submitBtn = form.querySelector('.btn-submit');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                }
            });
        });
    }

    // Initialize file input displays
    function initFileInputs() {
        document.querySelectorAll('.file-input').forEach(input => {
            input.addEventListener('change', function () {
                const fileName = this.files[0]?.name || 'No file selected';
                const label = this.closest('.upload-area')?.querySelector('.file-label span') ||
                             this.closest('.file-upload-container')?.querySelector('.file-label');
                if (label) label.textContent = fileName;
            });
        });
    }

    // Handle file selection and upload
    function handleFileSelect(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            
            // Validate file type
            if (!file.type.includes('pdf')) {
                showAlert('Please select a PDF file', 'error');
                return;
            }

            // Validate file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                showAlert('File size should not exceed 10MB', 'error');
                return;
            }

            uploadFile(file);
        }
    }

    // Upload file to server
    function uploadFile(file) {
        const formData = new FormData();
        formData.append('pdf_file', file);
        showLoading(true);

        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Automatically analyze after upload if checkbox is checked
                if (document.getElementById('auto-analyze')?.checked) {
                    analyzeDocument(data.document.id);
                }
                window.location.href = data.redirectUrl || '/dashboard/';
            } else {
                showAlert(data.error || 'Upload failed', 'error');
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
            showAlert('Upload failed. Please try again.', 'error');
        })
        .finally(() => showLoading(false));
    }

    // Handle form submission
    function handleFormSubmit(e) {
        const form = e.target;
        const fileInput = form.querySelector('input[type="file"]');
        
        if (!fileInput || fileInput.files.length === 0) {
            e.preventDefault();
            showAlert('Please select a file to upload', 'error');
            return false;
        }
        
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        return true;
    }

    // Initialize AI chat interface
    function initAIChat() {
        document.querySelectorAll('#ai-chat-form[data-ajax="true"]').forEach(chatForm => {
            chatForm.addEventListener('submit', async function (e) {
                e.preventDefault();
                e.stopPropagation();

                const questionInput = this.querySelector('input[name="question"]');
                const question = questionInput?.value.trim();
                const chatMessages = this.closest('.ai-chat-container')?.querySelector('.ai-chat-messages') ||
                                    document.getElementById('chat-box');

                if (!question) {
                    addMessageToChat('Please enter a valid question', 'error', chatMessages);
                    questionInput?.focus();
                    return;
                }

                // Add user question to chat
                addMessageToChat(question, 'user', chatMessages);
                questionInput.value = '';

                // Show loading indicator
                const loadingId = 'loading-' + Date.now();
                addLoadingIndicator(loadingId, chatMessages);

                try {
                    // Get document ID from selector or hidden input
                    const docId = document.getElementById('document-selector')?.value || 
                                 document.getElementById('selected-document-id')?.value;

                    // Send query to server
                    const response = await queryDocument(question, docId);

                    // Remove loading indicator
                    document.getElementById(loadingId)?.remove();

                    if (response.success) {
                        // Format and display answer
                        const formattedAnswer = response.answer.replace(/\n/g, '<br>');
                        addMessageToChat(formattedAnswer, 'ai', chatMessages);

                        // Show sources if available
                        if (response.sources?.length > 0) {
                            addMessageToChat(`Sources: ${response.sources.join(', ')}`, 'ai meta', chatMessages);
                        }

                        // Show relevant chunks in debug mode
                        if (response.relevant_chunks?.length > 0 && document.body.classList.contains('debug-mode')) {
                            const chunksHtml = response.relevant_chunks.map(chunk => 
                                `<div class="chunk">${chunk.replace(/\n/g, '<br>')}</div>`
                            ).join('');
                            addMessageToChat(`Relevant chunks:<br>${chunksHtml}`, 'ai debug', chatMessages);
                        }
                    } else {
                        addMessageToChat(`Error: ${response.error || 'Unknown error'}`, 'error', chatMessages);
                    }
                } catch (error) {
                    document.getElementById(loadingId)?.remove();
                    addMessageToChat(`Error: ${error.message || 'Failed to process request'}`, 'error', chatMessages);
                    console.error('Chat Error:', error);
                }
            });
        });
    }

    // Add message to chat interface
    function addMessageToChat(message, className, container) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        const avatarIcon = className.includes('error') ? 'exclamation-circle' :
                          className.includes('ai') ? 'robot' : 'user';

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${avatarIcon}"></i>
            </div>
            <div class="message-content">${message}</div>
        `;
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    // Add loading indicator to chat
    function addLoadingIndicator(id, container) {
        const loadingDiv = document.createElement('div');
        loadingDiv.id = id;
        loadingDiv.className = 'message ai loading';
        loadingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <i class="fas fa-spinner fa-spin"></i> Processing...
            </div>
        `;
        container.appendChild(loadingDiv);
        container.scrollTop = container.scrollHeight;
    }

    // Show loading state for buttons
    function showLoading(show) {
        document.querySelectorAll('button[type="submit"]').forEach(btn => {
            btn.disabled = show;
            if (show) {
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            } else {
                btn.innerHTML = btn.dataset.originalText || 'Submit';
            }
        });
    }

    // Show alert message
    function showAlert(message, type = 'info') {
        // Replace with your preferred alert system
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.classList.add('fade-out');
            setTimeout(() => alertDiv.remove(), 500);
        }, 3000);
    }

    // Load and display documents
   function loadDocuments() {
    fetch('/all-documents/')  // Ensure this matches your URL pattern
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error("Response is not JSON");
            }
            return response.json();
        })
        .then(data => {
            if (data.documents?.length > 0) {
                updateDocumentGrid(data.documents);
            }
        })
        .catch(error => {
            console.error('Error loading documents:', error);
            showAlert('Failed to load documents. Please try again.', 'error');
        });
}

    // Update document grid display
    function updateDocumentGrid(documents) {
        const documentGrid = document.querySelector('.document-grid');
        if (!documentGrid) return;

        documentGrid.innerHTML = documents.map(doc => `
            <div class="document-card ${doc.isAnalyzed ? 'analyzed' : ''}">
                <div class="document-icon">
                    <i class="fas fa-file-pdf"></i>
                    ${doc.isAnalyzed ? '<span class="badge analyzed-badge">Analyzed</span>' : ''}
                </div>
                <div class="document-info">
                    <h3>${doc.fileName}</h3>
                    <p>Uploaded:
                    <div class="document-actions">
                        <a href="/document/${doc.id}/" class="btn-action">View</a>
                        <a href="/analyze/${doc.id}/" class="btn-action">Analyze</a>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function initPDFViewerCheck() {
        const isIE = /*@cc_on!@*/false || !!document.documentMode;
        const isEdge = !isIE && !!window.StyleMedia;
        const pdfSupported = !isIE && !isEdge;

        if (!pdfSupported) {
            document.querySelector('.pdf-viewer-wrapper')?.classList.add('no-pdf-support');
            document.body.classList.add('no-pdf-support');
        }
    }
});


// Add this to your upload success handler
function analyzeUploadedPDF(docId) {
    fetch(`/api/analyze-pdf/${docId}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`Analysis complete: ${data.chunk_count} chunks created`);
        } else {
            console.error('Analysis failed:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

const stripe = Stripe("{{ STRIPE_PUBLISHABLE_KEY }}"); // Make sure this key is correctly injected into your template
