import pandas as pd
from sqlalchemy.exc import IntegrityError

from manage import db
from invisible_flow.copa.data_allegation import DataAllegation


class Loader:

    def __init__(self):
        self.matches = []
        self.new_data = []

    def load_into_db(self, transformed_data: pd.DataFrame):

        for row in transformed_data.itertuples():

            new_allegation = DataAllegation(cr_id=row.cr_id)
            db.session.add(new_allegation)
            try:
                db.session.commit()
            except IntegrityError:
                self.matches.append(transformed_data.iloc[row[0]])
                db.session.rollback()
            else:
                self.new_data.append(transformed_data.iloc[row[0]])

        db.session.close()

    def original_load_strategy(self, transformed_data: pd.DataFrame):
        self.existing_crid = pd.DataFrame(DataAllegation.query.with_entities(DataAllegation.cr_id)).values.flatten().tolist()

        for row in transformed_data.itertuples():
            if row.cr_id not in self.existing_crid:
               new_allegation = DataAllegation(cr_id=row.cr_id)
               db.session.add(new_allegation)
               self.new_data.append(transformed_data.iloc[row[0]])
            else:
                self.matches.append(transformed_data.iloc[row[0]])

        db.session.close()

    def get_matches(self):
        return self.matches

    def get_new_data(self):
        return self.new_data
