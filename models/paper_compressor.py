import re
from PyPDF2 import PdfReader


class PaperCompressor:
    def __init__(self):
        self.chunk_size = 1000

    def extract_content(self, pdf_file):
        text_content = ""

        try:
            reader = PdfReader(pdf_file)

            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()

                if page_text:
                    text_content += f"\n\n[Page {i+1}]\n\n"
                    text_content += page_text

        except Exception as e:
            return {"error": f"PDF extraction failed: {str(e)}"}

        if not text_content.strip():
            return {"error": "No readable text found in PDF."}

        # Clean text
        text_content = re.sub(r"-\n", "", text_content)
        text_content = re.sub(r"\n+", "\n", text_content)
        text_content = re.sub(r"[ \t]+", " ", text_content)

        clean_text = text_content.strip()

        # Extract citations
        citations = re.findall(r"\[(\d+)\]", clean_text)
        citations = list(set(citations))

        # Create chunks
        chunks = self._create_chunks(clean_text)

        return {
            "chunks": chunks[:150],  # limit for speed
            "citations": citations,
            "full_text": clean_text
        }

    def _create_chunks(self, text):
        paragraphs = text.split("\n")

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if len(para) < 40:
                continue

            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += " " + para
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
