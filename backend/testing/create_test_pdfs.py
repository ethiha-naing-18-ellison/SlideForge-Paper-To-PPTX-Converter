#!/usr/bin/env python3
"""
Script to create 7 different test PDF files with various document types and structures
for testing the SlideForge application.
"""

import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, red, green, purple, orange, brown
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def create_pdf(filename, title, content_sections, doc_type="Document"):
    """Create a PDF file with the given title and content sections."""
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=blue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=black
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Build the story
    story = []
    
    # Add title
    story.append(Paragraph(f"{title}", title_style))
    story.append(Spacer(1, 20))
    
    # Add document type
    story.append(Paragraph(f"Document Type: {doc_type}", heading_style))
    story.append(Spacer(1, 10))
    
    # Add content sections
    for section_title, section_content in content_sections:
        story.append(Paragraph(section_title, heading_style))
        story.append(Paragraph(section_content, body_style))
        story.append(Spacer(1, 10))
    
    # Build the PDF
    doc.build(story)
    print(f"Created: {filename}")

def main():
    """Create 7 different test PDF files."""
    
    # 1. Report Type
    report_content = [
        ("Executive Summary", 
         "This report provides a comprehensive analysis of the quarterly performance metrics for Q3 2024. The analysis covers key performance indicators, market trends, and strategic recommendations for the upcoming quarter."),
        ("Methodology", 
         "Data was collected from multiple sources including internal databases, customer surveys, and market research reports. Statistical analysis was performed using advanced analytics tools to ensure accuracy and reliability."),
        ("Key Findings", 
         "Revenue increased by 15% compared to the previous quarter. Customer satisfaction scores improved by 8%. Market share expanded by 2.3% in the target demographic. Operational efficiency improved by 12% through process optimization."),
        ("Recommendations", 
         "Continue investment in digital transformation initiatives. Expand customer support channels. Implement new marketing strategies targeting emerging markets. Enhance product development pipeline."),
        ("Conclusion", 
         "The Q3 results demonstrate strong performance across all key metrics. The strategic initiatives implemented in the previous quarter have yielded positive results. Continued focus on innovation and customer satisfaction will drive future growth.")
    ]
    create_pdf("test_report_type.pdf", "Quarterly Performance Report Q3 2024", report_content, "Report")

    # 2. User Manual
    manual_content = [
        ("Introduction", 
         "Welcome to the Advanced Data Analytics Platform User Manual. This comprehensive guide will help you navigate through all features and functionalities of the system. The platform is designed to provide powerful data analysis capabilities for business users."),
        ("Installation Guide", 
         "To install the platform, download the installer from the official website. Run the setup wizard and follow the on-screen instructions. Ensure your system meets the minimum requirements: Windows 10/11, 8GB RAM, 2GB free disk space."),
        ("Getting Started", 
         "After installation, launch the application and create your user account. The dashboard provides quick access to all major features. Use the navigation menu to explore different modules and functionalities."),
        ("Core Features", 
         "Data Import: Support for CSV, Excel, and JSON files. Visualization Tools: Create charts, graphs, and interactive dashboards. Analysis Tools: Statistical analysis, trend detection, and predictive modeling. Export Options: Generate reports in PDF, Excel, or PowerPoint formats."),
        ("Troubleshooting", 
         "If you encounter issues, check the system requirements and ensure all dependencies are installed. Contact technical support with detailed error messages and system information. Regular updates are available through the application's update mechanism.")
    ]
    create_pdf("test_user_manual.pdf", "Advanced Data Analytics Platform - User Manual", manual_content, "User Manual")

    # 3. Research Paper
    research_content = [
        ("Abstract", 
         "This study investigates the impact of artificial intelligence on modern healthcare systems. Through comprehensive analysis of implementation cases and patient outcomes, we demonstrate significant improvements in diagnostic accuracy and treatment efficiency."),
        ("Introduction", 
         "Artificial intelligence has emerged as a transformative technology in healthcare, offering unprecedented opportunities for improving patient care and operational efficiency. This research examines the practical applications and measurable outcomes of AI integration in clinical settings."),
        ("Literature Review", 
         "Previous studies have shown varying degrees of success in AI healthcare applications. Research by Johnson et al. (2023) demonstrated 23% improvement in diagnostic accuracy. Smith and colleagues (2024) reported 15% reduction in treatment time through AI-assisted decision support systems."),
        ("Methodology", 
         "We conducted a multi-center study involving 15 hospitals across three countries. Data was collected over 18 months, including patient records, treatment outcomes, and physician feedback. Statistical analysis was performed using advanced machine learning algorithms."),
        ("Results", 
         "The study revealed significant improvements across all measured parameters. Diagnostic accuracy increased by 28%, treatment time decreased by 22%, and patient satisfaction scores improved by 35%. Cost savings averaged 18% across participating institutions."),
        ("Discussion", 
         "These findings support the widespread adoption of AI technologies in healthcare. However, challenges remain in implementation, training, and regulatory compliance. Future research should focus on long-term outcomes and scalability."),
        ("Conclusion", 
         "AI integration in healthcare shows promising results with measurable improvements in patient care and operational efficiency. Continued research and development are essential for maximizing the potential benefits while addressing implementation challenges.")
    ]
    create_pdf("test_research_paper.pdf", "Impact of Artificial Intelligence on Healthcare Systems: A Multi-Center Study", research_content, "Research Paper")

    # 4. School Project Report
    school_project_content = [
        ("Project Overview", 
         "Our science project explores the effects of different light wavelengths on plant growth. We hypothesized that blue light would promote faster growth compared to red and green light. This project was conducted over a period of 6 weeks in our school laboratory."),
        ("Materials and Methods", 
         "We used three identical plant pots with the same soil type and seed variety. Each pot was placed under different colored LED lights: blue, red, and green. We measured plant height daily and recorded observations about leaf color and overall health."),
        ("Experimental Setup", 
         "The experiment was conducted in a controlled environment with consistent temperature and humidity. Plants were watered equally and received 12 hours of light exposure daily. Measurements were taken at the same time each day to ensure consistency."),
        ("Results", 
         "After 6 weeks, plants under blue light showed 25% more growth compared to red light and 40% more than green light. Leaf color was also more vibrant under blue light. Plants under green light showed the slowest growth rate."),
        ("Analysis", 
         "Our results support the hypothesis that blue light promotes better plant growth. This is likely due to blue light's role in photosynthesis and chlorophyll production. The findings align with previous research on light spectrum effects on plant development."),
        ("Conclusion", 
         "Blue light significantly enhances plant growth compared to other wavelengths. This knowledge can be applied to indoor gardening and agricultural practices. Future experiments could explore different plant species and light intensity variations.")
    ]
    create_pdf("test_school_project.pdf", "Effects of Light Wavelength on Plant Growth - Science Project Report", school_project_content, "School Project Report")

    # 5. School Assignment
    assignment_content = [
        ("Assignment Title", 
         "Critical Analysis of Shakespeare's 'Macbeth': Character Development and Themes"),
        ("Introduction", 
         "This assignment examines the character development of Macbeth and Lady Macbeth throughout the play, analyzing how their relationship evolves and contributes to the overall themes of ambition, guilt, and fate."),
        ("Character Analysis - Macbeth", 
         "Macbeth begins as a loyal and honorable warrior, respected by his peers and king. However, his encounter with the witches and his wife's influence trigger his tragic flaw of ambition. His transformation from hero to tyrant demonstrates Shakespeare's exploration of how power corrupts."),
        ("Character Analysis - Lady Macbeth", 
         "Lady Macbeth initially appears stronger and more ambitious than her husband. She manipulates Macbeth into committing regicide, but her strength proves to be her downfall. Her eventual descent into madness shows the psychological consequences of guilt and evil deeds."),
        ("Thematic Analysis", 
         "The play explores several key themes: the corrupting nature of power, the relationship between gender and violence, the consequences of unchecked ambition, and the role of fate versus free will. These themes are developed through the characters' actions and dialogue."),
        ("Literary Devices", 
         "Shakespeare employs various literary devices including dramatic irony, foreshadowing, and symbolism. The recurring motif of blood represents guilt and the impossibility of washing away evil deeds. The witches' prophecies create dramatic tension and explore fate."),
        ("Conclusion", 
         "Macbeth serves as a powerful exploration of human nature and the consequences of ambition. The character development of Macbeth and Lady Macbeth provides insight into how power and guilt can destroy even the strongest individuals.")
    ]
    create_pdf("test_school_assignment.pdf", "Macbeth Character Analysis - English Literature Assignment", assignment_content, "School Assignment")

    # 6. Assignment Report
    assignment_report_content = [
        ("Executive Summary", 
         "This assignment report presents a comprehensive analysis of modern cybersecurity threats and defense strategies. The research covers emerging threats, current defense mechanisms, and recommendations for improving organizational security posture."),
        ("Problem Statement", 
         "With the increasing digitization of business operations, organizations face growing cybersecurity challenges. Traditional security measures are no longer sufficient against sophisticated cyber attacks. This report identifies key vulnerabilities and proposes effective countermeasures."),
        ("Research Objectives", 
         "The primary objectives were to identify current cybersecurity threats, analyze existing defense strategies, evaluate their effectiveness, and propose improvements. Secondary objectives included cost-benefit analysis of security measures and risk assessment methodologies."),
        ("Methodology", 
         "Research was conducted through literature review, case study analysis, and expert interviews. Data was collected from academic sources, industry reports, and real-world incident reports. Analysis was performed using qualitative and quantitative methods."),
        ("Key Findings", 
         "Phishing attacks remain the most common threat vector. Ransomware attacks have increased by 150% in the last year. Social engineering techniques are becoming more sophisticated. Many organizations lack comprehensive incident response plans."),
        ("Recommendations", 
         "Implement multi-factor authentication across all systems. Conduct regular security awareness training for employees. Develop comprehensive incident response procedures. Invest in advanced threat detection and response tools."),
        ("Implementation Plan", 
         "Phase 1: Security assessment and gap analysis. Phase 2: Implementation of basic security controls. Phase 3: Advanced security measures deployment. Phase 4: Monitoring and continuous improvement."),
        ("Conclusion", 
         "Effective cybersecurity requires a multi-layered approach combining technical controls, employee training, and organizational policies. Regular assessment and adaptation to emerging threats is essential for maintaining security posture.")
    ]
    create_pdf("test_assignment_report.pdf", "Cybersecurity Threats and Defense Strategies - Assignment Report", assignment_report_content, "Assignment Report")

    # 7. Documentation
    documentation_content = [
        ("System Overview", 
         "The Enterprise Resource Planning (ERP) System is a comprehensive software solution designed to integrate and manage core business processes. This documentation provides detailed information about system architecture, configuration, and usage."),
        ("Architecture", 
         "The system follows a three-tier architecture: presentation layer (web interface), business logic layer (application server), and data layer (database). Built using Java Enterprise Edition with Oracle database backend. Supports multiple deployment models including on-premise and cloud."),
        ("Installation and Setup", 
         "System requirements: Java 11+, Oracle Database 19c, 16GB RAM minimum. Installation process involves database setup, application server configuration, and web server deployment. Detailed setup scripts and configuration files are provided in the installation package."),
        ("User Management", 
         "Role-based access control with predefined user roles: Administrator, Manager, Employee, and Viewer. User authentication supports LDAP integration and multi-factor authentication. Password policies enforce security requirements and regular updates."),
        ("Module Configuration", 
         "Core modules include: Financial Management, Human Resources, Inventory Management, and Customer Relationship Management. Each module can be configured independently with specific business rules and workflows. Custom fields and reports can be added as needed."),
        ("Database Schema", 
         "The database consists of 150+ tables organized into functional schemas. Primary tables include users, organizations, transactions, and audit logs. Foreign key relationships maintain data integrity across modules. Indexing strategies optimize query performance."),
        ("API Documentation", 
         "RESTful API endpoints provide integration capabilities with external systems. Authentication uses OAuth 2.0 with JWT tokens. API responses follow standard HTTP status codes and JSON format. Rate limiting and throttling prevent abuse."),
        ("Troubleshooting", 
         "Common issues include database connection problems, memory allocation errors, and configuration conflicts. Diagnostic tools provide detailed error logging and system health monitoring. Support procedures include escalation paths and resolution timeframes."),
        ("Maintenance", 
         "Regular maintenance tasks include database backups, log rotation, and performance monitoring. Patch management follows a quarterly release schedule. System updates require scheduled downtime and rollback procedures are documented.")
    ]
    create_pdf("test_documentation.pdf", "Enterprise Resource Planning System - Technical Documentation", documentation_content, "Documentation")

    print("\nAll 7 test PDF files have been created successfully!")
    print("Files created:")
    print("1. test_report_type.pdf - Report Type")
    print("2. test_user_manual.pdf - User Manual")
    print("3. test_research_paper.pdf - Research Paper")
    print("4. test_school_project.pdf - School Project Report")
    print("5. test_school_assignment.pdf - School Assignment")
    print("6. test_assignment_report.pdf - Assignment Report")
    print("7. test_documentation.pdf - Documentation")

if __name__ == "__main__":
    main()
