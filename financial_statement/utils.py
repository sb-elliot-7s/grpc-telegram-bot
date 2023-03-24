class Utils:

    @staticmethod
    def parse_year(report_dict: dict) -> str:
        return report_dict.get('acceptedDate').split()[0].split('-')[0]

    @staticmethod
    def get_pdf_url_or_none(pdf: str | bytes) -> str | None:
        return pdf if isinstance(pdf, str) else None
