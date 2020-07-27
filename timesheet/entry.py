from timesheet import models as db
from timesheet.conf import Session


class DisplayEntry:
    """Class to handle updating/organizing data for displaying the entry"""

    def __init__(self, entries):
        self.employee = entries[0].employee
        self.project = entries[0].project
        self.ending_date = entries[0].ending_date
        self.entries = entries
        self.hours = [e.days for e in entries]

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours = value

    @property
    def project_totals(self):
        totals = []
        for hr in self.hours:
            totals.append(sum(hr))
        return totals

    @property
    def day_totals(self):
        totals = [0 for _ in range(7)]
        for hr in self.hours:
            totals = [sum(hours) for hours in zip(totals, hr)]
        return totals

    @property
    def notes(self):
        return [e.note for e in self.entries]

    @property
    def projects(self):
        return [e.project for e in self.entries]

    @property
    def rows(self):
        _rows = []
        for project, hours, project_total, note in zip(
            self.projects, self.hours, self.project_totals, self.notes
        ):
            row = []
            if project is None:
                row.append(None)
            else:
                row.append(project.number)
            row.extend(hours)
            row.extend([project_total, note])
            # _rows.append([project.number, hours, project_total, note])
            _rows.append(row)
        return _rows


def main():
    session = Session()
    # entries = session.query(db.Entry).all()
    # for e in entries:
    #     print(e)

    entries = session.query(db.Entry).filter_by(ending_date="1975-11-12").all()
    de = DisplayEntry(entries)
    print(de.project_totals)
    print(de.day_totals)
    print(de.hours)
    print(de.notes)
    print(de.projects)
    print(de.rows)
    for row in de.rows:
        print(row)


if __name__ == "__main__":
    main()
