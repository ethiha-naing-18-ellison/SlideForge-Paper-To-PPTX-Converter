# -*- coding: utf-8 -*-
"""Advanced NLP content generator for high-quality slide content."""

from __future__ import annotations
import re
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

class ContentGenerator:
    """Advanced content generator for creating meaningful slide content."""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.section_templates = {
            "ABSTRACT": self._generate_abstract_content,
            "INTRODUCTION": self._generate_introduction_content,
            "LITERATURE": self._generate_literature_content,
            "METHODS": self._generate_methods_content,
            "RESULTS": self._generate_results_content,
            "DISCUSSION": self._generate_discussion_content,
            "CONCLUSION": self._generate_conclusion_content
        }
    
    def generate_section_content(self, section_name: str, raw_text: str, target_bullets: int = 6) -> List[str]:
        """Generate high-quality content for a specific section."""
        # Clean and preprocess the text
        cleaned_text = self._preprocess_text(raw_text)
        
        # Extract key information
        key_phrases = self._extract_key_phrases(cleaned_text)
        main_topics = self._identify_main_topics(cleaned_text)
        important_sentences = self._extract_important_sentences(cleaned_text)
        
        # Generate content based on section type
        if section_name in self.section_templates:
            return self.section_templates[section_name](
                cleaned_text, key_phrases, main_topics, important_sentences, target_bullets
            )
        else:
            return self._generate_general_content(
                cleaned_text, key_phrases, main_topics, important_sentences, target_bullets
            )
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common grammar issues
        text = re.sub(r'(\w)([A-Z][a-z])', r'\1 \2', text)  # Add space between camelCase
        text = re.sub(r'(\w)(\d)', r'\1 \2', text)  # Add space between word and number
        text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Add space between number and word
        
        # Fix specific issues
        text = text.replace("Proposed ModelHRbSBM", "Proposed Model HRbSBM")
        text = text.replace("This proposedmodel", "This proposed model")
        text = text.replace("Hand Recognition Based", "Hand Recognition-Based")
        text = text.replace("LITERATURE REVIEWThe", "LITERATURE REVIEW The")
        text = text.replace("Due tothe", "Due to the")
        text = text.replace("Due toits", "Due to its")
        text = text.replace("In thecurrent", "In the current")
        
        return text
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract important key phrases from text."""
        sentences = sent_tokenize(text)
        key_phrases = []
        
        for sentence in sentences:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(sentence.lower())
            pos_tags = pos_tag(tokens)
            
            # Extract noun phrases and important terms
            phrases = []
            current_phrase = []
            
            for token, tag in pos_tags:
                if tag.startswith('NN') or tag.startswith('JJ'):  # Nouns and adjectives
                    if token not in self.stop_words and len(token) > 2:
                        current_phrase.append(token)
                else:
                    if current_phrase:
                        phrases.append(' '.join(current_phrase))
                        current_phrase = []
            
            if current_phrase:
                phrases.append(' '.join(current_phrase))
            
            key_phrases.extend(phrases)
        
        # Return most common phrases
        phrase_counts = Counter(key_phrases)
        return [phrase for phrase, count in phrase_counts.most_common(10)]
    
    def _identify_main_topics(self, text: str) -> List[str]:
        """Identify main topics and themes in the text."""
        sentences = sent_tokenize(text)
        topics = []
        
        # Look for topic indicators
        topic_indicators = [
            'focus', 'aim', 'objective', 'goal', 'purpose', 'target',
            'problem', 'challenge', 'issue', 'solution', 'approach',
            'method', 'technique', 'system', 'model', 'framework'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for indicator in topic_indicators:
                if indicator in sentence_lower:
                    # Extract the topic from the sentence
                    words = word_tokenize(sentence)
                    for i, word in enumerate(words):
                        if indicator in word.lower():
                            # Get surrounding context
                            start = max(0, i-3)
                            end = min(len(words), i+4)
                            topic = ' '.join(words[start:end])
                            topics.append(topic)
                            break
        
        return list(set(topics))[:5]  # Return unique topics
    
    def _extract_important_sentences(self, text: str) -> List[str]:
        """Extract the most important sentences based on content and structure."""
        sentences = sent_tokenize(text)
        scored_sentences = []
        
        for sentence in sentences:
            score = 0
            
            # Score based on length (prefer medium-length sentences)
            words = word_tokenize(sentence)
            if 10 <= len(words) <= 25:
                score += 2
            elif 5 <= len(words) <= 30:
                score += 1
            
            # Score based on content indicators
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in ['propose', 'develop', 'implement', 'design']):
                score += 3
            if any(word in sentence_lower for word in ['result', 'find', 'show', 'demonstrate']):
                score += 3
            if any(word in sentence_lower for word in ['benefit', 'advantage', 'improve', 'enhance']):
                score += 2
            if any(word in sentence_lower for word in ['problem', 'challenge', 'issue']):
                score += 2
            
            # Score based on technical terms
            technical_terms = ['system', 'model', 'algorithm', 'technology', 'method', 'approach']
            if any(term in sentence_lower for term in technical_terms):
                score += 1
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, score in scored_sentences[:10]]
    
    def _generate_abstract_content(self, text: str, key_phrases: List[str], 
                                 main_topics: List[str], important_sentences: List[str], 
                                 target_bullets: int) -> List[str]:
        """Generate content for Abstract section."""
        bullets = []
        
        # Extract the main problem/objective
        problem_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['problem', 'challenge', 'issue', 'need'])]
        if problem_sentences:
            bullets.append(f"**Problem Statement:** {self._clean_sentence(problem_sentences[0])}")
        
        # Extract the proposed solution
        solution_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['propose', 'develop', 'design', 'implement'])]
        if solution_sentences:
            bullets.append(f"**Proposed Solution:** {self._clean_sentence(solution_sentences[0])}")
        
        # Extract key benefits
        benefit_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['benefit', 'advantage', 'improve', 'enhance'])]
        if benefit_sentences:
            bullets.append(f"**Key Benefits:** {self._clean_sentence(benefit_sentences[0])}")
        
        # Extract methodology overview
        method_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['method', 'approach', 'technique', 'algorithm'])]
        if method_sentences:
            bullets.append(f"**Methodology:** {self._clean_sentence(method_sentences[0])}")
        
        # Extract results/outcomes
        result_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['result', 'outcome', 'performance', 'evaluation'])]
        if result_sentences:
            bullets.append(f"**Key Results:** {self._clean_sentence(result_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_introduction_content(self, text: str, key_phrases: List[str], 
                                     main_topics: List[str], important_sentences: List[str], 
                                     target_bullets: int) -> List[str]:
        """Generate content for Introduction section."""
        bullets = []
        
        # Background and motivation
        background_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['background', 'motivation', 'context', 'current'])]
        if background_sentences:
            bullets.append(f"**Background:** {self._clean_sentence(background_sentences[0])}")
        
        # Problem statement
        problem_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['problem', 'challenge', 'issue', 'limitation'])]
        if problem_sentences:
            bullets.append(f"**Problem Statement:** {self._clean_sentence(problem_sentences[0])}")
        
        # Research objectives
        objective_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['objective', 'goal', 'aim', 'purpose'])]
        if objective_sentences:
            bullets.append(f"**Research Objectives:** {self._clean_sentence(objective_sentences[0])}")
        
        # Proposed approach
        approach_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['approach', 'method', 'solution', 'propose'])]
        if approach_sentences:
            bullets.append(f"**Proposed Approach:** {self._clean_sentence(approach_sentences[0])}")
        
        # Expected contributions
        contribution_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['contribution', 'benefit', 'impact', 'significance'])]
        if contribution_sentences:
            bullets.append(f"**Expected Contributions:** {self._clean_sentence(contribution_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_literature_content(self, text: str, key_phrases: List[str], 
                                   main_topics: List[str], important_sentences: List[str], 
                                   target_bullets: int) -> List[str]:
        """Generate content for Literature Review section."""
        bullets = []
        
        # Current state of technology
        current_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['current', 'existing', 'traditional', 'conventional'])]
        if current_sentences:
            bullets.append(f"**Current State:** {self._clean_sentence(current_sentences[0])}")
        
        # Related work
        related_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['related', 'previous', 'existing work', 'literature'])]
        if related_sentences:
            bullets.append(f"**Related Work:** {self._clean_sentence(related_sentences[0])}")
        
        # Technology trends
        trend_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['trend', 'development', 'advancement', 'evolution'])]
        if trend_sentences:
            bullets.append(f"**Technology Trends:** {self._clean_sentence(trend_sentences[0])}")
        
        # Challenges and limitations
        challenge_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['challenge', 'limitation', 'drawback', 'issue'])]
        if challenge_sentences:
            bullets.append(f"**Challenges:** {self._clean_sentence(challenge_sentences[0])}")
        
        # Research gaps
        gap_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['gap', 'need', 'requirement', 'opportunity'])]
        if gap_sentences:
            bullets.append(f"**Research Gaps:** {self._clean_sentence(gap_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_methods_content(self, text: str, key_phrases: List[str], 
                                main_topics: List[str], important_sentences: List[str], 
                                target_bullets: int) -> List[str]:
        """Generate content for Methods section."""
        bullets = []
        
        # System architecture
        architecture_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['architecture', 'design', 'structure', 'framework'])]
        if architecture_sentences:
            bullets.append(f"**System Architecture:** {self._clean_sentence(architecture_sentences[0])}")
        
        # Methodology
        method_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['method', 'methodology', 'approach', 'technique'])]
        if method_sentences:
            bullets.append(f"**Methodology:** {self._clean_sentence(method_sentences[0])}")
        
        # Implementation details
        implementation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['implement', 'develop', 'create', 'build'])]
        if implementation_sentences:
            bullets.append(f"**Implementation:** {self._clean_sentence(implementation_sentences[0])}")
        
        # Tools and technologies
        tool_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['tool', 'technology', 'software', 'platform'])]
        if tool_sentences:
            bullets.append(f"**Tools & Technologies:** {self._clean_sentence(tool_sentences[0])}")
        
        # Data collection
        data_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['data', 'dataset', 'collection', 'gathering'])]
        if data_sentences:
            bullets.append(f"**Data Collection:** {self._clean_sentence(data_sentences[0])}")
        
        # Evaluation metrics
        evaluation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['evaluation', 'metric', 'measure', 'assessment'])]
        if evaluation_sentences:
            bullets.append(f"**Evaluation Metrics:** {self._clean_sentence(evaluation_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_results_content(self, text: str, key_phrases: List[str], 
                                main_topics: List[str], important_sentences: List[str], 
                                target_bullets: int) -> List[str]:
        """Generate content for Results section."""
        bullets = []
        
        # Performance results
        performance_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['performance', 'result', 'outcome', 'achievement'])]
        if performance_sentences:
            bullets.append(f"**Performance Results:** {self._clean_sentence(performance_sentences[0])}")
        
        # Key findings
        finding_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['finding', 'discovery', 'observation', 'analysis'])]
        if finding_sentences:
            bullets.append(f"**Key Findings:** {self._clean_sentence(finding_sentences[0])}")
        
        # Comparative analysis
        comparison_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['compare', 'versus', 'better', 'improvement'])]
        if comparison_sentences:
            bullets.append(f"**Comparative Analysis:** {self._clean_sentence(comparison_sentences[0])}")
        
        # User feedback
        feedback_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['feedback', 'user', 'experience', 'satisfaction'])]
        if feedback_sentences:
            bullets.append(f"**User Feedback:** {self._clean_sentence(feedback_sentences[0])}")
        
        # System evaluation
        evaluation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['evaluation', 'assessment', 'testing', 'validation'])]
        if evaluation_sentences:
            bullets.append(f"**System Evaluation:** {self._clean_sentence(evaluation_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_discussion_content(self, text: str, key_phrases: List[str], 
                                   main_topics: List[str], important_sentences: List[str], 
                                   target_bullets: int) -> List[str]:
        """Generate content for Discussion section."""
        bullets = []
        
        # Interpretation of results
        interpretation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['interpret', 'explain', 'understand', 'meaning'])]
        if interpretation_sentences:
            bullets.append(f"**Result Interpretation:** {self._clean_sentence(interpretation_sentences[0])}")
        
        # Implications
        implication_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['implication', 'impact', 'significance', 'consequence'])]
        if implication_sentences:
            bullets.append(f"**Implications:** {self._clean_sentence(implication_sentences[0])}")
        
        # Limitations
        limitation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['limitation', 'constraint', 'drawback', 'weakness'])]
        if limitation_sentences:
            bullets.append(f"**Limitations:** {self._clean_sentence(limitation_sentences[0])}")
        
        # Future work
        future_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['future', 'next', 'improvement', 'enhancement'])]
        if future_sentences:
            bullets.append(f"**Future Work:** {self._clean_sentence(future_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_conclusion_content(self, text: str, key_phrases: List[str], 
                                   main_topics: List[str], important_sentences: List[str], 
                                   target_bullets: int) -> List[str]:
        """Generate content for Conclusion section."""
        bullets = []
        
        # Summary of contributions
        contribution_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['contribution', 'achievement', 'accomplishment', 'success'])]
        if contribution_sentences:
            bullets.append(f"**Key Contributions:** {self._clean_sentence(contribution_sentences[0])}")
        
        # Main findings
        finding_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['finding', 'result', 'outcome', 'conclusion'])]
        if finding_sentences:
            bullets.append(f"**Main Findings:** {self._clean_sentence(finding_sentences[0])}")
        
        # Impact and significance
        impact_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['impact', 'significance', 'importance', 'value'])]
        if impact_sentences:
            bullets.append(f"**Impact & Significance:** {self._clean_sentence(impact_sentences[0])}")
        
        # Future directions
        future_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['future', 'direction', 'recommendation', 'suggestion'])]
        if future_sentences:
            bullets.append(f"**Future Directions:** {self._clean_sentence(future_sentences[0])}")
        
        return bullets[:target_bullets]
    
    def _generate_general_content(self, text: str, key_phrases: List[str], 
                                main_topics: List[str], important_sentences: List[str], 
                                target_bullets: int) -> List[str]:
        """Generate general content for any section."""
        bullets = []
        
        # Use the most important sentences
        for i, sentence in enumerate(important_sentences[:target_bullets]):
            cleaned_sentence = self._clean_sentence(sentence)
            if cleaned_sentence:
                bullets.append(f"**Point {i+1}:** {cleaned_sentence}")
        
        return bullets
    
    def _clean_sentence(self, sentence: str) -> str:
        """Clean and format a sentence for presentation."""
        # Remove extra whitespace
        sentence = re.sub(r'\s+', ' ', sentence.strip())
        
        # Ensure proper capitalization
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]
        
        # Ensure proper ending
        if sentence and not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        
        return sentence
