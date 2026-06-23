
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def create_pdf_report(
    output_file,
    insights
):

    doc = SimpleDocTemplate(
        output_file
    )

    styles = (
        getSampleStyleSheet()
    )

    story = []

    story.append(
        Paragraph(
            "CSV Analytics Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,12)
    )

    for item in insights:

        story.append(
            Paragraph(
                item,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,6)
        )

    doc.build(story)
