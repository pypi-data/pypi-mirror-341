"""
NLP task detection for SBYB.

This module provides specialized components for detecting NLP tasks.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
import os
import re

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError


class NLPDetector(SBYBComponent):
    """
    NLP task detection component.
    
    This component specializes in detecting natural language processing tasks.
    """
    
    NLP_TASKS = [
        'text_classification',
        'sentiment_analysis',
        'named_entity_recognition',
        'text_generation',
        'summarization',
        'translation',
        'question_answering',
        'text_regression'
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the NLP detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: Union[pd.DataFrame, str], text_column: Optional[str] = None, 
               target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect if the data represents an NLP task and identify the specific task type.
        
        Args:
            data: Input data or path to text data.
            text_column: Column name containing text data (if data is a DataFrame).
            target: Target variable name or index (if applicable).
            
        Returns:
            Dictionary with detection results:
                - is_nlp: Whether the task is an NLP task
                - task_type: Specific NLP task type
                - confidence: Confidence score for the detection
                - details: Additional details about the detection
        """
        # Handle different input types
        if isinstance(data, str):
            # Path to a file or directory
            return self._detect_from_path(data, target)
        elif isinstance(data, pd.DataFrame):
            # DataFrame with text data
            return self._detect_from_dataframe(data, text_column, target)
        else:
            raise TaskDetectionError(f"Unsupported data type for NLP detection: {type(data)}")
    
    def _detect_from_path(self, path: str, target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect NLP task from a file or directory path.
        
        Args:
            path: Path to file or directory.
            target: Target variable name or index (if applicable).
            
        Returns:
            Dictionary with detection results.
        """
        if os.path.isdir(path):
            # Directory with text files
            # Check for common NLP dataset structures
            subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            
            if len(subdirs) > 0:
                # Likely a text classification dataset with subdirectories for classes
                return {
                    'is_nlp': True,
                    'task_type': 'text_classification',
                    'confidence': 0.8,
                    'details': {
                        'n_classes': len(subdirs),
                        'classes': subdirs,
                        'data_source': 'directory'
                    }
                }
            else:
                # Generic text data
                return {
                    'is_nlp': True,
                    'task_type': 'text_classification',  # Default assumption
                    'confidence': 0.6,
                    'details': {
                        'data_source': 'directory',
                        'note': 'No clear class structure, defaulting to text classification'
                    }
                }
        else:
            # Single file
            file_extension = os.path.splitext(path)[1].lower()
            
            if file_extension in ['.txt', '.csv', '.json', '.xml']:
                # Try to read a sample of the file to determine content
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        sample = f.read(10000)  # Read first 10KB
                    
                    # Check for common patterns
                    has_long_text = any(len(line) > 100 for line in sample.split('\n') if line.strip())
                    has_qa_pattern = '?' in sample and len(re.findall(r'\?\s+[A-Z]', sample)) > 0
                    has_sentiment_words = any(word in sample.lower() for word in ['positive', 'negative', 'sentiment', 'rating', 'stars'])
                    
                    if has_qa_pattern:
                        task_type = 'question_answering'
                        confidence = 0.7
                    elif has_sentiment_words:
                        task_type = 'sentiment_analysis'
                        confidence = 0.7
                    elif has_long_text:
                        task_type = 'summarization'
                        confidence = 0.6
                    else:
                        task_type = 'text_classification'
                        confidence = 0.5
                    
                    return {
                        'is_nlp': True,
                        'task_type': task_type,
                        'confidence': confidence,
                        'details': {
                            'data_source': 'file',
                            'file_type': file_extension,
                            'has_long_text': has_long_text,
                            'has_qa_pattern': has_qa_pattern,
                            'has_sentiment_words': has_sentiment_words
                        }
                    }
                except:
                    # If reading fails, return a generic result
                    return {
                        'is_nlp': True,
                        'task_type': 'text_classification',  # Default assumption
                        'confidence': 0.5,
                        'details': {
                            'data_source': 'file',
                            'file_type': file_extension,
                            'note': 'Could not analyze file content'
                        }
                    }
            else:
                return {
                    'is_nlp': False,
                    'confidence': 0.7,
                    'details': {
                        'reason': f'Unsupported file type for NLP: {file_extension}',
                        'data_source': 'file'
                    }
                }
    
    def _detect_from_dataframe(self, data: pd.DataFrame, text_column: Optional[str] = None, 
                              target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect NLP task from a DataFrame.
        
        Args:
            data: Input DataFrame.
            text_column: Column name containing text data.
            target: Target variable name or index (if applicable).
            
        Returns:
            Dictionary with detection results.
        """
        # If text_column is not specified, try to find it
        if text_column is None:
            text_column = self._find_text_column(data)
            
            if text_column is None:
                return {
                    'is_nlp': False,
                    'confidence': 0.8,
                    'details': {
                        'reason': 'No suitable text column found in the DataFrame'
                    }
                }
        
        # Verify that the text column exists
        if text_column not in data.columns:
            return {
                'is_nlp': False,
                'confidence': 0.9,
                'details': {
                    'reason': f'Specified text column "{text_column}" not found in the DataFrame'
                }
            }
        
        # Analyze text characteristics
        text_data = data[text_column].astype(str)
        avg_length = text_data.str.len().mean()
        max_length = text_data.str.len().max()
        has_long_text = avg_length > 100 or max_length > 500
        
        # If target is specified, determine the task type
        if target is not None:
            # Extract target variable
            if isinstance(target, int):
                y = data.iloc[:, target]
                target_name = data.columns[target]
            else:
                y = data[target]
                target_name = target
            
            # Check if it's classification or regression
            is_categorical = pd.api.types.is_categorical_dtype(y.dtype) or pd.api.types.is_string_dtype(y.dtype)
            n_unique = y.nunique()
            is_classification = is_categorical or (pd.api.types.is_numeric_dtype(y.dtype) and n_unique <= min(10, len(y) * 0.05))
            
            if is_classification:
                # Check for sentiment analysis patterns
                has_sentiment_pattern = any(col.lower() in ['sentiment', 'rating', 'stars', 'score', 'emotion'] 
                                           for col in data.columns)
                
                if has_sentiment_pattern:
                    task_type = 'sentiment_analysis'
                    confidence = 0.8
                else:
                    task_type = 'text_classification'
                    confidence = 0.9
                
                return {
                    'is_nlp': True,
                    'task_type': task_type,
                    'confidence': confidence,
                    'details': {
                        'text_column': text_column,
                        'target_column': target_name,
                        'n_classes': n_unique,
                        'avg_text_length': avg_length,
                        'has_long_text': has_long_text,
                        'has_sentiment_pattern': has_sentiment_pattern if 'has_sentiment_pattern' in locals() else False
                    }
                }
            else:
                # Regression task
                return {
                    'is_nlp': True,
                    'task_type': 'text_regression',
                    'confidence': 0.9,
                    'details': {
                        'text_column': text_column,
                        'target_column': target_name,
                        'avg_text_length': avg_length,
                        'has_long_text': has_long_text
                    }
                }
        
        # If no target is specified, try to guess the task type from text characteristics
        has_qa_pattern = text_data.str.contains('\?').mean() > 0.2
        has_sentiment_words = text_data.str.contains('positive|negative|good|bad|excellent|terrible', 
                                                    case=False).mean() > 0.1
        
        if has_qa_pattern:
            task_type = 'question_answering'
            confidence = 0.7
        elif has_sentiment_words:
            task_type = 'sentiment_analysis'
            confidence = 0.7
        elif has_long_text:
            task_type = 'summarization'
            confidence = 0.6
        else:
            task_type = 'text_classification'
            confidence = 0.5
        
        return {
            'is_nlp': True,
            'task_type': task_type,
            'confidence': confidence,
            'details': {
                'text_column': text_column,
                'avg_text_length': avg_length,
                'has_long_text': has_long_text,
                'has_qa_pattern': has_qa_pattern,
                'has_sentiment_words': has_sentiment_words
            }
        }
    
    def _find_text_column(self, data: pd.DataFrame) -> Optional[str]:
        """
        Find the most likely text column in a DataFrame.
        
        Args:
            data: Input DataFrame.
            
        Returns:
            Name of the most likely text column, or None if no suitable column is found.
        """
        # Look for columns with string data type
        string_columns = [col for col in data.columns if pd.api.types.is_string_dtype(data[col].dtype)]
        
        if not string_columns:
            return None
        
        # Calculate average string length for each column
        avg_lengths = {}
        for col in string_columns:
            avg_lengths[col] = data[col].astype(str).str.len().mean()
        
        # Look for columns with common text-related names
        text_related_names = ['text', 'content', 'description', 'summary', 'comment', 'review', 'message', 'document']
        for name in text_related_names:
            for col in string_columns:
                if name in col.lower():
                    # If the column name contains a text-related term and has reasonable length, return it
                    if avg_lengths[col] > 20:
                        return col
        
        # If no column with text-related name is found, return the column with the longest average string length
        if avg_lengths:
            best_col = max(avg_lengths.items(), key=lambda x: x[1])
            if best_col[1] > 20:  # Only return if average length is reasonable
                return best_col[0]
        
        return None
    
    def suggest_preprocessing(self, data: Union[pd.DataFrame, str], text_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Suggest preprocessing steps for the text data.
        
        Args:
            data: Input data or path to text data.
            text_column: Column name containing text data (if data is a DataFrame).
            
        Returns:
            Dictionary with suggested preprocessing steps.
        """
        # Get text data
        if isinstance(data, str):
            # For simplicity, just return general recommendations for file paths
            return {
                'suggested_steps': [
                    'tokenization',
                    'lowercasing',
                    'stopword_removal',
                    'stemming_or_lemmatization',
                    'vectorization'
                ],
                'vectorization_methods': [
                    {'method': 'tfidf', 'suitability': 'high'},
                    {'method': 'count', 'suitability': 'medium'},
                    {'method': 'word_embeddings', 'suitability': 'high'}
                ]
            }
        
        elif isinstance(data, pd.DataFrame):
            # If text_column is not specified, try to find it
            if text_column is None:
                text_column = self._find_text_column(data)
                
                if text_column is None:
                    return {
                        'error': 'No suitable text column found in the DataFrame'
                    }
            
            # Verify that the text column exists
            if text_column not in data.columns:
                return {
                    'error': f'Specified text column "{text_column}" not found in the DataFrame'
                }
            
            # Analyze text characteristics
            text_data = data[text_column].astype(str)
            avg_length = text_data.str.len().mean()
            max_length = text_data.str.len().max()
            has_long_text = avg_length > 100 or max_length > 500
            
            # Check for uppercase text
            uppercase_ratio = text_data.str.count(r'[A-Z]').sum() / text_data.str.count(r'[a-zA-Z]').sum()
            needs_lowercasing = uppercase_ratio > 0.2
            
            # Check for punctuation
            punctuation_ratio = text_data.str.count(r'[^\w\s]').sum() / text_data.str.len().sum()
            has_punctuation = punctuation_ratio > 0.05
            
            # Check for numbers
            number_ratio = text_data.str.count(r'\d').sum() / text_data.str.len().sum()
            has_numbers = number_ratio > 0.05
            
            # Suggest preprocessing steps
            steps = ['tokenization']
            
            if needs_lowercasing:
                steps.append('lowercasing')
            
            if has_punctuation:
                steps.append('punctuation_removal')
            
            if has_numbers and number_ratio < 0.2:  # If not too many numbers
                steps.append('number_removal')
            
            steps.extend(['stopword_removal', 'stemming_or_lemmatization'])
            
            # Suggest vectorization methods
            vectorization_methods = []
            
            if has_long_text:
                vectorization_methods.append({'method': 'tfidf', 'suitability': 'high'})
                vectorization_methods.append({'method': 'word_embeddings', 'suitability': 'high'})
                vectorization_methods.append({'method': 'count', 'suitability': 'low'})
            else:
                vectorization_methods.append({'method': 'tfidf', 'suitability': 'high'})
                vectorization_methods.append({'method': 'count', 'suitability': 'medium'})
                vectorization_methods.append({'method': 'word_embeddings', 'suitability': 'medium'})
            
            return {
                'suggested_steps': steps,
                'vectorization_methods': vectorization_methods,
                'details': {
                    'text_column': text_column,
                    'avg_length': avg_length,
                    'max_length': max_length,
                    'has_long_text': has_long_text,
                    'uppercase_ratio': uppercase_ratio,
                    'punctuation_ratio': punctuation_ratio,
                    'number_ratio': number_ratio
                }
            }
        
        else:
            return {
                'error': f'Unsupported data type for NLP preprocessing suggestions: {type(data)}'
            }
