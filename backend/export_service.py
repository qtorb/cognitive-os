"""
Export Service para Cognitive OS — Genera PDFs y JSON.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import io
import json
from sqlalchemy.orm import Session
from models import User, Decision, PersonalPattern, Analysis


def generate_export_pdf(user: User, db: Session) -> bytes:
    """
    Genera un PDF con decisiones y patrones del usuario.
    Retorna el PDF como bytes.
    """
    # Obtener datos
    decisions = db.query(Decision).filter(Decision.user_id == user.user_id).all()
    patterns = db.query(PersonalPattern).filter(PersonalPattern.user_id == user.user_id).all()

    # Crear buffer
    pdf_buffer = io.BytesIO()

    # Crear documento PDF
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Estilos
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    # Story para el PDF
    story = []

    # Portada
    story.append(Paragraph("🧠 Cognitive OS", title_style))
    story.append(Paragraph("Reporte de Decisiones Personales", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 6))

    # Información del usuario
    story.append(PageBreak())
    story.append(Paragraph("📋 Perfil del Usuario", heading_style))

    user_info = [
        ["Campo", "Valor"],
        ["Email", user.email or "—"],
        ["Rol", user.role or "—"],
        ["Áreas de Decisión", ", ".join(user.decision_areas) if user.decision_areas else "—"],
        ["Horizonte", user.horizon or "—"],
        ["Registrado", user.created_at.strftime('%d/%m/%Y') if user.created_at else "—"],
    ]

    user_table = Table(user_info, colWidths=[2*inch, 3.5*inch])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')])
    ]))

    story.append(user_table)
    story.append(Spacer(1, 12))

    # Resumen de Decisiones
    story.append(Paragraph("📊 Resumen de Decisiones", heading_style))

    total_decisions = len(decisions)
    completed = sum(1 for d in decisions if d.status == "completed")
    in_progress = sum(1 for d in decisions if d.status == "analyzing" or d.status == "reviewing")
    drafts = sum(1 for d in decisions if d.status == "draft")

    summary_text = f"""
    <b>Total de decisiones:</b> {total_decisions}<br/>
    <b>Completadas:</b> {completed} ({int(completed/max(total_decisions, 1)*100)}%)<br/>
    <b>En análisis:</b> {in_progress}<br/>
    <b>Borradores:</b> {drafts}<br/>
    """

    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Patrones Descubiertos
    if patterns:
        story.append(PageBreak())
        story.append(Paragraph("🎯 Tus Patrones Personales", heading_style))
        story.append(Spacer(1, 6))

        for pattern in patterns:
            pattern_text = f"""
            <b>{pattern.icon} {pattern.title}</b><br/>
            <font size=9>{pattern.description}</font><br/>
            <font size=8 color="#718096">
            Fuerza inicial: {pattern.initial_strength}/10 → Actual: {pattern.current_strength}/10
            </font>
            """
            story.append(Paragraph(pattern_text, styles['Normal']))
            story.append(Spacer(1, 10))

    # Últimas decisiones (primeras 5)
    if decisions:
        story.append(PageBreak())
        story.append(Paragraph("🔍 Últimas Decisiones", heading_style))
        story.append(Spacer(1, 6))

        for decision in decisions[:5]:
            decision_text = f"""
            <b>{decision.title}</b><br/>
            <font size=9>
            Área: {decision.area} | Tipo: {decision.decision_type}<br/>
            Convicción: {decision.conviction}/10 | Estado: {decision.status}<br/>
            </font>
            <font size=8 color="#718096">
            {decision.context[:100]}...
            </font>
            """
            story.append(Paragraph(decision_text, styles['Normal']))
            story.append(Spacer(1, 12))

    # Footer
    story.append(PageBreak())
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("—", styles['Normal']))
    story.append(Paragraph(
        "Este reporte fue generado automáticamente por Cognitive OS.<br/>"
        "Tus decisiones y patrones son privados y están encriptados.",
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER)
    ))

    # Generar PDF
    doc.build(story)

    # Obtener bytes
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
