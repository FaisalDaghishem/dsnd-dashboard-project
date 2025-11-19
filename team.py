# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies for SQL execution
from .sql_execution import QueryMixin


class Team(QueryBase, QueryMixin):
    # Set the class attribute name to "team"
    name = "team"

    # Define a names method (returns a list of tuples)
    def names(self):
        # Query 5
        query = f"""
            SELECT team_name, team_id
            FROM {self.name}
            ORDER BY team_name
        """
        return self.query(query)

    # Define a username method (returns a list of tuples)
    def username(self, id):
        # Query 6
        query = f"""
            SELECT team_name
            FROM {self.name}
            WHERE {self.name}_id = {id}
        """
        return self.query(query)

    # Machine learning model data (do NOT edit this)
    def model_data(self, id):
        return f"""
            SELECT positive_events, negative_events FROM (
                SELECT employee_id
                    , SUM(positive_events) positive_events
                    , SUM(negative_events) negative_events
                FROM {self.name}
                JOIN employee_events 
                USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """