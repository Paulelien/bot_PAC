"""
Preprocesador de PDFs para el Chatbot PAC
Divide PDFs en chunks pequeños y crea embeddings para búsqueda semántica
"""

import os
import json
import tiktoken
from typing import List, Dict, Any
import PyPDF2
from pathlib import Path

class PDFPreprocessor:
    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        """
        Inicializar preprocesador
        
        Args:
            chunk_size: Tamaño máximo de cada chunk en tokens
            overlap: Solapamiento entre chunks para mantener contexto
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Para GPT-3.5/4
        
    def count_tokens(self, text: str) -> int:
        """Contar tokens en un texto"""
        return len(self.tokenizer.encode(text))
    
    def split_text_into_chunks(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dividir texto en chunks de tamaño específico
        
        Args:
            text: Texto completo del PDF
            metadata: Metadatos del PDF (unidad, tema, etc.)
            
        Returns:
            Lista de chunks con contenido y metadatos
        """
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        current_tokens = 0
        
        for sentence in sentences:
            sentence = sentence.strip() + ". "
            sentence_tokens = self.count_tokens(sentence)
            
            # Si agregar la oración excede el límite, crear nuevo chunk
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                chunks.append({
                    "id": f"{metadata['unidad']}_{metadata['tema']}_{len(chunks)}",
                    "content": current_chunk.strip(),
                    "tokens": current_tokens,
                    "metadata": metadata.copy()
                })
                
                # Mantener solapamiento para contexto
                overlap_text = current_chunk[-self.overlap:] if self.overlap > 0 else ""
                current_chunk = overlap_text + sentence
                current_tokens = self.count_tokens(current_chunk)
            else:
                current_chunk += sentence
                current_tokens += sentence_tokens
        
        # Agregar el último chunk si tiene contenido
        if current_chunk.strip():
            chunks.append({
                "id": f"{metadata['unidad']}_{metadata['tema']}_{len(chunks)}",
                "content": current_chunk.strip(),
                "tokens": current_tokens,
                "metadata": metadata.copy()
            })
        
        return chunks
    
    def process_pdf(self, pdf_path: str, unidad: int, tema: str) -> List[Dict[str, Any]]:
        """
        Procesar un PDF y dividirlo en chunks
        
        Args:
            pdf_path: Ruta al archivo PDF
            unidad: Número de unidad del curso
            tema: Tema o sección del PDF
            
        Returns:
            Lista de chunks del PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extraer texto de todas las páginas
                for page in pdf_reader.pages:
                    text += page.extract_text() + " "
                
                # Metadatos del PDF
                metadata = {
                    "unidad": unidad,
                    "tema": tema,
                    "source": pdf_path,
                    "total_pages": len(pdf_reader.pages),
                    "total_tokens": self.count_tokens(text)
                }
                
                # Dividir en chunks
                chunks = self.split_text_into_chunks(text, metadata)
                
                print(f"✅ PDF procesado: {pdf_path}")
                print(f"   - Total tokens: {metadata['total_tokens']}")
                print(f"   - Chunks creados: {len(chunks)}")
                print(f"   - Tamaño promedio por chunk: {metadata['total_tokens'] // len(chunks)} tokens")
                
                return chunks
                
        except Exception as e:
            print(f"❌ Error procesando {pdf_path}: {str(e)}")
            return []
    
    def process_all_pdfs(self, pdfs_dir: str = "pdfs_curso") -> List[Dict[str, Any]]:
        """
        Procesar todos los PDFs del directorio
        
        Args:
            pdfs_dir: Directorio con los PDFs del curso
            
        Returns:
            Lista de todos los chunks de todos los PDFs
        """
        all_chunks = []
        pdf_files = {
            "Contenidos_Unidad_1_PAC.pdf": {"unidad": 1, "tema": "conceptos_basicos_iso9001"},
            "Contenidos_Unidad_2_PAC.pdf": {"unidad": 2, "tema": "auditorias_certificaciones"},
            "Contenidos_Unidad_3_PAC.pdf": {"unidad": 3, "tema": "plan_aseguramiento_obras_publicas"}
        }
        
        for pdf_file, info in pdf_files.items():
            pdf_path = os.path.join(pdfs_dir, pdf_file)
            if os.path.exists(pdf_path):
                chunks = self.process_pdf(pdf_path, info["unidad"], info["tema"])
                all_chunks.extend(chunks)
            else:
                print(f"⚠️  PDF no encontrado: {pdf_path}")
        
        return all_chunks
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_file: str = "pdf_chunks.json"):
        """
        Guardar chunks en archivo JSON
        
        Args:
            chunks: Lista de chunks a guardar
            output_file: Archivo de salida
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Chunks guardados en: {output_file}")
            print(f"   - Total chunks: {len(chunks)}")
            
        except Exception as e:
            print(f"❌ Error guardando chunks: {str(e)}")

def main():
    """Función principal para ejecutar el preprocesamiento"""
    print("🚀 Iniciando preprocesamiento de PDFs del curso PAC...")
    
    # Crear preprocesador
    preprocessor = PDFPreprocessor(chunk_size=800, overlap=100)
    
    # Procesar todos los PDFs
    all_chunks = preprocessor.process_all_pdfs()
    
    if all_chunks:
        # Guardar chunks en archivo JSON
        preprocessor.save_chunks(all_chunks)
        
        # Estadísticas finales
        total_tokens = sum(chunk["tokens"] for chunk in all_chunks)
        avg_chunk_size = total_tokens // len(all_chunks)
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   - Total chunks: {len(all_chunks)}")
        print(f"   - Total tokens: {total_tokens}")
        print(f"   - Tamaño promedio por chunk: {avg_chunk_size} tokens")
        print(f"   - Archivo de salida: pdf_chunks.json")
        
    else:
        print("❌ No se pudieron procesar los PDFs")

if __name__ == "__main__":
    main()
