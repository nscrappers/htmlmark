"""Generate human-readable extraction reports from pipeline results."""

from dataclasses import dataclass, field
from typing import List, Optional
from htmlmark.summary import TableSummary, ListSummary


@dataclass
class ReportSection:
    title: str
    lines: List[str] = field(default_factory=list)

    def add(self, line: str) -> None:
        self.lines.append(line)

    def render(self) -> str:
        header = f"## {self.title}"
        body = "\n".join(f"  {l}" for l in self.lines)
        return f"{header}\n{body}" if self.lines else header


@dataclass
class ExtractionReport:
    title: str = "htmlmark Extraction Report"
    sections: List[ReportSection] = field(default_factory=list)

    def add_section(self, section: ReportSection) -> None:
        self.sections.append(section)

    def render(self) -> str:
        parts = [f"# {self.title}"]
        for s in self.sections:
            parts.append(s.render())
        return "\n\n".join(parts)


def report_from_table_summary(summary: TableSummary, label: Optional[str] = None) -> ExtractionReport:
    report = ExtractionReport(title=label or "Table Extraction Report")
    sec = ReportSection("Table Summary")
    sec.add(f"Rows extracted : {summary.row_count}")
    sec.add(f"Columns        : {summary.column_count}")
    sec.add(f"Has header     : {summary.has_header}")
    if summary.column_names:
        sec.add(f"Column names   : {', '.join(summary.column_names)}")
    report.add_section(sec)
    return report


def report_from_list_summary(summary: ListSummary, label: Optional[str] = None) -> ExtractionReport:
    report = ExtractionReport(title=label or "List Extraction Report")
    sec = ReportSection("List Summary")
    sec.add(f"Items extracted : {summary.item_count}")
    sec.add(f"Max depth       : {summary.max_depth}")
    sec.add(f"Ordered         : {summary.ordered}")
    report.add_section(sec)
    return report


def combine_reports(*reports: ExtractionReport, title: str = "Combined Report") -> ExtractionReport:
    combined = ExtractionReport(title=title)
    for r in reports:
        for sec in r.sections:
            combined.add_section(sec)
    return combined
