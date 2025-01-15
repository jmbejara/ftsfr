# app/series.py

import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app import db
from .models import TimeSeries, SeriesGroup, Keyword


class SeriesSearcher:
    """
    A utility class providing searching capabilities for TimeSeries and/or SeriesGroup
    based on a single search string, but with multiple booleans to control which attributes
    to match (name, code, keyword, etc.).
    """

    @classmethod
    def search(
        cls,
        search_text: str,
        search_by_name: bool = True,
        search_by_code: bool = True,
        search_by_keyword: bool = True,
        partial: bool = True,
        search_time_series: bool = True,
        search_series_group: bool = True,
        session=None,
        limit_rows: int = 100,
        print_findings: bool = False,
    ) -> pd.DataFrame:
        """
        Searches TimeSeries and/or SeriesGroup based on a single search string.
        The user can choose to apply that search string to name, code, and/or keyword fields.

        Parameters
        ----------
        search_text : str
            The text to match against name, code, or keywords.
        search_by_name : bool, default True
            If True, match `search_text` against the name field.
        search_by_code : bool, default True
            If True, match `search_text` against the code field
            (time_series_code for TimeSeries, series_group_code for SeriesGroup).
        search_by_keyword : bool, default True
            If True, match `search_text` against the related keywords' word field.
        partial : bool, default True
            If True, performs partial/ILIKE matching. If False, uses exact match.
        search_time_series : bool, default True
            Whether to include TimeSeries in the search.
        search_series_group : bool, default True
            Whether to include SeriesGroup in the search.
        session : Session, optional
            Existing SQLAlchemy session. If None, uses db.session.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing matched records, with columns:
            ["type", "id", "name", "code", "description", "keywords"].
        """
        # check if space is present in the search_text
        if " " in search_text:
            search_texts = search_text.split(" ")
            all_dfs = []
            for spec_search_text in search_texts:
                df = cls.search(
                    search_text=spec_search_text,
                    search_by_name=search_by_name,
                    search_by_code=search_by_code,
                    search_by_keyword=search_by_keyword,
                    partial=partial,
                    search_time_series=search_time_series,
                    search_series_group=search_series_group,
                    session=session,
                    limit_rows=limit_rows,
                    print_findings=print_findings,
                )
                if isinstance(df, pd.DataFrame):
                    all_dfs.append(df)
            if len(all_dfs) > 0:
                df = pd.concat(all_dfs)
                df = df.drop_duplicates(["id"])
                return cls.limit_rows_of_df(df, limit_rows)
            else:
                return None

        if session is None:
            session = db.session

        # Normalize search_text just in case:
        if not search_text:
            # If there's no text, just return empty results
            return pd.DataFrame(
                columns=["type", "id", "name", "code", "description", "keywords"]
            )

        # Prepare the final list of dict rows for our DataFrame
        result_rows = []

        # Define the filter condition based on partial or exact match
        def get_filter(column):
            if partial:
                return column.ilike(f"%{search_text}%")
            else:
                return column == search_text

        if search_time_series:
            # Start base query with joinedload for keywords
            ts_query = session.query(TimeSeries).options(
                joinedload(TimeSeries.keywords)
            )

            or_conditions = []

            # a) By name
            if search_by_name:
                or_conditions.append(get_filter(TimeSeries.name))

            # b) By code
            if search_by_code:
                or_conditions.append(get_filter(TimeSeries.time_series_code))

            # c) By keyword using `any()`
            if search_by_keyword:
                if partial:
                    keyword_filter = TimeSeries.keywords.any(
                        Keyword.word.ilike(f"%{search_text}%")
                    )
                else:
                    keyword_filter = TimeSeries.keywords.any(
                        Keyword.word == search_text
                    )
                or_conditions.append(keyword_filter)

            # Combine all conditions with OR
            if or_conditions:
                ts_query = ts_query.filter(or_(*or_conditions))

            # Execute the query
            ts_list = ts_query.all()

            # Debug: Print matched TimeSeries
            if print_findings:
                print(f"Matched TimeSeries ({len(ts_list)}):")
                for ts in ts_list:
                    print(
                        f" - ID: {ts.id}, Name: {ts.name}, Code: {ts.time_series_code}, Keywords: {[kw.word for kw in ts.keywords]}"
                    )

            # Convert TimeSeries results to row dicts
            for ts in ts_list:
                kw_list = [kw.word for kw in ts.keywords]
                row = {
                    "type": "TimeSeries",
                    "id": ts.id,
                    "name": ts.name,
                    "code": ts.time_series_code,
                    "description": ts.description,
                    "keywords": ", ".join(kw_list),
                }
                result_rows.append(row)

        if search_series_group:
            # Start base query with joinedload for keywords
            sg_query = session.query(SeriesGroup).options(
                joinedload(SeriesGroup.keywords)
            )

            or_conditions = []

            # a) By name
            if search_by_name:
                or_conditions.append(get_filter(SeriesGroup.name))

            # b) By code
            if search_by_code:
                or_conditions.append(get_filter(SeriesGroup.series_group_code))

            # c) By keyword using `any()`
            if search_by_keyword:
                if partial:
                    keyword_filter = SeriesGroup.keywords.any(
                        Keyword.word.ilike(f"%{search_text}%")
                    )
                else:
                    keyword_filter = SeriesGroup.keywords.any(
                        Keyword.word == search_text
                    )
                or_conditions.append(keyword_filter)

            # Combine all conditions with OR
            if or_conditions:
                sg_query = sg_query.filter(or_(*or_conditions))

            # Execute the query
            sg_list = sg_query.all()

            # Debug: Print matched SeriesGroups
            if print_findings:
                print(f"Matched SeriesGroups ({len(sg_list)}):")
                for sg in sg_list:
                    print(
                        f" - ID: {sg.id}, Name: {sg.name}, Code: {sg.series_group_code}, Keywords: {[kw.word for kw in sg.keywords]}"
                    )

            # Convert SeriesGroup results to row dicts
            for sg in sg_list:
                kw_list = [kw.word for kw in sg.keywords]
                row = {
                    "type": "SeriesGroup",
                    "id": sg.id,
                    "name": sg.name,
                    "code": sg.series_group_code,
                    "description": sg.description,
                    "keywords": ", ".join(kw_list),
                }
                result_rows.append(row)

        df = pd.DataFrame(result_rows)

        if df.empty:
            return None

        cls.limit_rows_of_df(df, limit_rows)

        return df

    @staticmethod
    def limit_rows_of_df(df, limit_rows):
        if isinstance(limit_rows, bool) and limit_rows:
            limit_rows = 100

        if isinstance(limit_rows, int):
            df = df.head(limit_rows)

        return df
