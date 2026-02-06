from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
from datetime import datetime

def generate_pdf(vehicle, entries, from_address, to_address, start_date, end_date):
    """Generate PDF report for transport entries"""
    
    # Create output directory if it doesn't exist
    output_dir = 'generated_pdfs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/{vehicle.name}_{timestamp}.pdf'
    
    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        alignment=TA_LEFT
    )
    
    # Add header section with From and To addresses
    header_data = [
        [
            Paragraph(f'<b>FROM:</b><br/>{from_address.replace(chr(10), "<br/>")}', header_style),
            Paragraph(f'<b>TO:</b><br/>{to_address.replace(chr(10), "<br/>")}', header_style)
        ]
    ]
    
    header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    # Add title
    title = Paragraph(f'Transport Report - {vehicle.name}', title_style)
    story.append(title)
    
    # Add date range
    date_range = Paragraph(
        f'<b>Period:</b> {start_date.strftime("%d/%m/%Y")} to {end_date.strftime("%d/%m/%Y")}',
        styles['Normal']
    )
    story.append(date_range)
    story.append(Spacer(1, 20))
    
    # Create table data
    table_data = [
        ['Date', 'Route', 'KM', 'Rate', 'Amount', 'Extra', 'Total']
    ]
    
    total_km = 0
    total_amount = 0
    total_extra = 0
    grand_total = 0
    
    for entry in entries:
        table_data.append([
            entry.date.strftime('%d/%m/%Y'),
            entry.route_name,
            f'{entry.km_driven:.2f}',
            f'₹{entry.rate:.2f}',
            f'₹{entry.amount:.2f}',
            f'₹{entry.extra:.2f}',
            f'₹{entry.total_amount:.2f}'
        ])
        total_km += entry.km_driven
        total_amount += entry.amount
        total_extra += entry.extra
        grand_total += entry.total_amount
    
    # Add totals row
    table_data.append([
        'TOTAL',
        '',
        f'{total_km:.2f}',
        '',
        f'₹{total_amount:.2f}',
        f'₹{total_extra:.2f}',
        f'₹{grand_total:.2f}'
    ])
    
    # Create table
    col_widths = [1*inch, 1.8*inch, 0.8*inch, 0.9*inch, 1.1*inch, 0.9*inch, 1.1*inch]
    table = Table(table_data, colWidths=col_widths)
    
    # Style table
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Align numbers to right
        ('ALIGN', (0, 1), (1, -1), 'LEFT'),    # Align text to left
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFA726')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('TOPPADDING', (0, -1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        
        # Alternate row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Add summary
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )
    
    story.append(Paragraph('<b>Summary:</b>', summary_style))
    story.append(Paragraph(f'Total Entries: {len(entries)}', summary_style))
    story.append(Paragraph(f'Total Kilometers: {total_km:.2f} km', summary_style))
    story.append(Paragraph(f'Total Amount: ₹{grand_total:.2f}', summary_style))
    
    # Build PDF
    doc.build(story)
    
    return filename
