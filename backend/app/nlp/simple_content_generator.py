# -*- coding: utf-8 -*-
"""Simple but effective content generator for high-quality slide content."""

from __future__ import annotations
import re
from typing import List, Dict
from collections import Counter

class SimpleContentGenerator:
    """Simple but effective content generator for creating meaningful slide content."""
    
    def __init__(self):
        self.section_templates = {
            "ABSTRACT": self._generate_abstract_content,
            "INTRODUCTION": self._generate_introduction_content,
            "BACKGROUND": self._generate_background_content,
            "PROBLEM_STATEMENT": self._generate_problem_statement_content,
            "PROPOSED_APPROACH": self._generate_proposed_approach_content,
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
        important_sentences = self._extract_important_sentences(cleaned_text)
        
        # Generate content based on section type
        if section_name in self.section_templates:
            return self.section_templates[section_name](
                cleaned_text, important_sentences, target_bullets
            )
        else:
            return self._generate_general_content(
                cleaned_text, important_sentences, target_bullets
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
    
    def _extract_important_sentences(self, text: str) -> List[str]:
        """Extract the most important sentences based on content and structure."""
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]  # Reduced minimum length
        
        scored_sentences = []
        
        for sentence in sentences:
            score = 0
            
            # Score based on length (prefer medium-length sentences)
            words = sentence.split()
            if 8 <= len(words) <= 40:  # Increased max length
                score += 2
            elif 5 <= len(words) <= 50:  # Increased max length
                score += 1
            
            # Score based on content indicators (expanded keywords)
            sentence_lower = sentence.lower()
            
            # High-priority keywords (score +4)
            high_priority = ['propose', 'develop', 'implement', 'design', 'create', 'build', 'deploy', 'construct']
            if any(word in sentence_lower for word in high_priority):
                score += 4
                
            high_priority_results = ['result', 'find', 'show', 'demonstrate', 'achieve', 'obtain', 'achieve', 'accomplish', 'succeed']
            if any(word in sentence_lower for word in high_priority_results):
                score += 4
                
            # Medium-priority keywords (score +3)
            medium_priority = ['benefit', 'advantage', 'improve', 'enhance', 'optimize', 'upgrade', 'advance', 'progress']
            if any(word in sentence_lower for word in medium_priority):
                score += 3
                
            medium_priority_problems = ['problem', 'challenge', 'issue', 'limitation', 'constraint', 'difficulty', 'obstacle', 'barrier']
            if any(word in sentence_lower for word in medium_priority_problems):
                score += 3
                
            # Technical keywords (score +2)
            technical_terms = ['system', 'model', 'algorithm', 'technology', 'method', 'approach', 'framework', 'architecture', 'protocol', 'mechanism']
            if any(word in sentence_lower for word in technical_terms):
                score += 2
                
            domain_terms = ['cloud', 'computing', 'education', 'learning', 'teaching', 'smart', 'board', 'recognition', 'gesture', 'hand']
            if any(word in sentence_lower for word in domain_terms):
                score += 2
                
            performance_terms = ['performance', 'efficiency', 'accuracy', 'reliability', 'speed', 'quality', 'effectiveness', 'productivity']
            if any(word in sentence_lower for word in performance_terms):
                score += 2
                
            user_terms = ['user', 'interface', 'experience', 'interaction', 'usability', 'accessibility', 'satisfaction', 'feedback']
            if any(word in sentence_lower for word in user_terms):
                score += 2
                
            # Lower-priority keywords (score +1)
            data_terms = ['data', 'information', 'processing', 'analysis', 'collection', 'gathering', 'storage', 'management']
            if any(word in sentence_lower for word in data_terms):
                score += 1
                
            cost_terms = ['cost', 'budget', 'resource', 'infrastructure', 'investment', 'expense', 'saving', 'economic']
            if any(word in sentence_lower for word in cost_terms):
                score += 1
                
            # Additional technical terms
            additional_tech = ['api', 'database', 'server', 'client', 'network', 'communication', 'integration', 'deployment']
            if any(word in sentence_lower for word in additional_tech):
                score += 1
                
            # Research and evaluation terms
            research_terms = ['study', 'research', 'investigation', 'experiment', 'test', 'evaluation', 'assessment', 'validation']
            if any(word in sentence_lower for word in research_terms):
                score += 1
            
            # Objective and goal terms (higher priority)
            objective_terms = ['objective', 'goal', 'aim', 'target', 'purpose', 'intention', 'mission', 'vision', 'research aim', 'study aim']
            if any(word in sentence_lower for word in objective_terms):
                score += 3  # Higher score for objective-related content
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences (increased to 30)
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, score in scored_sentences[:30]]
    
    def _generate_abstract_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
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
    
    def _generate_introduction_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Introduction section (overview)."""
        bullets = []
        
        # Overview of the research
        overview_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['research', 'study', 'project', 'work', 'investigation'])]
        if overview_sentences:
            detailed_overview = self._create_detailed_bullet(overview_sentences, 3)
            bullets.append(f"**Research Overview:** {detailed_overview}")
        
        # Key motivation
        motivation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['motivation', 'inspire', 'drive', 'purpose', 'goal'])]
        if motivation_sentences:
            detailed_motivation = self._create_detailed_bullet(motivation_sentences, 2)
            bullets.append(f"**Key Motivation:** {detailed_motivation}")
        
        # Scope and significance
        scope_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['scope', 'significance', 'importance', 'impact', 'value'])]
        if scope_sentences:
            detailed_scope = self._create_detailed_bullet(scope_sentences, 2)
            bullets.append(f"**Scope & Significance:** {detailed_scope}")
        
        # Expected outcomes
        outcome_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['outcome', 'result', 'achievement', 'success', 'benefit'])]
        if outcome_sentences:
            detailed_outcomes = self._create_detailed_bullet(outcome_sentences, 2)
            bullets.append(f"**Expected Outcomes:** {detailed_outcomes}")
        
        return bullets[:target_bullets]
    
    def _generate_background_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Background section."""
        bullets = []
        
        # Current state and context
        current_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['current', 'present', 'existing', 'today', 'now'])]
        if current_sentences:
            detailed_current = self._create_detailed_bullet(current_sentences, 3)
            bullets.append(f"**Current State:** {detailed_current}")
        
        # Technology trends and evolution
        trend_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['trend', 'evolution', 'development', 'advancement', 'progress'])]
        if trend_sentences:
            detailed_trends = self._create_detailed_bullet(trend_sentences, 3)
            bullets.append(f"**Technology Trends:** {detailed_trends}")
        
        # Industry context and adoption
        industry_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['industry', 'sector', 'field', 'domain', 'market'])]
        if industry_sentences:
            detailed_industry = self._create_detailed_bullet(industry_sentences, 2)
            bullets.append(f"**Industry Context:** {detailed_industry}")
        
        # Educational landscape
        education_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['education', 'learning', 'teaching', 'academic', 'institution'])]
        if education_sentences:
            detailed_education = self._create_detailed_bullet(education_sentences, 3)
            bullets.append(f"**Educational Landscape:** {detailed_education}")
        
        # Challenges in current systems
        challenge_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['challenge', 'difficulty', 'issue', 'problem', 'limitation'])]
        if challenge_sentences:
            detailed_challenges = self._create_detailed_bullet(challenge_sentences, 2)
            bullets.append(f"**Current Challenges:** {detailed_challenges}")
        
        return bullets[:target_bullets]
    
    def _generate_problem_statement_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Problem Statement & Objectives section."""
        bullets = []
        
        # Main problem identification
        problem_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['problem', 'issue', 'challenge', 'difficulty', 'obstacle'])]
        if problem_sentences:
            detailed_problem = self._create_detailed_bullet(problem_sentences, 3)
            bullets.append(f"**Main Problem:** {detailed_problem}")
        
        # Research objectives and goals
        objective_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['objective', 'goal', 'aim', 'target', 'purpose', 'intention', 'mission', 'vision'])]
        if objective_sentences:
            detailed_objectives = self._create_detailed_bullet(objective_sentences, 3)
            bullets.append(f"**Research Objectives:** {detailed_objectives}")
        
        # Impact of the problem
        impact_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['impact', 'effect', 'consequence', 'result', 'outcome'])]
        if impact_sentences:
            detailed_impact = self._create_detailed_bullet(impact_sentences, 2)
            bullets.append(f"**Problem Impact:** {detailed_impact}")
        
        # Stakeholders affected
        stakeholder_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['teacher', 'student', 'user', 'institution', 'organization'])]
        if stakeholder_sentences:
            detailed_stakeholders = self._create_detailed_bullet(stakeholder_sentences, 2)
            bullets.append(f"**Affected Stakeholders:** {detailed_stakeholders}")
        
        # Expected outcomes and deliverables
        outcome_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['outcome', 'result', 'achievement', 'deliverable', 'output', 'product', 'solution', 'system', 'model'])]
        if outcome_sentences:
            detailed_outcomes = self._create_detailed_bullet(outcome_sentences, 2)
            bullets.append(f"**Expected Outcomes:** {detailed_outcomes}")
        
        # Current limitations
        limitation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['limitation', 'constraint', 'restriction', 'drawback', 'weakness'])]
        if limitation_sentences:
            detailed_limitations = self._create_detailed_bullet(limitation_sentences, 2)
            bullets.append(f"**Current Limitations:** {detailed_limitations}")
        
        return bullets[:target_bullets]
    

    
    def _generate_proposed_approach_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Proposed Approach section."""
        bullets = []
        
        # Overall approach
        approach_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['approach', 'method', 'strategy', 'technique', 'solution'])]
        if approach_sentences:
            detailed_approach = self._create_detailed_bullet(approach_sentences, 3)
            bullets.append(f"**Overall Approach:** {detailed_approach}")
        
        # Technology selection
        technology_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['technology', 'system', 'platform', 'tool', 'framework'])]
        if technology_sentences:
            detailed_technology = self._create_detailed_bullet(technology_sentences, 3)
            bullets.append(f"**Technology Selection:** {detailed_technology}")
        
        # Implementation strategy
        implementation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['implement', 'develop', 'create', 'build', 'deploy'])]
        if implementation_sentences:
            detailed_implementation = self._create_detailed_bullet(implementation_sentences, 3)
            bullets.append(f"**Implementation Strategy:** {detailed_implementation}")
        
        # Key features and capabilities
        feature_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['feature', 'capability', 'function', 'ability', 'characteristic'])]
        if feature_sentences:
            detailed_features = self._create_detailed_bullet(feature_sentences, 2)
            bullets.append(f"**Key Features:** {detailed_features}")
        
        # Advantages and benefits
        advantage_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['advantage', 'benefit', 'improvement', 'enhancement', 'superior'])]
        if advantage_sentences:
            detailed_advantages = self._create_detailed_bullet(advantage_sentences, 2)
            bullets.append(f"**Advantages & Benefits:** {detailed_advantages}")
        
        # Innovation aspects
        innovation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['innovation', 'novel', 'unique', 'original', 'creative'])]
        if innovation_sentences:
            detailed_innovation = self._create_detailed_bullet(innovation_sentences, 2)
            bullets.append(f"**Innovation Aspects:** {detailed_innovation}")
        
        return bullets[:target_bullets]
    
    def _generate_literature_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate comprehensive content for Literature Review section."""
        bullets = []
        
        # Current state of technology and existing solutions
        current_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['current', 'existing', 'traditional', 'conventional', 'state of the art', 'present', 'available', 'existing solution'])]
        if current_sentences:
            detailed_current = self._create_detailed_bullet(current_sentences, 4)
            bullets.append(f"**Current State of Technology:** {detailed_current}")
        
        # Related work and research studies
        related_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['related', 'previous', 'existing work', 'literature', 'research', 'study', 'paper', 'publication', 'article'])]
        if related_sentences:
            detailed_related = self._create_detailed_bullet(related_sentences, 4)
            bullets.append(f"**Related Research & Studies:** {detailed_related}")
        
        # Technology trends and evolution
        trend_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['trend', 'development', 'advancement', 'evolution', 'progress', 'innovation', 'emerging', 'latest', 'recent'])]
        if trend_sentences:
            detailed_trends = self._create_detailed_bullet(trend_sentences, 4)
            bullets.append(f"**Technology Trends & Evolution:** {detailed_trends}")
        
        # Challenges and limitations in existing systems
        challenge_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['challenge', 'limitation', 'drawback', 'issue', 'problem', 'difficulty', 'obstacle', 'weakness', 'shortcoming'])]
        if challenge_sentences:
            detailed_challenges = self._create_detailed_bullet(challenge_sentences, 4)
            bullets.append(f"**Current Challenges & Limitations:** {detailed_challenges}")
        
        # Research gaps and opportunities
        gap_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['gap', 'need', 'requirement', 'opportunity', 'potential', 'future', 'missing', 'unexplored', 'untapped'])]
        if gap_sentences:
            detailed_gaps = self._create_detailed_bullet(gap_sentences, 4)
            bullets.append(f"**Research Gaps & Opportunities:** {detailed_gaps}")
        
        # Market analysis and industry adoption
        market_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['market', 'adoption', 'industry', 'commercial', 'business', 'enterprise', 'sector', 'field'])]
        if market_sentences:
            detailed_market = self._create_detailed_bullet(market_sentences, 3)
            bullets.append(f"**Market Analysis & Industry Adoption:** {detailed_market}")
        
        # Cost and resource considerations
        cost_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['cost', 'budget', 'resource', 'infrastructure', 'investment', 'expense', 'economic', 'financial'])]
        if cost_sentences:
            detailed_cost = self._create_detailed_bullet(cost_sentences, 3)
            bullets.append(f"**Cost & Resource Considerations:** {detailed_cost}")
        
        # Educational context and applications
        education_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['education', 'learning', 'teaching', 'academic', 'institution', 'student', 'classroom', 'school'])]
        if education_sentences:
            detailed_education = self._create_detailed_bullet(education_sentences, 3)
            bullets.append(f"**Educational Context & Applications:** {detailed_education}")
        
        # Comparative analysis of existing solutions
        comparison_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['compare', 'versus', 'better', 'alternative', 'solution', 'approach', 'different', 'similar'])]
        if comparison_sentences:
            detailed_comparison = self._create_detailed_bullet(comparison_sentences, 3)
            bullets.append(f"**Comparative Analysis of Solutions:** {detailed_comparison}")
        
        # User needs and requirements analysis
        user_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['user', 'need', 'requirement', 'demand', 'expectation', 'satisfaction', 'preference', 'behavior'])]
        if user_sentences:
            detailed_user = self._create_detailed_bullet(user_sentences, 3)
            bullets.append(f"**User Needs & Requirements Analysis:** {detailed_user}")
        
        # Technical standards and protocols
        standard_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['standard', 'protocol', 'specification', 'guideline', 'best practice', 'framework', 'methodology'])]
        if standard_sentences:
            detailed_standards = self._create_detailed_bullet(standard_sentences, 3)
            bullets.append(f"**Technical Standards & Protocols:** {detailed_standards}")
        
        # Performance and evaluation metrics
        performance_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['performance', 'evaluation', 'metric', 'measure', 'assessment', 'benchmark', 'criteria'])]
        if performance_sentences:
            detailed_performance = self._create_detailed_bullet(performance_sentences, 3)
            bullets.append(f"**Performance & Evaluation Metrics:** {detailed_performance}")
        
        # Security and privacy considerations
        security_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['security', 'privacy', 'protection', 'safety', 'vulnerability', 'risk'])]
        if security_sentences:
            detailed_security = self._create_detailed_bullet(security_sentences, 3)
            bullets.append(f"**Security & Privacy Considerations:** {detailed_security}")
        
        # Scalability and deployment challenges
        scalability_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['scalability', 'deployment', 'implementation', 'production', 'real-world', 'practical'])]
        if scalability_sentences:
            detailed_scalability = self._create_detailed_bullet(scalability_sentences, 3)
            bullets.append(f"**Scalability & Deployment Challenges:** {detailed_scalability}")
        
        # Future research directions
        future_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['future', 'direction', 'prospect', 'potential', 'next generation', 'emerging'])]
        if future_sentences:
            detailed_future = self._create_detailed_bullet(future_sentences, 3)
            bullets.append(f"**Future Research Directions:** {detailed_future}")
        
        return bullets[:target_bullets]
    
    def _generate_methods_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate comprehensive content for Methods section."""
        bullets = []
        
        # Research methodology and approach
        method_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['method', 'methodology', 'approach', 'technique', 'strategy', 'procedure', 'research method'])]
        if method_sentences:
            detailed_methodology = self._create_detailed_bullet(method_sentences, 4)
            bullets.append(f"**Research Methodology & Approach:** {detailed_methodology}")
        
        # System architecture and design
        architecture_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['architecture', 'design', 'structure', 'framework', 'system design', 'component', 'modular'])]
        if architecture_sentences:
            detailed_architecture = self._create_detailed_bullet(architecture_sentences, 4)
            bullets.append(f"**System Architecture & Design:** {detailed_architecture}")
        
        # Implementation process and development
        implementation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['implement', 'develop', 'create', 'build', 'deploy', 'construct', 'development process'])]
        if implementation_sentences:
            detailed_implementation = self._create_detailed_bullet(implementation_sentences, 5)
            bullets.append(f"**Implementation Process & Development:** {detailed_implementation}")
        
        # Tools, technologies, and platforms
        tool_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['tool', 'technology', 'software', 'platform', 'library', 'framework', 'api', 'language', 'programming'])]
        if tool_sentences:
            detailed_tools = self._create_detailed_bullet(tool_sentences, 4)
            bullets.append(f"**Tools, Technologies & Platforms:** {detailed_tools}")
        
        # Data collection and processing methodology
        data_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['data', 'dataset', 'collection', 'gathering', 'processing', 'analysis', 'storage', 'preprocessing'])]
        if data_sentences:
            detailed_data = self._create_detailed_bullet(data_sentences, 4)
            bullets.append(f"**Data Collection & Processing Methodology:** {detailed_data}")
        
        # Algorithm design and computational methods
        algorithm_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['algorithm', 'model', 'function', 'procedure', 'process', 'mechanism', 'computational', 'mathematical'])]
        if algorithm_sentences:
            detailed_algorithm = self._create_detailed_bullet(algorithm_sentences, 4)
            bullets.append(f"**Algorithm Design & Computational Methods:** {detailed_algorithm}")
        
        # User interface and interaction design
        ui_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['interface', 'user', 'interaction', 'experience', 'gui', 'usability', 'design', 'layout'])]
        if ui_sentences:
            detailed_ui = self._create_detailed_bullet(ui_sentences, 3)
            bullets.append(f"**User Interface & Interaction Design:** {detailed_ui}")
        
        # Performance optimization and efficiency
        performance_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['performance', 'optimization', 'efficiency', 'speed', 'accuracy', 'quality', 'improvement'])]
        if performance_sentences:
            detailed_performance = self._create_detailed_bullet(performance_sentences, 3)
            bullets.append(f"**Performance Optimization & Efficiency:** {detailed_performance}")
        
        # Evaluation methodology and testing procedures
        evaluation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['evaluation', 'metric', 'measure', 'assessment', 'testing', 'validation', 'experiment', 'benchmark'])]
        if evaluation_sentences:
            detailed_evaluation = self._create_detailed_bullet(evaluation_sentences, 4)
            bullets.append(f"**Evaluation Methodology & Testing Procedures:** {detailed_evaluation}")
        
        # Security, reliability, and robustness
        security_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['security', 'reliability', 'robustness', 'stability', 'error handling', 'protection', 'safety'])]
        if security_sentences:
            detailed_security = self._create_detailed_bullet(security_sentences, 3)
            bullets.append(f"**Security, Reliability & Robustness:** {detailed_security}")
        
        # Database design and storage architecture
        database_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['database', 'storage', 'server', 'client', 'network', 'data management'])]
        if database_sentences:
            detailed_database = self._create_detailed_bullet(database_sentences, 3)
            bullets.append(f"**Database Design & Storage Architecture:** {detailed_database}")
        
        # Communication protocols and system integration
        communication_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['communication', 'integration', 'api', 'protocol', 'connection', 'interoperability'])]
        if communication_sentences:
            detailed_communication = self._create_detailed_bullet(communication_sentences, 3)
            bullets.append(f"**Communication Protocols & System Integration:** {detailed_communication}")
        
        # Development environment and deployment setup
        environment_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['environment', 'setup', 'configuration', 'installation', 'deployment', 'infrastructure'])]
        if environment_sentences:
            detailed_environment = self._create_detailed_bullet(environment_sentences, 3)
            bullets.append(f"**Development Environment & Deployment Setup:** {detailed_environment}")
        
        # Quality assurance and testing methodology
        quality_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['quality', 'assurance', 'testing', 'verification', 'validation', 'debugging', 'error'])]
        if quality_sentences:
            detailed_quality = self._create_detailed_bullet(quality_sentences, 3)
            bullets.append(f"**Quality Assurance & Testing Methodology:** {detailed_quality}")
        
        # Scalability and performance considerations
        scalability_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['scalability', 'performance', 'capacity', 'load', 'throughput', 'concurrent'])]
        if scalability_sentences:
            detailed_scalability = self._create_detailed_bullet(scalability_sentences, 3)
            bullets.append(f"**Scalability & Performance Considerations:** {detailed_scalability}")
        
        # Risk assessment and mitigation strategies
        risk_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['risk', 'assessment', 'mitigation', 'vulnerability', 'threat', 'safety'])]
        if risk_sentences:
            detailed_risk = self._create_detailed_bullet(risk_sentences, 3)
            bullets.append(f"**Risk Assessment & Mitigation Strategies:** {detailed_risk}")
        
        # Cost analysis and resource management
        cost_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['cost', 'budget', 'resource', 'management', 'economic', 'financial', 'investment'])]
        if cost_sentences:
            detailed_cost = self._create_detailed_bullet(cost_sentences, 3)
            bullets.append(f"**Cost Analysis & Resource Management:** {detailed_cost}")
        
        return bullets[:target_bullets]
    
    def _generate_results_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Results section."""
        bullets = []
        
        # Performance results and metrics
        performance_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['performance', 'result', 'outcome', 'achievement', 'metric', 'score'])]
        if performance_sentences:
            detailed_performance = self._create_detailed_bullet(performance_sentences, 3)
            bullets.append(f"**Performance Results:** {detailed_performance}")
        
        # Key findings and discoveries
        finding_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['finding', 'discovery', 'observation', 'analysis', 'insight', 'conclusion'])]
        if finding_sentences:
            detailed_findings = self._create_detailed_bullet(finding_sentences, 3)
            bullets.append(f"**Key Findings:** {detailed_findings}")
        
        # Comparative analysis and benchmarks
        comparison_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['compare', 'versus', 'better', 'improvement', 'benchmark', 'alternative'])]
        if comparison_sentences:
            detailed_comparison = self._create_detailed_bullet(comparison_sentences, 3)
            bullets.append(f"**Comparative Analysis:** {detailed_comparison}")
        
        # User feedback and experience
        feedback_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['feedback', 'user', 'experience', 'satisfaction', 'usability', 'interface'])]
        if feedback_sentences:
            detailed_feedback = self._create_detailed_bullet(feedback_sentences, 3)
            bullets.append(f"**User Experience:** {detailed_feedback}")
        
        # System evaluation and testing
        evaluation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['evaluation', 'assessment', 'testing', 'validation', 'verification', 'experiment'])]
        if evaluation_sentences:
            detailed_evaluation = self._create_detailed_bullet(evaluation_sentences, 3)
            bullets.append(f"**System Evaluation:** {detailed_evaluation}")
        
        # Accuracy and reliability results
        accuracy_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['accuracy', 'reliability', 'precision', 'efficiency', 'effectiveness', 'quality'])]
        if accuracy_sentences:
            detailed_accuracy = self._create_detailed_bullet(accuracy_sentences, 2)
            bullets.append(f"**Accuracy & Reliability:** {detailed_accuracy}")
        
        # Cost and resource analysis
        cost_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['cost', 'budget', 'resource', 'efficiency', 'savings', 'economic'])]
        if cost_sentences:
            detailed_cost = self._create_detailed_bullet(cost_sentences, 2)
            bullets.append(f"**Cost Analysis:** {detailed_cost}")
        
        # Scalability and deployment results
        scalability_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['scalability', 'deployment', 'production', 'real-world', 'implementation', 'practical'])]
        if scalability_sentences:
            detailed_scalability = self._create_detailed_bullet(scalability_sentences, 2)
            bullets.append(f"**Scalability Results:** {detailed_scalability}")
        
        # Speed and response time results
        speed_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['speed', 'time', 'response', 'latency', 'duration', 'fast'])]
        if speed_sentences:
            detailed_speed = self._create_detailed_bullet(speed_sentences, 2)
            bullets.append(f"**Speed & Response Time:** {detailed_speed}")
        
        # Error rates and success metrics
        error_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['error', 'success', 'failure', 'rate', 'percentage', 'statistic'])]
        if error_sentences:
            detailed_error = self._create_detailed_bullet(error_sentences, 2)
            bullets.append(f"**Error Rates & Success Metrics:** {detailed_error}")
        
        # User adoption and acceptance
        adoption_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['adoption', 'acceptance', 'usage', 'utilization', 'implementation'])]
        if adoption_sentences:
            detailed_adoption = self._create_detailed_bullet(adoption_sentences, 2)
            bullets.append(f"**User Adoption & Acceptance:** {detailed_adoption}")
        
        # Technical performance indicators
        technical_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['technical', 'system', 'infrastructure', 'capacity', 'throughput'])]
        if technical_sentences:
            detailed_technical = self._create_detailed_bullet(technical_sentences, 2)
            bullets.append(f"**Technical Performance:** {detailed_technical}")
        
        return bullets[:target_bullets]
    
    def _generate_discussion_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
        """Generate content for Discussion section."""
        bullets = []
        
        # Interpretation of results
        interpretation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['interpret', 'explain', 'understand', 'meaning', 'analysis'])]
        if interpretation_sentences:
            detailed_interpretation = self._create_detailed_bullet(interpretation_sentences, 3)
            bullets.append(f"**Result Interpretation:** {detailed_interpretation}")
        
        # Implications and significance
        implication_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['implication', 'impact', 'significance', 'consequence', 'importance'])]
        if implication_sentences:
            detailed_implications = self._create_detailed_bullet(implication_sentences, 3)
            bullets.append(f"**Implications & Significance:** {detailed_implications}")
        
        # Limitations and constraints
        limitation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['limitation', 'constraint', 'drawback', 'weakness', 'challenge'])]
        if limitation_sentences:
            detailed_limitations = self._create_detailed_bullet(limitation_sentences, 3)
            bullets.append(f"**Limitations & Constraints:** {detailed_limitations}")
        
        # Future work and improvements
        future_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['future', 'next', 'improvement', 'enhancement', 'development'])]
        if future_sentences:
            detailed_future = self._create_detailed_bullet(future_sentences, 3)
            bullets.append(f"**Future Work & Improvements:** {detailed_future}")
        
        # Practical applications and deployment
        application_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['application', 'deployment', 'practical', 'real-world', 'implementation'])]
        if application_sentences:
            detailed_applications = self._create_detailed_bullet(application_sentences, 2)
            bullets.append(f"**Practical Applications:** {detailed_applications}")
        
        # Industry impact and adoption potential
        industry_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['industry', 'market', 'adoption', 'commercial', 'business'])]
        if industry_sentences:
            detailed_industry = self._create_detailed_bullet(industry_sentences, 2)
            bullets.append(f"**Industry Impact:** {detailed_industry}")
        
        # Educational implications
        education_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['education', 'learning', 'teaching', 'academic', 'student'])]
        if education_sentences:
            detailed_education = self._create_detailed_bullet(education_sentences, 2)
            bullets.append(f"**Educational Implications:** {detailed_education}")
        
        # Technical challenges and solutions
        technical_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['technical', 'challenge', 'solution', 'problem', 'issue'])]
        if technical_sentences:
            detailed_technical = self._create_detailed_bullet(technical_sentences, 2)
            bullets.append(f"**Technical Challenges:** {detailed_technical}")
        
        # User experience considerations
        user_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['user', 'experience', 'interface', 'usability', 'satisfaction'])]
        if user_sentences:
            detailed_user = self._create_detailed_bullet(user_sentences, 2)
            bullets.append(f"**User Experience Considerations:** {detailed_user}")
        
        # Cost-benefit analysis
        cost_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['cost', 'benefit', 'economic', 'investment', 'saving'])]
        if cost_sentences:
            detailed_cost = self._create_detailed_bullet(cost_sentences, 2)
            bullets.append(f"**Cost-Benefit Analysis:** {detailed_cost}")
        
        # Recommendations and suggestions
        recommendation_sentences = [s for s in important_sentences if any(word in s.lower() for word in ['recommendation', 'suggestion', 'proposal', 'advice', 'guideline'])]
        if recommendation_sentences:
            detailed_recommendations = self._create_detailed_bullet(recommendation_sentences, 2)
            bullets.append(f"**Recommendations:** {detailed_recommendations}")
        
        return bullets[:target_bullets]
    
    def _generate_conclusion_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
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
    
    def _generate_general_content(self, text: str, important_sentences: List[str], target_bullets: int) -> List[str]:
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
    
    def _create_detailed_bullet(self, sentences: List[str], max_sentences: int = 3) -> str:
        """Create a detailed bullet point by combining multiple sentences."""
        if not sentences:
            return ""
        
        # Take up to max_sentences and combine them
        selected_sentences = sentences[:max_sentences]
        combined = " ".join([self._clean_sentence(s) for s in selected_sentences])
        
        # Ensure it's not too long (max 100 words for more comprehensive content)
        words = combined.split()
        if len(words) > 100:
            combined = " ".join(words[:100])
            if not combined.endswith('.'):
                combined += '.'
        
        return combined
