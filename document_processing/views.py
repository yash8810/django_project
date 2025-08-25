from datetime import timezone
import io
import json
import logging
import numpy as np
import faiss
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import groq
from PyPDF2 import PdfReader
from .forms import PDFUploadForm
from .models import Document, AnalysisResult, UploadedPDF, CustomUser
from django.conf import settings
import os
from .forms import QueryForm
from document_processing.chunk_pdfs import process_new_document
import stripe



# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='a', encoding='utf-8')
logger = logging.getLogger(__name__)



# Load the FAISS index and metadata

vector_folder = 'Y:/YBAI/Document_AI/document_intelligence/document_processing/vector_store'  # Replace with your vector store path
faiss_index = faiss.read_index(f"{vector_folder}/faiss_index.faiss")
with open(f"{vector_folder}/chunk_metadata.json", "r", encoding="utf-8") as f:
    chunk_metadata = json.load(f)

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Query function
def query_faiss(query, faiss_index, model, chunk_metadata, top_k=5):
    if faiss_index.ntotal == 0:
        raise ValueError("FAISS index is empty. Ensure embeddings were added.")

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)

    # Perform FAISS search
    distances, indices = faiss_index.search(query_embedding, top_k)

    # Safely extract matching chunks
    results = []
    for idx in indices[0]:
        if 0 <= idx < len(chunk_metadata):
            results.append(chunk_metadata[idx])
        else:
            print(f"Warning: index {idx} out of bounds for chunk_metadata")
    return results


# View to handle user query
def query_view(request):
    results = []
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = query_faiss(query, faiss_index, model, chunk_metadata)
    else:
        form = QueryForm()

    return render(request, "query_page.html", {"form": form, "results": results})




# Initialize SentenceTransformer and OpenAI client
grok_client = groq.Client(api_key=settings.GROK_API_KEY)

def home(request):
    return render(request, 'home.html')

def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            print("User successfully registered and logged in")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
    return render(request, 'register.html')

def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    uploadedPdfs = UploadedPDF.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    recentAnalyses = AnalysisResult.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    context = {
        'uploadedPdfs': uploadedPdfs,
        'recentAnalyses': recentAnalyses,
        'documentsCount': UploadedPDF.objects.filter(user=request.user).count(),
        'analysisCount': AnalysisResult.objects.filter(user=request.user).count(),
        'reportsCount': AnalysisResult.objects.filter(user=request.user).count(),
        'accuracy': "80%",
    }
    return render(request, 'dashboard.html', context)


@login_required
def uploadDocument(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.user = request.user

                if not document.pdf_file.name.lower().endswith('.pdf'):
                    return JsonResponse({
                        'success': False,
                        'error': 'Only PDF files are allowed'
                    }, status=400)

                if document.pdf_file.size > 10 * 1024 * 1024:
                    return JsonResponse({
                        'success': False,
                        'error': 'File size should not exceed 10MB'
                    }, status=400)

                document.save()  # Save first to get document.id

                full_path = document.pdf_file.path
                chunk_metadata, index = process_new_document(full_path, document.id)  # Pass doc_id here


                # Process chunks and index bytes as you do
                clean_chunks = [{k: v.replace('\x00', '') if isinstance(v, str) else v for k, v in chunk.items()} for chunk in chunk_metadata]

                document.chunk_metadata = json.dumps(clean_chunks)
                document.faiss_index = index  # assuming this is bytes

                document.save()

                return JsonResponse({
                    'success': True,
                    'document': {   
                        'id': document.id,
                        'name': document.file_name,
                        'url': document.pdf_file.url,
                        'uploadedAt': document.uploaded_at.strftime("%b %d, %Y")
                    },
                    'redirectUrl': reverse('dashboard')
                })

            except Exception as e:
                logger.exception(f"Document upload failed: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)

        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

    # For GET requests, just render the form, don't return chunk_metadata or index
    form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})


def extract_text_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    extracted_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
    if not extracted_text.strip():
        raise ValueError("PDF contains no extractable text")
    return extracted_text

def split_text_into_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return text_splitter.split_text(text)

def generate_embeddings(chunks):
    return model.encode(chunks).astype(np.float32)

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return faiss.serialize_index(index)




@login_required
def uploadSuccess(request):
    return render(request, 'upload_success.html')

@login_required
def allDocuments(request):
    documents = UploadedPDF.objects.filter(user=request.user).order_by('-uploaded_at')
    return JsonResponse({
        'success': True,
        'documents': [{
            'id': doc.id,
            'fileName': doc.file_name,
            'uploadedAt': doc.uploaded_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        } for doc in documents]
    })


@login_required
def viewDocument(request, docId):
    document = get_object_or_404(UploadedPDF, id=docId, user=request.user)
    return render(request, 'view_document.html', {'document': document})

print(settings.GROK_API_KEY)  # Ensure this is set in settings.py


