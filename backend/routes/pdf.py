"""API routes for PDF upload and chat"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from models.pdf import PDFUploadResponse, PDFAskRequest, PDFAskResponse
from services.pdf_service import get_pdf_service
from services.pdf_document_store import get_pdf_document_store
from services.gemini_service import get_gemini_service
import asyncio

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post(
    "/upload",
    response_model=PDFUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload PDF document"
)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF document for analysis
    
    The PDF will be:
    1. Text extracted from all pages
    2. Split into chunks
    3. Stored in memory for querying
    """
    print(f"\n[PDF/UPLOAD] Received file: {file.filename}")
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Read file content
        print("[PDF/UPLOAD] Reading file content...")
        content = await file.read()
        print(f"[PDF/UPLOAD] Read {len(content)} bytes")
        
        # Process PDF
        pdf_service = get_pdf_service()
        
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(pdf_service.process_pdf, content, file.filename),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="PDF processing timed out"
            )
        
        # Store chunks
        doc_store = get_pdf_document_store()
        doc_store.add_pdf_chunks(result['chunks'], file.filename)
        
        print(f"[PDF/UPLOAD] ✓ Success")
        
        return PDFUploadResponse(
            filename=file.filename,
            num_chunks=result['num_chunks'],
            total_chars=result['total_chars'],
            message=f"PDF uploaded and processed successfully. {result['num_chunks']} chunks created."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[PDF/UPLOAD] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process PDF: {str(e)}"
        )

@router.post(
    "/ask",
    response_model=PDFAskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask question about uploaded PDF"
)
async def ask_about_pdf(request: PDFAskRequest):
    """
    Ask a question about the uploaded PDF
    
    The AI will:
    1. Search relevant sections from the PDF
    2. Generate an answer based on the content
    3. Respond in your language (English/Hindi/Hinglish)
    """
    print(f"\n[PDF/ASK] Query: '{request.query}'")
    
    try:
        # Check if PDF is uploaded
        doc_store = get_pdf_document_store()
        
        if not doc_store.has_documents():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No PDF uploaded. Please upload a PDF first using /pdf/upload"
            )
        
        print(f"[PDF/ASK] Current PDF: {doc_store.current_pdf}")
        
        # Search relevant content
        print("[PDF/ASK] Searching relevant content...")
        relevant_chunks = doc_store.search(request.query, top_k=3)
        
        # Build context
        if relevant_chunks:
            context = "\n\n".join([
                f"[Section {i+1}]\n{chunk['content']}"
                for i, chunk in enumerate(relevant_chunks)
            ])
        else:
            # If no relevant chunks, use all content
            context = doc_store.get_all_content()[:3000]  # Limit to 3000 chars
        
        print(f"[PDF/ASK] Context length: {len(context)} chars")
        
        # Generate answer using Gemini
        print("[PDF/ASK] Generating answer...")
        gemini_service = get_gemini_service()
        
        prompt = f"""You are a helpful AI assistant. A user has uploaded a PDF document and is asking questions about it.

User's Question: {request.query}

Relevant Content from PDF:
{context}

Instructions:
1. Answer the user's question based ONLY on the provided PDF content
2. If the user asked in Hindi/Hinglish, respond in that language
3. Be clear, concise, and helpful
4. If the answer is not in the PDF content, say so politely
5. Use examples from the PDF when relevant

Answer:"""
        
        try:
            answer = await asyncio.wait_for(
                gemini_service.generate_response(
                    system_prompt="You are a helpful AI assistant that answers questions about uploaded documents.",
                    user_prompt=prompt,
                    temperature=0.7
                ),
                timeout=20.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Answer generation timed out"
            )
        
        print(f"[PDF/ASK] ✓ Answer generated ({len(answer)} chars)")
        
        return PDFAskResponse(
            query=request.query,
            answer=answer.strip(),
            source=doc_store.current_pdf
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[PDF/ASK] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )

@router.get(
    "/status",
    summary="Check PDF upload status"
)
async def get_pdf_status():
    """Check if a PDF is currently uploaded"""
    doc_store = get_pdf_document_store()
    
    if doc_store.has_documents():
        return {
            "uploaded": True,
            "filename": doc_store.current_pdf,
            "num_chunks": len(doc_store.documents)
        }
    else:
        return {
            "uploaded": False,
            "filename": None,
            "num_chunks": 0
        }
