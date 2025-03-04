import os
import re
import fitz  
import openpyxl  
from io import BytesIO
from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
from docx import Document
from config import Config 
from app.models.category_models import Category
from app.models.file_models import File
from flask_login import current_user
from app.services.services import CRUDService

ALLOWED_EXTENSIONS = {"txt", "csv", "pdf", "docx", "xlsx"}

file_service = CRUDService(File)
categories_service = CRUDService(Category)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_xlsx(file):
    """Extract text from an XLSX file."""
    text = []
    file.seek(0)  
    workbook = openpyxl.load_workbook(file, data_only=True)
    
    for sheet in workbook.sheetnames:
        ws = workbook[sheet]
        for row in ws.iter_rows(values_only=True):
            text.append(" ".join(str(cell) for cell in row if cell)) 
            
    return "\n".join(text).strip()

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    pdf_bytes = file.read()
    pdf_stream = BytesIO(pdf_bytes)
    
    try:
        with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print("Error reading PDF:", e)
        return ""

    return text.strip()

def get_categories_from_db():
    categories = {}
    db_categories = categories_service.get()

    for category in db_categories:
        if category.keywords:
            categories[category.name] = category.keywords  

    return categories

def categorize_content(content):
    if not content.strip():  
        return "Uncategorized"

    categories = get_categories_from_db() 

    for category, keywords in categories.items():
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", content, re.IGNORECASE):
                return category  

    return "Uncategorized"

def upload_file(request):
    if "docs_file" not in request.files:
        return jsonify({'error': True, 'message': 'No file part'}), 400

    file = request.files["docs_file"]
    
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({'error': True, 'message': 'Invalid file'}), 400

    file_ext = file.filename.rsplit(".", 1)[1].lower()
    
    content = ""
    if file_ext == "pdf":
        content = extract_text_from_pdf(file)
    elif file_ext == "docx":
        content = extract_text_from_docx(file)
    elif file_ext == "xlsx":
        content = extract_text_from_xlsx(file)
    else:  
        content = file.read().decode("utf-8")

    # Categorize content
    category_name = categorize_content(content)
    if category_name == "Uncategorized":
        return jsonify({'error': True, 'message': 'File does not match any category. Upload denied.'}), 400

    # Fetch category from database
    category = categories_service.get_one(name=category_name)
    if not category:
        return jsonify({'error': True, 'message': 'Category not found in database.'}), 400

    filename = secure_filename(file.filename)

    existing_file = file_service.get_one(filename=filename, category_id=category.id)
    if existing_file:
        return jsonify({
            'error': True,
            'message': f'File "{filename}" already exists under the "{category_name}" category!'
        }), 400

    upload_folder = os.path.join(current_app.root_path, "static", "upload")
    os.makedirs(upload_folder, exist_ok=True)  

    filepath = os.path.join("static", "upload", filename)
    full_path = os.path.join(upload_folder, filename)

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    file.save(full_path)

    uploader_id = current_user.id if current_user.is_authenticated else None
    
    file_data = {
        "filename": filename,
        "filepath": filepath,
        "file_size": file_size,
        "file_extension": file_ext,
        "category_id": category.id,
        "uploader_id": uploader_id 
    }
    file_service.create(**file_data)

    return jsonify({
        "filename": filename,
        "category": category_name,
        "file_url": f"/{filepath}",
        "message": "File uploaded successfully!"
    })


def delete_file(request, file_id=None):
    if request.method == 'DELETE':
        file = file_service.get_one(id=file_id)
        
        if not file:
            return jsonify({"success": False, "message": "File not found"}), 404

        # Remove file from storage
        try:
            file_path = os.path.join(current_app.root_path, file.filepath)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            return jsonify({"success": False, "message": f"Error deleting file: {str(e)}"}), 500

        file_service.delete(file.id)

        return jsonify({"success": True, "message": "File deleted successfully!"})