@csrf_exempt 
def set_selected_document(request):
    if request.method == "POST":
        data = json.loads(request.body)
        doc_id = data.get("document_id", "")
        request.session["selected_document_id"] = doc_id
        return JsonResponse({"status": "success", "document_id": doc_id})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
import faiss
import numpy as np
import logging

logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
@require_POST
def askAi(request):
    
    """
    Handle AI queries, supporting both document-specific and general knowledge.
    """

    response_data = {
        'success': False,
        'answer': '',
        'sources': [],
        'error': None,
        'relevant_chunks': []
    }

    try:
        # --- Input Processing ---
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
                question = str(data.get('question', '')).strip()
                doc_id = str(data.get('document_id', '') or '').strip()
                # doc_id = str(data.get('document_id', '')).strip()
            except json.JSONDecodeError:
                response_data['error'] = 'Invalid JSON'
                return JsonResponse(response_data, status=400)
        else:
            question = str(request.POST.get('question', '')).strip()
            doc_id = str(request.POST.get('document_id', '')).strip()

        if not question:
            response_data['error'] = 'Question required'
            return JsonResponse(response_data, status=400)

        # Use session value if document_id is not provided
        # if not doc_id:
        #     doc_id = str(request.session.get("selected_document_id", "")).strip()

        # logger.info(f"AI query: '{question}', doc_id='{doc_id or 'None'}'")

        # --- All Documents Mode ---
        # if doc_id == "1000":
        #     from .models import UploadedPDF  # Ensure this import exists

        #     documents = UploadedPDF.objects.filter(user=request.user)

        #     all_chunks = []
        #     for document in documents:
        #         if not (document.chunk_metadata and document.faiss_index):
        #             continue
        #         try:
        #             chunks = json.loads(document.chunk_metadata)
        #             index = faiss.deserialize_index(bytes(document.faiss_index))

        #             query_embedding = model.encode([question])[0].astype(np.float32)
        #             distances, indices = index.search(np.array([query_embedding], dtype=np.float32), 3)

        #             for i, idx in enumerate(indices[0]):
        #                 if distances[0][i] < 1.0:
        #                     all_chunks.append((chunks[idx]['text'], distances[0][i], document.file_name))

        #         except Exception as e:
        #             logger.warning(f"Skipping document {document.file_name}: {e}")
        #             continue

        #     if not all_chunks:
        #         response_data['error'] = 'No relevant info in any document'
        #         return JsonResponse(response_data, status=404)

        #     sorted_chunks = sorted(all_chunks, key=lambda x: x[1])[:3]
        #     relevant_chunks = [chunk for chunk, _, _ in sorted_chunks]
        #     sources = list(set(source for _, _, source in sorted_chunks))

        #     context = "\n\n".join(relevant_chunks)
        #     prompt = f"""Answer based on this document context:\n{context}\n\nQuestion: {question}\nAnswer:"""

        #     ai_response = grok_client.chat.completions.create(
        #         model="llama3-8b-8192",
        #         messages=[
        #             {"role": "system", "content": "Precise doc analysis. Use context ONLY."},
        #             {"role": "user", "content": prompt}
        #         ],
        #         temperature=0.3, max_tokens=800, top_p=0.9
        #     )
        #     answer = ai_response.choices[0].message.content.strip()

        #     response_data.update({
        #         'success': True,
        #         'answer': answer,
        #         'sources': sources,
        #         'relevant_chunks': relevant_chunks
        #     })
        #     return JsonResponse(response_data)

        # # --- Single Document Logic ---
        # elif doc_id:
        #     from .models import UploadedPDF  # Ensure this import exists
        #     try:

        #         print("yaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #         print(doc_id)
        #         document = get_object_or_404(UploadedPDF, id=doc_id, user=request.user)
        #         print(document)

        #         if not (document.chunk_metadata and document.faiss_index):
        #             response_data['error'] = 'Document not ready for analysis'
        #             return JsonResponse(response_data, status=400)

        #         chunks = json.loads(document.chunk_metadata)
        #         index = faiss.deserialize_index(bytes(document.faiss_index))

        #         query_embedding = model.encode([question])[0].astype(np.float32)
        #         distances, indices = index.search(np.array([query_embedding], dtype=np.float32), 3)

        #         relevant_chunks = [
        #             chunks[idx]['text']
        #             for i, idx in enumerate(indices[0])
        #             if distances[0][i] < 1.0
        #         ]

        #         if not relevant_chunks:
        #             response_data['error'] = 'No relevant info in document'
        #             return JsonResponse(response_data, status=404)

        #         context = "\n\n".join(relevant_chunks)
        #         prompt = f"""Answer based on this document context:\n{context}\n\nQuestion: {question}\nAnswer:"""

        #         ai_response = grok_client.chat.completions.create(
        #             model="llama3-8b-8192",
        #             messages=[
        #                 {"role": "system", "content": "Precise doc analysis. Use context ONLY."},
        #                 {"role": "user", "content": prompt}
        #             ],
        #             temperature=0.3, max_tokens=800, top_p=0.9
        #         )
        #         answer = ai_response.choices[0].message.content.strip()

        #         response_data.update({
        #             'success': True,
        #             'answer': answer,
        #             'sources': [document.file_name],
        #             'relevant_chunks': relevant_chunks[:3]
        #         })
        #         return JsonResponse(response_data)

        #     except UploadedPDF.DoesNotExist:
        #         response_data['error'] = 'Document not found'
        #         return JsonResponse(response_data, status=404)
        #     except faiss.FaissError as e:
        #         logger.error(f"FAISS error: {e}")
        #         response_data['error'] = f"Vector search error: {e}"
        #         return JsonResponse(response_data, status=500)
        #     except Exception as e:
        #         logger.exception(f"Doc processing error (doc_id={doc_id}): {e}")
        #         response_data['error'] = f'Document error: {e}'
        #         return JsonResponse(response_data, status=500)

        # --- General Knowledge Fallback ---
        try:
            ai_response = grok_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Helpful AI assistant. Concise, accurate answers."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7, max_tokens=700, top_p=0.95
            )
            answer = ai_response.choices[0].message.content.strip()
            response_data.update({
                'success': True,
                'answer': answer,
                'sources': ['General knowledge']
            })
            return JsonResponse(response_data)

        except Exception as e:
            logger.exception(f"Grok API error: {e}")
            response_data['error'] = 'AI service error'
            return JsonResponse(response_data, status=500)

    except Exception as e:
        logger.exception(f"Unexpected error in askAi: {e}")
        response_data['error'] = 'Internal server error'
        return JsonResponse(response_data, status=500)


