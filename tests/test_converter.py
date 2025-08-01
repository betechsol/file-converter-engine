import pytest
import os
from converter.app import FileConverter

@pytest.fixture
def sample_files(tmp_path):
    # Create test files
    pdf_path = tmp_path / "test.pdf"
    docx_path = tmp_path / "test.docx"
    image_path = tmp_path / "test.png"
    
    # PDF
    with open(pdf_path, 'wb') as f:
        f.write(b'%PDF dummy content')  # Minimal PDF header
    
    # DOCX
    from docx import Document
    doc = Document()
    doc.add_paragraph("Test DOCX content")
    doc.save(docx_path)
    
    # Image (white 1x1 pixel)
    from PIL import Image
    Image.new('RGB', (1, 1), color='white').save(image_path)
    
    return pdf_path, docx_path, image_path

def test_pdf_conversion(sample_files, tmp_path):
    pdf_path, _, _ = sample_files
    output = tmp_path / "output.txt"
    assert FileConverter.pdf_to_txt(str(pdf_path), str(output)) is not None
    assert os.path.exists(output)

def test_docx_conversion(sample_files, tmp_path):
    _, docx_path, _ = sample_files
    output = tmp_path / "output.txt"
    assert FileConverter.docx_to_txt(str(docx_path), str(output)) is not None
    assert "Test DOCX content" in open(output).read()

def test_image_conversion(sample_files, tmp_path):
    _, _, image_path = sample_files
    output = tmp_path / "output.txt"
    assert FileConverter.image_to_txt(str(image_path), str(output)) is not None
