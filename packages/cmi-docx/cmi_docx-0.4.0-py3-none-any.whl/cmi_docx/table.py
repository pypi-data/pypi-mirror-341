"""Extends a python-docx Table cell with additional functionality."""

from docx import oxml, table
from docx.oxml import ns

from cmi_docx import paragraph, styles


class ExtendCell:
    """Extends a python-docx Word cell with additional functionality."""

    def __init__(self, cell: table._Cell) -> None:
        """Initializes an ExtendCell object.

        Args:
            cell: The cell to extend.
        """
        self.cell = cell

    def format(self, style: styles.CellStyle) -> None:
        """Formats a cell in a Word table.

        Args:
            style: The style to apply to the cell.
        """
        if style.paragraph is not None:
            for table_paragraph in self.cell.paragraphs:
                paragraph.ExtendParagraph(table_paragraph).format(style.paragraph)

        if style.background_rgb is not None:
            shading = oxml.parse_xml(
                (
                    r'<w:shd {} w:fill="'
                    + f"{rgb_to_hex(*style.background_rgb)}"
                    + r'"/>'
                ).format(
                    ns.nsdecls("w"),
                ),
            )
            self.cell._tc.get_or_add_tcPr().append(shading)  # noqa: SLF001

        if style.borders:
            for border in style.borders:
                self._apply_border(border)

    def _apply_border(self, border: styles.CellBorder) -> None:
        """Applies the borders styling to the cell.

        Args:
            border: The style to apply to the cell.
        """
        tc_pr = self.cell._tc.get_or_add_tcPr()

        tc_borders = tc_pr.first_child_found_in("w:tcBorders")
        if tc_borders is None:
            tc_borders = oxml.OxmlElement("w:tcBorders")
            tc_pr.append(tc_borders)

        for edge in border.sides:
            tag = "w:{}".format(edge)
            element = tc_borders.find(ns.qn(tag))
            if element is None:
                element = oxml.OxmlElement(tag)
                tc_borders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color"]:
                if value := getattr(border, key):
                    element.set(ns.qn("w:{}".format(key)), str(value))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converts RGB values to a hexadecimal color code.

    Args:
        r: The red component of the RGB color.
        g: The green component of the RGB color.
        b: The blue component of the RGB color.

    Returns:
        The hexadecimal color code representing the RGB color.
    """
    return f"#{r:02x}{g:02x}{b:02x}".upper()