@login_required
def analyzePdf(request, docId):
    document = get_object_or_404(UploadedPDF, id=docId, user=request.user)
    
    try:
        # 1. Extract text from PDF
        pdf_reader = PdfReader(document.pdf_file.path)
        extracted_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        
        if not extracted_text.strip():
            raise ValueError("PDF contains no extractable text")

        # 2. Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(extracted_text)

        print(f"Chunks: {chunks[:5]}") 
        
        # 3. Generate embeddings
        embeddings = model.encode(chunks, show_progress_bar=False)

        print(f"Embeddings shape: {embeddings.shape}")  # Verify the shape of embeddings

        # embeddings = np.array(embeddings, dtype=np.float32)  # Critical: ensure float32
        embedding_matrix = np.array(embeddings).astype('float32')
        
        # 4. Create and save FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        print(f"Index dimension: {dimension}, Embeddings type: {embeddings.dtype}")


        print(f"Number of vectors in the index: {index.ntotal}")

        
        # Serialize properly
        document.faiss_index = faiss.serialize_index(index).tobytes()
        
        # # Save metadata
        # document.chunk_metadata = json.dumps([{
        #     "doc_id": docId,
        #     "text": chunk,
        #     "page": (i // 3) + 1,
        #     "embedding_shape": embeddings[i].shape  # Store shape for verification
        # } for i, chunk in enumerate(chunks)])
        
        chunk_metadata = [{
                "doc_id": docId,
                "text": chunk,
                "page": (i // 3) + 1,  # Assuming page is based on chunk indexing
                "embedding_shape": embeddings[i].shape  # Store embedding shape for debugging
            } for i, chunk in enumerate(chunks)]


        print(f"Chunk metadata: {chunk_metadata[:5]}")  # Print first 5 metadata entries for inspection


        document.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Processed {len(chunks)} chunks',
            'embedding_shape': embeddings.shape
        })
        
    except Exception as e:
        logger.exception(f"PDF analysis failed: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def editProfile(request):
    return render(request, 'edit_profile.html')

@login_required
def changePassword(request):
    return render(request, 'change_password.html')

@login_required
def protectedPdfView(request, path):
    try:
        response = FileResponse(open(os.path.join(settings.MEDIA_ROOT, path), 'rb'))
        response['Content-Disposition'] = 'inline'
        return response
    except FileNotFoundError:
        raise Http404

@login_required
def extractedContent(request, docId):
    document = get_object_or_404(UploadedPDF, id=docId, user=request.user)
    try:
        pdf_reader = PdfReader(document.pdf_file.path)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""
        
        return JsonResponse({
            'success': True,
            'extractedText': extracted_text,
            'documentName': document.file_name
        }, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500, content_type='application/json')


@login_required
def verify_analysis(request, docId):
    document = get_object_or_404(UploadedPDF, id=docId, user=request.user)
    
    status = {
        'analyzed': False,
        'has_index': bool(document.faiss_index),
        'has_chunks': False,
        'error': None
    }
    
    if document.chunk_metadata:
        try:
            chunks = json.loads(document.chunk_metadata)
            status.update({
                'analyzed': True,
                'has_chunks': len(chunks) > 0,
                'chunk_count': len(chunks)
            })
        except Exception as e:
            status['error'] = f"Invalid chunk data: {str(e)}"
    
    return JsonResponse(status)

