from pathlib import Path
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter


class ExcelExport:

    @staticmethod
    def export(rows, headers, file_prefix):
        export_dir = Path("exportacoes")
        export_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = export_dir / f"{file_prefix}_{timestamp}.xlsx"

        wb = Workbook()
        ws = wb.active

        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for row in rows:
            ws.append(row)

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        for column in ws.columns:
            max_length = max(len(str(cell.value or "")) for cell in column)
            ws.column_dimensions[get_column_letter(column[0].column)].width = max_length + 2

        wb.save(file_path)

        return str(file_path.resolve())