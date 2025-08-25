"""Simple section mapping for the specific paper structure."""

def map_sections_by_content(text: str) -> dict:
    """Map sections based on content keywords and structure."""
    sections = {}
    
    # Clean the text by removing zero-width spaces and other special characters
    text_clean = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    # Define section keywords and their canonical names
    section_keywords = {
        "INTRODUCTION": ["1. INTRODUCTION", "INTRODUCTION"],
        "METHODS": ["3. METHODOLOGY", "METHODOLOGY"],
        "RESULTS": ["4. RESULTS", "RESULTS", "4. RESULTS & ANALYSIS"],
        "DISCUSSION": ["DISCUSSION", "ANALYSIS"],
        "CONCLUSION": ["5. CONCLUSION", "CONCLUSION"],
        "LITERATURE": ["2. LITERATURE REVIEW", "LITERATURE REVIEW"],
        "ABSTRACT": ["ABSTRACT", "ABSTRACT:"]
    }
    
    # Find all section positions
    section_positions = []
    for canon_name, keywords in section_keywords.items():
        for keyword in keywords:
            pos = text_clean.upper().find(keyword.upper())
            if pos != -1:
                section_positions.append((pos, canon_name, keyword))
    
    # Sort by position
    section_positions.sort()
    
    if not section_positions:
        # If no sections found, treat entire text as OTHER
        sections["OTHER"] = text
        return sections
    
    # Extract sections
    for i, (pos, canon_name, keyword) in enumerate(section_positions):
        # Find the end of this section (start of next section or end of text)
        if i + 1 < len(section_positions):
            end_pos = section_positions[i + 1][0]
        else:
            end_pos = len(text_clean)
        
        # Extract section content
        section_content = text_clean[pos:end_pos].strip()
        sections[canon_name] = section_content
    
    return sections
