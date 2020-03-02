from reportlab.graphics import shapes
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.units import cm, mm, inch, pica
import labels

BORDER=False
OR_CURRENT = True

SPECS = labels.Specification(216, 279, 3, 10, 66, 25,
        corner_radius=2,
        left_margin=6,
        right_margin=4,
        column_gap=4,
        top_margin=15,
        bottom_margin=14,
        row_gap=0,
        )

# 215.9 by 279.4
def write_label(label, width, height, person):
    lines = [
        person.name,
        person.address,
    ]
    if OR_CURRENT and len("\n".join(lines).split('\n')) < 4:
        lines.insert(1, "Or current resident",)
    elif OR_CURRENT:
        print("Skipping Or Current Resident for long address:\n{}", "\n".join(lines))
    text = "\n".join(lines)
    text = "\n".join([line.strip() for line in text.splitlines()])
    lab = Label()
    lab.setOrigin(5, height - 5)
    lab.fontSize = 12
    lab.setText(text)
    lab.boxAnchor = 'nw'
    label.add(lab)

def make_labels(people, outfile):
    sheet = labels.Sheet(SPECS, write_label, border=BORDER)
    sheet.add_labels(people)
    sheet.save(outfile)

