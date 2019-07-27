from jinja2 import FileSystemLoader, Environment

class Report_Generator:

    def __init__(self):
        # Configure Jinja and ready the loader
        self.env = Environment(loader=FileSystemLoader(searchpath="Template"))

        # Assemble the templates we'll use
        self.base_template = self.env.get_template("report_template.html")
        self.table_section_template = self.env.get_template("table_section.html")

        # Content to be published
        self.title = "Car Report"
        self.sections = list()
        return

    def add_table(self, car_name, car_price, summary):
        self.sections.append(self.table_section_template.render(
            car_name=car_name,
            car_price=car_price,
            summary=summary,
        ))
        return

    def make_report(self):
        with open("Outputs/Car_Finder_Report.html", "w") as f:
            f.write(self.base_template.render(title=self.title, sections=self.sections))
        return
