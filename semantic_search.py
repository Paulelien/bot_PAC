"""
Sistema de búsqueda semántica para chunks del curso PAC
Encuentra los chunks más relevantes para cada pregunta del estudiante
"""

import json
import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class SemanticSearch:
    def __init__(self, chunks_file: str = "pdf_chunks.json"):
        """
        Inicializar sistema de búsqueda semántica
        
        Args:
            chunks_file: Archivo JSON con los chunks preprocesados
        """
        self.chunks_file = chunks_file
        self.chunks = []
        self.vectorizer = None
        self.chunk_vectors = None
        
        # Cargar chunks si existen
        if os.path.exists(chunks_file):
            self.load_chunks()
            self.create_embeddings()
    
    def load_chunks(self):
        """Cargar chunks desde archivo JSON"""
        try:
            with open(self.chunks_file, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
            print(f"✅ Cargados {len(self.chunks)} chunks desde {self.chunks_file}")
        except Exception as e:
            print(f"❌ Error cargando chunks: {str(e)}")
            self.chunks = []
    
    def create_embeddings(self):
        """Crear embeddings TF-IDF para todos los chunks"""
        if not self.chunks:
            print("⚠️  No hay chunks para crear embeddings")
            return
        
        try:
            # Extraer contenido de los chunks
            chunk_texts = [chunk["content"] for chunk in self.chunks]
            
            # Crear vectorizador TF-IDF
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2
            )
            
            # Crear matriz de embeddings
            self.chunk_vectors = self.vectorizer.fit_transform(chunk_texts)
            
            print(f"✅ Embeddings creados para {len(self.chunks)} chunks")
            print(f"   - Dimensiones: {self.chunk_vectors.shape}")
            
        except Exception as e:
            print(f"❌ Error creando embeddings: {str(e)}")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Buscar chunks más relevantes para una consulta
        
        Args:
            query: Pregunta del estudiante
            top_k: Número de chunks más relevantes a retornar
            
        Returns:
            Lista de chunks más relevantes ordenados por relevancia
        """
        if not self.chunks or self.vectorizer is None or self.chunk_vectors is None:
            print("⚠️  Sistema de búsqueda no inicializado")
            return []
        
        try:
            # Vectorizar la consulta
            query_vector = self.vectorizer.transform([query])
            
            # Calcular similitud coseno
            similarities = cosine_similarity(query_vector, self.chunk_vectors).flatten()
            
            # Obtener índices de los chunks más similares
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            # Crear resultados con información de relevancia
            results = []
            for idx in top_indices:
                chunk = self.chunks[idx].copy()
                chunk["relevance_score"] = float(similarities[idx])
                chunk["similarity_percentage"] = round(similarities[idx] * 100, 2)
                results.append(chunk)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            print(f"🔍 Búsqueda para: '{query}'")
            print(f"   - Chunks encontrados: {len(results)}")
            print(f"   - Mejor relevancia: {results[0]['similarity_percentage']}%")
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {str(e)}")
            return []
    
    def search_by_topic(self, topic: str, unidad: int = None) -> List[Dict[str, Any]]:
        """
        Buscar chunks por tema específico
        
        Args:
            topic: Tema a buscar (ej: "ISO 9001", "evolución")
            unidad: Unidad específica (opcional)
            
        Returns:
            Lista de chunks relacionados con el tema
        """
        if not self.chunks:
            return []
        
        relevant_chunks = []
        topic_lower = topic.lower()
        
        for chunk in self.chunks:
            # Filtrar por unidad si se especifica
            if unidad and chunk["metadata"]["unidad"] != unidad:
                continue
            
            # Buscar tema en contenido y metadatos
            content_lower = chunk["content"].lower()
            metadata_lower = str(chunk["metadata"]).lower()
            
            if topic_lower in content_lower or topic_lower in metadata_lower:
                chunk_copy = chunk.copy()
                chunk_copy["relevance_score"] = 1.0
                chunk_copy["similarity_percentage"] = 100.0
                relevant_chunks.append(chunk_copy)
        
        # Ordenar por relevancia
        relevant_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        print(f"🔍 Búsqueda por tema: '{topic}'")
        print(f"   - Chunks encontrados: {len(relevant_chunks)}")
        if unidad:
            print(f"   - Filtrado por Unidad {unidad}")
        
        return relevant_chunks
    
    def get_chunk_by_id(self, chunk_id: str) -> Dict[str, Any]:
        """
        Obtener un chunk específico por ID
        
        Args:
            chunk_id: ID único del chunk
            
        Returns:
            Chunk específico o None si no se encuentra
        """
        for chunk in self.chunks:
            if chunk["id"] == chunk_id:
                return chunk
        return None
    
    def get_chunks_by_unidad(self, unidad: int) -> List[Dict[str, Any]]:
        """
        Obtener todos los chunks de una unidad específica
        
        Args:
            unidad: Número de unidad
            
        Returns:
            Lista de chunks de la unidad
        """
        return [chunk for chunk in self.chunks if chunk["metadata"]["unidad"] == unidad]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas del sistema de búsqueda
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.chunks:
            return {}
        
        total_tokens = sum(chunk["tokens"] for chunk in self.chunks)
        avg_chunk_size = total_tokens // len(self.chunks)
        
        unidades = {}
        for chunk in self.chunks:
            unidad = chunk["metadata"]["unidad"]
            if unidad not in unidades:
                unidades[unidad] = {"chunks": 0, "tokens": 0}
            unidades[unidad]["chunks"] += 1
            unidades[unidad]["tokens"] += chunk["tokens"]
        
        return {
            "total_chunks": len(self.chunks),
            "total_tokens": total_tokens,
            "avg_chunk_size": avg_chunk_size,
            "unidades": unidades,
            "embeddings_created": self.vectorizer is not None
        }

def main():
    """Función principal para probar el sistema de búsqueda"""
    print("🔍 Iniciando sistema de búsqueda semántica...")
    
    # Crear sistema de búsqueda
    search_system = SemanticSearch()
    
    if not search_system.chunks:
        print("❌ No hay chunks disponibles. Ejecuta pdf_preprocessor.py primero.")
        return
    
    # Mostrar estadísticas
    stats = search_system.get_statistics()
    print(f"\n📊 Estadísticas del sistema:")
    print(f"   - Total chunks: {stats['total_chunks']}")
    print(f"   - Total tokens: {stats['total_tokens']}")
    print(f"   - Tamaño promedio: {stats['avg_chunk_size']} tokens")
    print(f"   - Embeddings creados: {stats['embeddings_created']}")
    
    # Ejemplo de búsqueda
    test_query = "evolución de la norma ISO 9001"
    print(f"\n🧪 Prueba de búsqueda: '{test_query}'")
    
    results = search_system.search(test_query, top_k=3)
    for i, chunk in enumerate(results, 1):
        print(f"\n   {i}. Chunk ID: {chunk['id']}")
        print(f"      Relevancia: {chunk['similarity_percentage']}%")
        print(f"      Unidad: {chunk['metadata']['unidad']}")
        print(f"      Tokens: {chunk['tokens']}")
        print(f"      Contenido: {chunk['content'][:100]}...")

if __name__ == "__main__":
    main()
