from decouple import config
from mistralai import Mistral
from pathlib import Path
import base64


def ocr_url_pdf_to_markdown(url, client):
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": url},
        include_image_base64=True,
    )

    full_doc = "\n\n".join(
        [
            f"### Page {i + 1}\n{ocr_response.pages[i].markdown}"
            for i in range(len(ocr_response.pages))
        ]
    )
    return full_doc


def ocr_local_pdf_to_markdown(pdf_path, client):
    """Process a local PDF file using base64 data URI."""
    
    # Read the PDF file and encode it as base64
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()
    
    # Create a data URI with the base64 encoded PDF
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    data_uri = f"data:application/pdf;base64,{pdf_base64}"
    
    # Process using the data URI
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": data_uri},
        include_image_base64=True,
    )

    full_doc = "\n\n".join(
        [
            f"### Page {i + 1}\n{ocr_response.pages[i].markdown}"
            for i in range(len(ocr_response.pages))
        ]
    )
    return full_doc


def process_all_pdfs_in_references():
    """Find all PDFs in references/ and OCR them to _references/."""
    api_key = config("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)
    
    references_dir = Path("references")
    output_dir = Path("_references")
    
    # Ensure output directory exists (fix the directory creation)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDF files in references/ (including subdirectories)
    pdf_files = list(references_dir.rglob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    for pdf_path in pdf_files:
        # Calculate relative path from references/ to maintain directory structure
        relative_path = pdf_path.relative_to(references_dir)
        
        # Create corresponding .md filename
        md_filename = relative_path.with_suffix('.md')
        output_path = output_dir / md_filename
        
        # Create subdirectories in _references if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip if .md file already exists
        if output_path.exists():
            print(f"Skipping {pdf_path} - markdown file already exists at {output_path}")
            continue
        
        print(f"Processing {pdf_path}...")
        try:
            # Process the PDF
            markdown_content = ocr_local_pdf_to_markdown(pdf_path, client)
            
            # Save the markdown file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            print(f"  -> Saved to {output_path}")
            
        except Exception as e:
            print(f"  -> Error processing {pdf_path}: {e}")


if __name__ == "__main__":
    process_all_pdfs_in_references()
